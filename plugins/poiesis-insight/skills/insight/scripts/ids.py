#!/usr/bin/env python3
"""Ids and `From` lines in a project's notes: the next free id, what rests on what, and what went stale when a
verdict changed. It reports; it changes nothing. Run with `python3 -I`.

  ids.py next IN            the next free id for a prefix: IN-004
  ids.py list [--prefix IN] every object with an id: its note, its day, its From and its verdict
  ids.py stale              objects that rest on something dropped, weakened or challenged again since

An object is a heading with a line `- **Id:** IN-001` under it. `- **From:** IN-001, QN-002, some-note` names
what it rests on: ids, note names and citation keys, separated by commas. Its day is its own line
`- **Written:** YYYY-MM-DD` or, without one, the date that starts the note's file name.

`stale` reads the challenge stamps (`insights/challenge-stamps.jsonl`) and prints one line per finding:

  STALE           something in From was dropped, weakened or challenged again after the object's day
  THROUGH         the object rests on an object that is stale
  DROPPED SOURCE  something in From had already been dropped on the object's day
  SAME DAY        something in From was challenged again on the object's day: which came first is not known
  NO DATE         the object has no day, so nothing can be said about it

A verdict given on the object's own day is not called stale: on one day the usual order is challenge, then
build. Days are compared, not hours.

Looks in `research`, `insights`, `foresight`, `frontier` and `design` under --root (default: the current
folder); --folders names others. Numbers are never reused: `next` also counts ids that appear only in a From
line or in a stamp. Rows of a log table (F-001, E-001) are not objects here.

Exit codes: 0 when nothing is stale (for `next` and `list`: always, unless the stamp file is damaged);
1 when `stale` finds something, or the stamp file is damaged; 2 a wrong command line.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import challenge_stamp as stamps  # noqa: E402  (the same folder; -I leaves it off the path)

FOLDERS = ("research", "insights", "foresight", "frontier", "design")
OBJECT_ID_RE = re.compile(r"[A-Z]{1,3}-\d+")
PREFIX_RE = re.compile(r"[A-Z]{1,3}")
FROM_LINE_RE = re.compile(r"^[ \t]*[-*+][ \t]+\*\*from:?\*\*:?[ \t]*(.*)$", re.IGNORECASE)
WRITTEN_LINE_RE = re.compile(r"^[ \t]*[-*+][ \t]+\*\*written:?\*\*:?[ \t]*(\d{4}-\d{2}-\d{2})\b", re.IGNORECASE)
FILE_DAY_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:\D|$)")
CITATION_RE = re.compile(r"\[@[^\]]*\]")


def from_items(value: str) -> list[str]:
    """The entries of a From line. A citation such as `[@key, p. 4]` stays whole."""
    kept = CITATION_RE.findall(value)
    rest = CITATION_RE.sub(",", value)
    parts = [part.strip(" \t`*[]().") for part in re.split(r"[,;]", rest)]
    return [part for part in parts if part] + kept


def read_objects(root: Path, folders: tuple[str, ...]) -> tuple[list[dict], list[str]]:
    """Every object under the folders, in path order, and the ids found more than once."""
    found: list[dict] = []
    seen: dict[str, str] = {}
    twice: list[str] = []
    for folder in folders:
        base = root / folder
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            if any(part.startswith(".") for part in path.relative_to(root).parts):
                continue
            try:
                text = path.read_text(encoding="utf-8-sig")
            except (OSError, UnicodeDecodeError):
                continue
            name = path.relative_to(root).as_posix()
            file_day = FILE_DAY_RE.match(path.name)
            for heading, lines in stamps.blocks(text):
                id_ = day = None
                rests_on: list[str] = []
                for line in lines:
                    hit = stamps.ID_LINE_RE.match(line)
                    if hit and id_ is None:
                        id_ = hit.group(1)
                    hit = FROM_LINE_RE.match(line)
                    if hit and not rests_on:
                        rests_on = from_items(hit.group(1))
                    hit = WRITTEN_LINE_RE.match(line)
                    if hit and day is None:
                        day = hit.group(1)
                if id_ is None:
                    continue
                if id_ in seen:
                    if id_ not in twice:
                        twice.append(id_)
                    continue
                seen[id_] = name
                found.append({"id": id_, "text": stamps.normalise(heading), "file": name,
                              "day": day or (file_day.group(1) if file_day else None), "from": rests_on})
    return found, twice


def next_id(prefix: str, objects: list[dict], ledger: stamps.Ledger) -> str:
    pattern = re.compile(re.escape(prefix) + r"-(\d+)")
    numbers = [0]
    names = [obj["id"] for obj in objects] + [item for obj in objects for item in obj["from"]] + list(ledger.entries)
    for name in names:
        hit = pattern.fullmatch(name)
        if hit:
            numbers.append(int(hit.group(1)))
    return f"{prefix}-{max(numbers) + 1:03d}"


def findings(objects: list[dict], ledger: stamps.Ledger) -> list[tuple[str, dict, str]]:
    """(kind, object, sentence) for every finding, in the order of the objects."""
    by_id = {obj["id"]: obj for obj in objects}
    direct: dict[str, list[tuple[str, str]]] = {}
    for obj in objects:
        lines: list[tuple[str, str]] = []
        sources = [item for item in obj["from"] if OBJECT_ID_RE.fullmatch(item) and ledger.times(item)]
        if sources and obj["day"] is None:
            lines.append(("NO DATE", "no `Written` line and no date in the file name; From names "
                                     + ", ".join(sources) + ", which carry a verdict"))
        for source in sources if obj["day"] else []:
            entries = [stamp for _, stamp, _ in ledger.entries[source] if stamp]
            for position, stamp in enumerate(entries):
                first = position == 0
                what = f"{source} was {stamp['verdict']}" if first else f"{source} was challenged again " \
                                                                         f"({stamp['verdict']})"
                why = f": {stamp['again']}" if stamp.get("again") else ""
                if stamp["date"] > obj["day"]:
                    if first and stamp["verdict"] == "kept":
                        continue          # a first challenge that kept the conclusion changes nothing
                    lines.append(("STALE", f"{what} on {stamp['date']}{why}"))
                elif stamp["date"] == obj["day"] and not first:
                    lines.append(("SAME DAY", f"{what} on {stamp['date']}{why}, the object's own day"))
            current, _ = ledger.current(source)
            if current and current["verdict"] == "dropped" and current["date"] <= obj["day"]:
                lines.append(("DROPPED SOURCE", f"{source} was dropped on {current['date']}, on or before "
                                                "the object's day"))
        direct[obj["id"]] = lines

    stale = {id_ for id_, lines in direct.items() if any(kind == "STALE" for kind, _ in lines)}
    through: dict[str, str] = {}
    changed = True
    while changed:                       # staleness travels along From
        changed = False
        for obj in objects:
            if obj["id"] in stale:
                continue
            via = next((item for item in obj["from"] if item in stale and item in by_id), None)
            if via:
                stale.add(obj["id"])
                through[obj["id"]] = via
                changed = True

    out = []
    for obj in objects:
        for kind, sentence in direct[obj["id"]]:
            out.append((kind, obj, sentence))
        if obj["id"] in through:
            out.append(("THROUGH", obj, f"rests on {through[obj['id']]}, which is stale"))
    return out


def describe(obj: dict) -> str:
    return f"{obj['id']} ({obj['file']}, {obj['day'] or 'no date'})"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("next", "list", "stale"))
    parser.add_argument("prefix", nargs="?", help="for `next`: the letters before the dash, such as IN or QN")
    parser.add_argument("--prefix", dest="only", help="for `list`: only ids with this prefix")
    parser.add_argument("--root", default=".", help="the project's folder (default: the current one)")
    parser.add_argument("--folders", nargs="+", default=list(FOLDERS), help="folders under the root to read")
    parser.add_argument("--stamps", help=f"the stamp file (default {stamps.DEFAULT_STAMPS} under the root)")
    args = parser.parse_args(argv)

    root = Path(args.root)
    try:
        ledger = stamps.Ledger(Path(args.stamps) if args.stamps else root / stamps.DEFAULT_STAMPS)
    except stamps.Unreadable as problem:
        print(f"ids.py: {problem}", file=sys.stderr)
        return 2
    objects, twice = read_objects(root, tuple(args.folders))
    damaged = bool(ledger.damaged)
    for number, why in ledger.damaged:
        print(f"DAMAGED line {number} of {ledger.path} {why}: verdicts cannot be trusted until it is repaired")
    for id_ in twice:
        print(f"TWICE {id_}: the id is under more than one heading; only the first is read")

    if args.command == "next":
        if not args.prefix or not PREFIX_RE.fullmatch(args.prefix):
            parser.error("next needs a prefix of one to three capital letters, such as IN")
        print(next_id(args.prefix, objects, ledger))
        return 1 if damaged else 0

    if args.command == "list":
        shown = [obj for obj in objects if not args.only or obj["id"].startswith(args.only + "-")]
        for obj in shown:
            stamp, why = ledger.current(obj["id"])
            verdict = f"{stamp['verdict']} {stamp['date']}" if stamp else ("stamp altered" if why else "no stamp")
            rests_on = ", ".join(obj["from"]) or "-"
            print(f"{obj['id']} | {obj['file']} | {obj['day'] or 'no date'} | {verdict} | From: {rests_on} | "
                  f"{obj['text']}")
        print(f"{len(shown)} objects in {', '.join(args.folders)}.")
        return 1 if damaged else 0

    found = findings(objects, ledger)
    for kind, obj, sentence in found:
        print(f"{kind} {describe(obj)}: {sentence}")
    with_from = sum(1 for obj in objects if obj["from"])
    print(f"{len(objects)} objects read, {with_from} with a From line: {len(found)} "
          f"finding{'' if len(found) == 1 else 's'}.")
    return 1 if found or damaged else 0


if __name__ == "__main__":
    sys.exit(main())
