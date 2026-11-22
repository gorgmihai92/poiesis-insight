#!/usr/bin/env python3
"""Record a challenge verdict once, and check later that nobody changed it. Run with `python3 -I`.

  challenge_stamp.py write  --note FILE --id IN-001 --verdict weakened [--by agent|inline]
  challenge_stamp.py write  --note FILE --verdicts ANSWER.md           [--by agent|inline]
  challenge_stamp.py write  --id IN-001 --verdict kept (--text "..." | --text-file FILE)
  challenge_stamp.py verify --note FILE [--id IN-001 ...]
  challenge_stamp.py verify --id IN-001 (--text "..." | --text-file FILE) [--verdict kept]
  challenge_stamp.py list

A stamp is one line of JSON in `insights/challenge-stamps.jsonl` (`--stamps PATH` for another file):

  {"v": 1, "id": "IN-001", "verdict": "weakened", "date": "2026-11-22", "text_sha256": "...", "seal": "..."}

- `text_sha256` is the SHA-256 of the conclusion's sentence after `normalise()` below. In a note the sentence is
  the heading above the line `- **Id:** IN-001`.
- `seal` is the SHA-256 of the five lines `poiesis-challenge-stamp v1`, id, verdict, date, text_sha256, joined
  by a line feed. A line edited by hand no longer matches its seal.
- `by`, `again` and `where` are notes for the reader. They are not sealed.

`write` appends a line and never changes an earlier one. A conclusion that already has a stamp is refused,
unless `--again "why"` records a new challenge; the last line for an id is its current stamp. With `--verdicts`
the verdicts are read from the challenger's saved answer, so no label is typed by hand.

`verify` fails when the stamp is missing, when the sentence is no longer the one stamped, when the verdict shown
with the conclusion is not the stamped one, or when the stamp's line was altered.

Exit codes: 0 written, or everything checked is in order; 1 refused, or something does not verify; 2 a wrong
command line or a file that cannot be read.

The stamp is a seal against drift and retyping. It is not a signature: whoever can run this script can write a
stamp, so it makes a change visible and does not prevent one.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

VERSION = 1
VERDICTS = ("kept", "weakened", "dropped")
DEFAULT_STAMPS = "insights/challenge-stamps.jsonl"
SEAL_HEAD = "poiesis-challenge-stamp v1"

ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
HEX64_RE = re.compile(r"[0-9a-f]{64}")
SPACE_RE = re.compile(r"[\t\n\x0b\x0c\r ]+")

HEADING_RE = re.compile(r"^#{1,6}[ \t]+(.*)$")
FENCE_RE = re.compile(r"^[ \t]*(```|~~~)")
ID_LINE_RE = re.compile(r"^[ \t]*[-*+][ \t]+\*\*id:?\*\*:?[ \t]*(\S+)[ \t]*$", re.IGNORECASE)
CHALLENGE_LINE_RE = re.compile(r"^[ \t]*[-*+][ \t]+\*\*challenge:?\*\*:?[ \t]*(.*)$", re.IGNORECASE)
VERDICT_LINE_RE = re.compile(r"^[ \t]*[-*+][ \t]+\*\*verdict:?\*\*:?[ \t]*(.*)$", re.IGNORECASE)
NARROWER_LINE_RE = re.compile(r"^[ \t]*[-*+][ \t]+\*\*narrower:?\*\*:?[ \t]*(.*)$", re.IGNORECASE)
ITEM_RE = re.compile(r"^[ \t]*[-*+][ \t]+")
FIRST_WORD_RE = re.compile(r"[A-Za-z]+")
NO_NARROWER = {"", "-", "–", "—", "none", "none.", "n/a", "not applicable", "null"}


class Refused(Exception):
    """The command is understood and is not carried out (exit code 1)."""


class Unreadable(Exception):
    """A file cannot be read, or the command line is wrong (exit code 2)."""


# ---------- the text and its hash

def normalise(text: str) -> str:
    """The form of a conclusion's sentence that is hashed: Unicode NFC, each run of tab, line feed, vertical
    tab, form feed, carriage return and space turned into one space, and the spaces at both ends removed.
    Nothing else changes: capitals, punctuation, dashes, quotes and no-break spaces stay as typed."""
    return SPACE_RE.sub(" ", unicodedata.normalize("NFC", text)).strip(" ")


def text_hash(text: str) -> str:
    return hashlib.sha256(normalise(text).encode("utf-8")).hexdigest()


def seal_of(id_: str, verdict: str, date: str, text_sha256: str) -> str:
    lines = (SEAL_HEAD, id_, verdict, date, text_sha256)
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def make_stamp(id_: str, verdict: str, date: str, text: str, by: str | None = None,
               again: str | None = None, where: str | None = None) -> dict:
    digest = text_hash(text)
    stamp = {"v": VERSION, "id": id_, "verdict": verdict, "date": date, "text_sha256": digest,
             "seal": seal_of(id_, verdict, date, digest)}
    if by:
        stamp["by"] = by
    if again:
        stamp["again"] = again
    if where:
        stamp["where"] = where
    return stamp


def stamp_line(stamp: dict) -> str:
    return json.dumps(stamp, ensure_ascii=False)


def label_head(value: str) -> str:
    """A label as it is written, up to the `·` that starts its reason, without the bold marks."""
    return normalise(value.split("·")[0].replace("*", ""))


def first_word(value: str) -> str:
    """The first word of a label such as `**Weakened** · narrower`, in lower case; '' when there is none."""
    found = FIRST_WORD_RE.search(value or "")
    return found.group(0).lower() if found else ""


# ---------- the stamp file

class Ledger:
    """What a stamp file holds: `stamps` in file order, the lines that cannot be attributed to a conclusion
    (`damaged`), and for each id the lines that were altered (`altered`)."""

    def __init__(self, path: Path):
        self.path = path
        self.exists = path.is_file()
        self.stamps: list[dict] = []
        self.damaged: list[tuple[int, str]] = []
        self.entries: dict[str, list[tuple[int, dict | None, str]]] = {}
        if self.exists:
            try:
                lines = path.read_text(encoding="utf-8-sig").splitlines()
            except (OSError, UnicodeDecodeError) as err:
                raise Unreadable(f"cannot read {path}: {err}")
            for number, line in enumerate(lines, 1):
                if line.strip():
                    self._take(number, line)

    def _take(self, number: int, line: str) -> None:
        try:
            stamp = json.loads(line)
        except ValueError:
            self.damaged.append((number, "is not JSON"))
            return
        if not isinstance(stamp, dict) or not isinstance(stamp.get("id"), str) \
                or not ID_RE.fullmatch(stamp["id"]):
            self.damaged.append((number, "has no readable id"))
            return
        why = flaw(stamp)
        if why:
            self.entries.setdefault(stamp["id"], []).append((number, None, why))
            return
        stamp = dict(stamp, line=number)
        self.stamps.append(stamp)
        self.entries.setdefault(stamp["id"], []).append((number, stamp, ""))

    def current(self, id_: str) -> tuple[dict | None, str]:
        """The stamp in force for an id and '' when it can be trusted; otherwise None and the reason. The last
        line for an id is in force, and an altered last line is never replaced by an earlier one."""
        if self.damaged:
            number, why = self.damaged[0]
            return None, f"line {number} of {self.path} {why}, so the file cannot be trusted"
        entries = self.entries.get(id_)
        if not entries:
            return None, ""
        number, stamp, why = entries[-1]
        if stamp is None:
            return None, f"line {number} of {self.path} {why}"
        return stamp, ""

    def times(self, id_: str) -> int:
        return len(self.entries.get(id_, []))

    def append(self, stamps: list[dict]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        ends_clean = True
        if self.exists and self.path.stat().st_size:
            with self.path.open("rb") as handle:
                handle.seek(-1, 2)
                ends_clean = handle.read(1) == b"\n"
        with self.path.open("a", encoding="utf-8", newline="\n") as handle:
            if not ends_clean:
                handle.write("\n")
            for stamp in stamps:
                handle.write(stamp_line(stamp) + "\n")


def flaw(stamp: dict) -> str:
    """Why a line with a readable id is not a valid stamp, or ''."""
    if stamp.get("v") != VERSION:
        return f"has version {stamp.get('v')!r}, and this script reads version {VERSION}"
    verdict, date, digest, seal = (stamp.get(key) for key in ("verdict", "date", "text_sha256", "seal"))
    if verdict not in VERDICTS:
        return f"has the verdict {verdict!r}, which is not one of {', '.join(VERDICTS)}"
    if not isinstance(date, str) or not DATE_RE.fullmatch(date):
        return "has no date in the form YYYY-MM-DD"
    if not isinstance(digest, str) or not HEX64_RE.fullmatch(digest):
        return "has no text_sha256 of 64 hexadecimal digits"
    if seal != seal_of(stamp["id"], verdict, date, digest):
        return "does not match its seal: it was changed after it was written"
    return ""


# ---------- conclusions in a note

def read_file(path: str | Path) -> str:
    try:
        return Path(path).read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as err:
        raise Unreadable(f"cannot read {path}: {err}")


def blocks(markdown: str) -> list[tuple[str, list[str]]]:
    """Each heading with the lines under it, up to the next heading. Lines inside a fenced code block are
    skipped, so a `#` comment in code is not taken for a heading."""
    found: list[tuple[str, list[str]]] = []
    fenced = False
    for line in markdown.splitlines():
        if FENCE_RE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        heading = HEADING_RE.match(line)
        if heading:
            found.append((heading.group(1), []))
        elif found:
            found[-1][1].append(line)
    return found


def conclusions(markdown: str) -> tuple[dict[str, dict], list[str]]:
    """The conclusions of a note by id: `text` is the heading, `shown` the first word of the Challenge line
    ('' when the block has none) and `has_challenge_line` whether the line is there. Also the ids that appear
    under more than one heading."""
    by_id: dict[str, dict] = {}
    twice: list[str] = []
    for heading, lines in blocks(markdown):
        id_ = None
        label = None
        for line in lines:
            found = ID_LINE_RE.match(line)
            if found and id_ is None:
                id_ = found.group(1)
            found = CHALLENGE_LINE_RE.match(line)
            if found and label is None:
                label = found.group(1)
        if id_ is None:
            continue
        if id_ in by_id:
            if id_ not in twice:
                twice.append(id_)
            continue
        by_id[id_] = {"id": id_, "text": heading, "shown": first_word(label or ""),
                      "label": label_head(label or ""), "has_challenge_line": label is not None}
    return by_id, twice


def field(lines: list[str], pattern: re.Pattern) -> str | None:
    """The value of the first line that matches, with the lines it runs on to: a value ends at an empty line,
    at the next list item, or at a line that starts with a bold label such as `**Tally:**`."""
    for index, line in enumerate(lines):
        hit = pattern.match(line)
        if hit:
            parts = [hit.group(1)]
            for more in lines[index + 1:]:
                if not more.strip() or ITEM_RE.match(more) or more.lstrip().startswith("**"):
                    break
                parts.append(more)
            return " ".join(parts)
    return None


def answer_verdicts(markdown: str) -> list[dict]:
    """The verdicts in a challenger's saved answer: one block per conclusion, a heading that starts with the
    id, a line `- **Verdict:** kept|weakened|dropped`, and for a weakened one `- **Narrower:** the claim that
    survives`. Headings with no Verdict line are not verdicts."""
    found = []
    for heading, lines in blocks(markdown):
        verdict = field(lines, VERDICT_LINE_RE)
        narrower = field(lines, NARROWER_LINE_RE)
        if verdict is None:
            continue
        token = heading.split()[0].strip("*`:·,.") if heading.split() else ""
        narrower = normalise(narrower or "")
        if narrower.lower() in NO_NARROWER:
            narrower = ""
        found.append({"id": token, "verdict": first_word(verdict), "narrower": narrower})
    return found


# ---------- write

def today() -> str:
    return datetime.date.today().isoformat()


def check_date(value: str) -> str:
    try:
        if not DATE_RE.fullmatch(value):
            raise ValueError(value)
        return datetime.date.fromisoformat(value).isoformat()
    except ValueError:
        raise Unreadable(f"--date {value!r} is not a date in the form YYYY-MM-DD")


def where_of(note: str | None) -> str | None:
    """The note's path as a hint for the reader: relative to the current folder, never a home path."""
    if not note:
        return None
    path = Path(note)
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.name


def plan_stamp(ledger: Ledger, id_: str, verdict: str, text: str, date: str, by: str | None,
               again: str | None, where: str | None) -> dict:
    """The stamp to append, or Refused with the reason."""
    if not ID_RE.fullmatch(id_):
        raise Refused(f"{id_!r} is not an id: use letters, digits, dot, dash or underscore, such as IN-001")
    if verdict not in VERDICTS:
        raise Refused(f"{id_}: the verdict {verdict!r} is not one of {', '.join(VERDICTS)}")
    if not normalise(text):
        raise Refused(f"{id_}: the conclusion has no text")
    stamp, why = ledger.current(id_)
    if why:
        raise Refused(f"{id_}: {why}. Nothing was written")
    if stamp and not again:
        raise Refused(f"{id_} already has a stamp ({stamp['verdict']}, {stamp['date']}). A verdict is written "
                      "once. To record a new challenge, pass --again with the reason")
    if again and not stamp:
        raise Refused(f"{id_} has no stamp yet, so there is nothing to challenge again. Write it without "
                      "--again")
    return make_stamp(id_, verdict, date, text, by=by, again=normalise(again) if again else None, where=where)


def cmd_write(args) -> int:
    ledger = Ledger(Path(args.stamps))
    date = check_date(args.date) if args.date else today()
    where = where_of(args.note)
    notes: list[str] = []
    todo: list[tuple[str, str, str]] = []          # id, verdict, text

    if args.verdicts:
        if not args.note:
            raise Unreadable("--verdicts needs --note: the note holds the sentences that are stamped")
        if args.id or args.verdict or args.text or args.text_file:
            raise Unreadable("--verdicts takes the ids and verdicts from the answer: leave out --id, "
                             "--verdict, --text and --text-file")
        found, twice = conclusions(read_file(args.note))
        answers = answer_verdicts(read_file(args.verdicts))
        if not answers:
            raise Refused(f"{args.verdicts} holds no verdict: each conclusion needs a heading that starts "
                          "with its id and a line `- **Verdict:** kept`, `weakened` or `dropped`")
        problems = []
        seen = set()
        for answer in answers:
            id_ = answer["id"]
            if id_ in seen:
                problems.append(f"{id_}: the answer gives it two verdicts")
                continue
            seen.add(id_)
            if id_ in twice:
                problems.append(f"{id_}: the note has this id under two headings")
            elif id_ not in found:
                problems.append(f"{id_}: the answer gives a verdict, and {args.note} has no conclusion with "
                                "this id")
            elif answer["verdict"] not in VERDICTS:
                problems.append(f"{id_}: the answer's verdict is not one of {', '.join(VERDICTS)}")
            elif answer["verdict"] == "weakened" and answer["narrower"] \
                    and normalise(found[id_]["text"]) != answer["narrower"]:
                problems.append(f"{id_}: weakened, and the note's heading is not the narrower claim the "
                                "challenger gave. Copy that claim into the heading as it stands, then stamp")
            else:
                todo.append((id_, answer["verdict"], found[id_]["text"]))
                if found[id_]["shown"] and found[id_]["shown"] != answer["verdict"]:
                    notes.append(f"NOTE {id_}: the note shows \"{found[id_]['label']}\" and the stamp says "
                                 f"{answer['verdict']}. Change the note's label to match")
        if problems:
            for problem in problems:
                print(f"REFUSED {problem}")
            print("Nothing was written.")
            return 1
    else:
        if not args.id or len(args.id) != 1 or not args.verdict:
            raise Unreadable("write needs one --id and --verdict, or --verdicts with the challenger's answer")
        id_ = args.id[0]
        verdict = args.verdict.lower()
        if args.note:
            if args.text or args.text_file:
                raise Unreadable("give the sentence one way: --note, --text or --text-file")
            found, twice = conclusions(read_file(args.note))
            if id_ in twice:
                raise Refused(f"{id_}: the note has this id under two headings")
            if id_ not in found:
                raise Refused(f"{id_}: {args.note} has no conclusion with this id. A conclusion is a heading "
                              f"with a line `- **Id:** {id_}` under it")
            text = found[id_]["text"]
            if found[id_]["shown"] and found[id_]["shown"] != verdict:
                notes.append(f"NOTE {id_}: the note shows \"{found[id_]['label']}\" and the stamp says "
                             f"{verdict}. Change the note's label to match")
        else:
            text = one_text(args)
        todo.append((id_, verdict, text))

    try:
        stamps = [plan_stamp(ledger, id_, verdict, text, date, args.by, args.again, where)
                  for id_, verdict, text in todo]
    except Refused as refusal:
        print(f"REFUSED {refusal}.")
        if len(todo) > 1:
            print("Nothing was written.")
        return 1
    ledger.append(stamps)
    for stamp in stamps:
        print(f"STAMPED {stamp['id']} {stamp['verdict']} {stamp['date']} {stamp['text_sha256'][:12]}")
    for note in notes:
        print(note)
    print(f"Saved: {ledger.path}")
    return 0


def one_text(args) -> str:
    if bool(args.text) == bool(args.text_file):
        raise Unreadable("give the sentence one way: --note, --text or --text-file")
    return args.text if args.text else read_file(args.text_file)


# ---------- verify

def check(ledger: Ledger, id_: str, text: str | None, shown: str | None,
          label: str | None = None) -> list[tuple[str, str]]:
    """What is wrong with one conclusion, as (status, sentence) pairs; an empty list when it verifies.
    `text` is the sentence as it stands now. `shown` is the first word of the verdict displayed with it, in
    lower case ('' or None when none is displayed), and `label` is that verdict as written, for the message."""
    label = label or shown
    stamp, why = ledger.current(id_)
    if why:
        return [("STAMP ALTERED", why)]
    if stamp is None:
        said = f": \"{label}\" is shown, and no stamp backs it" if shown in VERDICTS else ""
        return [("NO STAMP", f"no challenge is recorded{said}")]
    wrong = []
    if text is not None and text_hash(text) != stamp["text_sha256"]:
        wrong.append(("TEXT CHANGED", f"the sentence is not the one stamped {stamp['verdict']} on "
                                      f"{stamp['date']}. Challenge it again"))
    if shown and shown != stamp["verdict"]:
        wrong.append(("VERDICT RETYPED", f"shown \"{label}\", stamped {stamp['verdict']} on {stamp['date']}"))
    return wrong


def cmd_verify(args) -> int:
    ledger = Ledger(Path(args.stamps))
    targets: list[tuple[str, str | None, str | None, str | None]] = []      # id, text, shown, label
    skipped: list[str] = []
    missing: list[str] = []
    if args.note:
        if args.text or args.text_file or args.verdict:
            raise Unreadable("with --note the sentence and the verdict shown are read from the note")
        found, twice = conclusions(read_file(args.note))
        wanted = args.id or list(found)
        for id_ in wanted:
            if id_ in twice:
                missing.append(f"TWICE {id_}: the note has this id under two headings")
            elif id_ not in found:
                missing.append(f"NOT IN NOTE {id_}: {args.note} has no conclusion with this id")
            elif not args.id and not found[id_]["has_challenge_line"] and not ledger.times(id_) \
                    and not ledger.damaged:
                skipped.append(id_)
            else:
                targets.append((id_, found[id_]["text"], found[id_]["shown"], found[id_]["label"]))
    else:
        if not args.id or len(args.id) != 1:
            raise Unreadable("verify needs --note, or one --id with --text or --text-file")
        shown = first_word(args.verdict) if args.verdict else None
        targets.append((args.id[0], one_text(args), shown, label_head(args.verdict or "") or None))

    bad = len(missing)
    for line in missing:
        print(line)
    for id_, text, shown, label in targets:
        wrong = check(ledger, id_, text, shown, label)
        if wrong:
            bad += 1
            for status, sentence in wrong:
                print(f"{status} {id_}: {sentence}")
        else:
            stamp, _ = ledger.current(id_)
            print(f"OK {id_} {stamp['verdict']} {stamp['date']}")
    for id_ in skipped:
        print(f"SKIPPED {id_}: no Challenge line and no stamp, so it is not read as a conclusion")
    total = len(targets) + len(missing)
    print(f"{total} checked: {total - bad} in order, {bad} not.")
    return 1 if bad else 0


# ---------- list

def cmd_list(args) -> int:
    ledger = Ledger(Path(args.stamps))
    if not ledger.exists:
        print(f"No stamps: {ledger.path} does not exist.")
        return 0
    bad = 0
    for number, why in ledger.damaged:
        print(f"DAMAGED line {number} {why}")
        bad += 1
    for id_ in ledger.entries:
        stamp, why = ledger.current(id_)
        times = ledger.times(id_)
        if stamp is None:
            print(f"STAMP ALTERED {id_}: {why}")
            bad += 1
            continue
        extra = [f"by {stamp['by']}"] if stamp.get("by") else []
        if times > 1:
            extra.append(f"challenged {times} times")
        if stamp.get("again"):
            extra.append(f"again: {stamp['again']}")
        print(f"{id_} {stamp['verdict']} {stamp['date']}" + (f" ({'; '.join(extra)})" if extra else ""))
    return 1 if bad else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    def common(command):
        command.add_argument("--stamps", default=DEFAULT_STAMPS, help=f"the stamp file (default {DEFAULT_STAMPS})")

    write = sub.add_parser("write", help="record a verdict once")
    common(write)
    write.add_argument("--id", action="append")
    write.add_argument("--verdict")
    write.add_argument("--note", help="the note that holds the conclusion: its heading is the sentence")
    write.add_argument("--text")
    write.add_argument("--text-file")
    write.add_argument("--verdicts", help="the challenger's saved answer: ids and verdicts are read from it")
    write.add_argument("--by", choices=("agent", "inline"),
                       help="who challenged: the challenger agent, or the session itself")
    write.add_argument("--again", help="why the conclusion was challenged again; appends a new stamp")
    write.add_argument("--date", help="the day of the challenge, YYYY-MM-DD (default today)")

    verify = sub.add_parser("verify", help="check conclusions against their stamps")
    common(verify)
    verify.add_argument("--id", action="append")
    verify.add_argument("--note")
    verify.add_argument("--text")
    verify.add_argument("--text-file")
    verify.add_argument("--verdict", help="the verdict shown with the conclusion, when it is not in a note")

    listing = sub.add_parser("list", help="the stamp in force for each conclusion")
    common(listing)

    args = parser.parse_args(argv)
    try:
        return {"write": cmd_write, "verify": cmd_verify, "list": cmd_list}[args.command](args)
    except Refused as refusal:
        print(f"REFUSED {refusal}.")
        return 1
    except Unreadable as problem:
        print(f"challenge_stamp.py: {problem}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
