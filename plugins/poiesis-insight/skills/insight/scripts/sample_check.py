#!/usr/bin/env python3
"""Pick claims at random from a report for a person to check against their sources, and say what the checks
so far allow. Run with `python3 -I`.

  sample_check.py pick insights/<report>.md [--n 5] [--seed N] [--log insights/human-checks.md]
  sample_check.py score [--log insights/human-checks.md]
  sample_check.py bound --checked 30 --wrong 0

`pick` lists the report's lines that point to a source: a page `(p. 4)`, a citation `[@key]`, a link to a note,
a `[[note]]` link, a DOI or a web address. It draws --n of them at random and adds one row for each to the log.
The draw is the script's, not the writer's, so the easy claims are not the ones chosen. The seed is printed:
the same report and seed give the same draw.

The person opens each source and fills the row's `result` cell with `ok` or `wrong`, and a few words under
`what was seen`. A row with an empty result has not been checked.

`score` counts the rows and prints the largest error rate the checks cannot rule out: with `wrong` errors in
`checked` claims, the true share of wrong claims is below the bound with 95% confidence (the exact one-sided
binomial bound). `bound` prints it for any two numbers.

  5 checked, 0 wrong: up to 45.1% of claims could be wrong
  30 checked, 0 wrong: up to 9.5%

Five clean checks on one report say little. The checks are judged on their total, across reports.

The log is a Markdown table; a cell cannot hold `|`, so one in a claim is written as `/`.
Exit codes: 0 done; 1 the report has no line that points to a source, or the log cannot be read; 2 a wrong
command line.
"""
from __future__ import annotations

import argparse
import datetime
import math
import random
import re
import secrets
import sys
from pathlib import Path

DEFAULT_LOG = "insights/human-checks.md"
HEADER = ("# Human checks\n\n"
          "Claims drawn at random by `sample_check.py`, for a person to check against the source. Fill `result` "
          "with `ok` or `wrong`.\n\n"
          "| date | report | line | claim | result | what was seen |\n"
          "|---|---|---|---|---|---|\n")
POINTS_TO_A_SOURCE = re.compile(
    r"\(pp?\.\s*\d+[^)]*\)|\[@[^\]]+\]|\]\([^)\s]+\.md[^)]*\)|\[\[[^\]]+\]\]|\b10\.\d{4,9}/\S+|https?://\S+", re.I)
SKIPPED_LINE = re.compile(r"^\s*(\||#|```|~~~|[-*+]\s+\*\*(Id|From|Written|Challenge):?\*\*)", re.I)
FENCE = re.compile(r"^\s*(```|~~~)")


def claims_of(report: str) -> list[tuple[int, str]]:
    """(line number, the line) for each line of a report that points to a source."""
    found = []
    fenced = False
    for number, line in enumerate(report.splitlines(), 1):
        if FENCE.match(line):
            fenced = not fenced
            continue
        if fenced or SKIPPED_LINE.match(line) or not POINTS_TO_A_SOURCE.search(line):
            continue
        found.append((number, re.sub(r"\s+", " ", line).strip()))
    return found


def upper_bound(checked: int, wrong: int, confidence: float = 0.95) -> float:
    """The largest share of wrong claims that `wrong` errors in `checked` claims do not rule out: the exact
    one-sided binomial (Clopper-Pearson) upper bound. With no error it is 1 - (1 - confidence) ** (1 / checked)."""
    if checked <= 0 or wrong < 0 or wrong > checked:
        raise ValueError("checked has to be at least 1, and wrong between 0 and checked")
    if wrong == checked:
        return 1.0
    alpha = 1 - confidence

    def at_most_wrong(share: float) -> float:
        return sum(math.comb(checked, k) * share ** k * (1 - share) ** (checked - k) for k in range(wrong + 1))

    low, high = 0.0, 1.0
    for _ in range(60):                       # bisection: at_most_wrong falls as the share rises
        middle = (low + high) / 2
        if at_most_wrong(middle) > alpha:
            low = middle
        else:
            high = middle
    return high


def bound_sentence(checked: int, wrong: int) -> str:
    share = upper_bound(checked, wrong) * 100
    return (f"{checked} checked, {wrong} wrong: up to {share:.1f}% of claims could be wrong "
            "(95% bound, exact binomial).")


def cell(text: str) -> str:
    return text.replace("|", "/").strip()


def read_rows(log: Path) -> list[list[str]]:
    rows = []
    for line in log.read_text(encoding="utf-8-sig").splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(cells) < 5 or cells[0] in ("date", "") or set(cells[0]) <= set("-: "):
            continue
        rows.append(cells)
    return rows


def cmd_pick(args) -> int:
    report = Path(args.report)
    try:
        claims = claims_of(report.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError) as err:
        print(f"sample_check.py: cannot read {report}: {err}", file=sys.stderr)
        return 2
    if not claims:
        print(f"No line of {report} points to a source (a page, a citation, a link to a note, a DOI or an "
              "address), so there is nothing to draw from.")
        return 1
    seed = args.seed if args.seed is not None else secrets.randbelow(10 ** 9)
    drawn = sorted(random.Random(seed).sample(claims, min(args.n, len(claims))))
    today = args.date or datetime.date.today().isoformat()
    log = Path(args.log)
    log.parent.mkdir(parents=True, exist_ok=True)
    new = not log.exists()
    with log.open("a", encoding="utf-8", newline="\n") as handle:
        if new:
            handle.write(HEADER)
        for number, line in drawn:
            handle.write(f"| {today} | {cell(report.as_posix())} | {number} | {cell(line)} |  |  |\n")
    print(f"{len(drawn)} of the {len(claims)} lines that point to a source, drawn with seed {seed}:")
    for number, line in drawn:
        print(f"  line {number}: {line}")
    if len(claims) < args.n:
        print(f"The report has only {len(claims)} such lines, fewer than the {args.n} asked for.")
    print(f"Added to {log}. A person opens each source and fills `result` with ok or wrong.")
    return 0


def cmd_score(args) -> int:
    log = Path(args.log)
    if not log.is_file():
        print(f"No checks yet: {log} does not exist.")
        return 0
    try:
        rows = read_rows(log)
    except (OSError, UnicodeDecodeError) as err:
        print(f"sample_check.py: cannot read {log}: {err}", file=sys.stderr)
        return 1
    results = [row[4].lower() for row in rows]
    ok, wrong = results.count("ok"), results.count("wrong")
    waiting = sum(1 for result in results if not result)
    other = len(results) - ok - wrong - waiting
    print(f"{len(rows)} rows: {ok} ok, {wrong} wrong, {waiting} not checked yet"
          + (f", {other} with a result that is neither ok nor wrong" if other else "") + ".")
    if ok + wrong:
        print(bound_sentence(ok + wrong, wrong))
    else:
        print("Nothing has been checked, so nothing can be said about the error rate.")
    return 0


def cmd_bound(args) -> int:
    try:
        print(bound_sentence(args.checked, args.wrong))
    except ValueError as err:
        print(f"sample_check.py: {err}", file=sys.stderr)
        return 2
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    pick = sub.add_parser("pick", help="draw claims from a report and add them to the log")
    pick.add_argument("report")
    pick.add_argument("--n", type=int, default=5)
    pick.add_argument("--seed", type=int)
    pick.add_argument("--date", help="the day written in the log (default today)")
    pick.add_argument("--log", default=DEFAULT_LOG)
    score = sub.add_parser("score", help="count the checks and print the bound")
    score.add_argument("--log", default=DEFAULT_LOG)
    bound = sub.add_parser("bound", help="the bound for two numbers")
    bound.add_argument("--checked", type=int, required=True)
    bound.add_argument("--wrong", type=int, required=True)
    args = parser.parse_args(argv)
    if args.command == "pick" and args.n < 1:
        parser.error("--n has to be at least 1")
    return {"pick": cmd_pick, "score": cmd_score, "bound": cmd_bound}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
