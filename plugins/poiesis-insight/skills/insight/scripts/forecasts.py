#!/usr/bin/env python3
"""Score a forecast log (Markdown table) with the Brier score. Run with `python3 -I`.

  forecasts.py foresight/forecasts.md

Columns: id | question | probability | made | resolve by | outcome | reasoning. Outcome is 1, 0 or empty.
Brier score = mean of (probability - outcome)^2 over resolved forecasts: 0 is perfect, 0.25 is what always
saying 50% earns, lower is better. Also lists forecasts past their date with no outcome yet.
"""
import argparse
import datetime as dt
import sys
from pathlib import Path


def rows(path: Path) -> list[list[str]]:
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or set(line) <= {"|", "-", " "}:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells and cells[0].lower() != "id" and not cells[0].startswith("<"):
            out.append(cells)
    return out


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("log", type=Path)
    a = p.parse_args()
    today = dt.date.today().isoformat()
    scored, due, bad = [], [], []
    for r in rows(a.log):
        if len(r) < 6:
            bad.append(r[0])
            continue
        fid, question, prob, _made, resolve, outcome = r[:6]
        try:
            pr = float(prob)
        except ValueError:
            bad.append(fid)
            continue
        if outcome in ("0", "1"):
            scored.append((fid, pr, int(outcome)))
        elif resolve and resolve <= today:
            due.append(f"{fid} ({resolve}): {question}")
    if scored:
        brier = sum((pr - o) ** 2 for _, pr, o in scored) / len(scored)
        print(f"Brier score: {brier:.3f} over {len(scored)} resolved forecasts (0 = perfect, 0.25 = always 50%)")
        for fid, pr, o in scored:
            print(f"  {fid}: said {pr:.0%}, outcome {o} → {(pr - o) ** 2:.3f}")
    else:
        print("No resolved forecasts yet.")
    if due:
        print("\nPast their date, outcome missing:")
        for d in due:
            print("  " + d)
    if bad:
        print("\nRows not understood: " + ", ".join(bad))
    return 0


if __name__ == "__main__":
    sys.exit(main())
