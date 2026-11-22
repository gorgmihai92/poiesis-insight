"""Build the eval case that puts the six conclusions of the lab's recorded trend scan to the `challenger` agent.

  python3 -I tests/eval_data.py [NOTEBOOK]      writes challenger-trend-scan/prompt.md from the notebook's fixtures

The conclusions and every number in the prompt are copied from the Poiesis Lab notebook's `fixtures/` by this
script, so nothing is retyped. `tests/test_evals.py` checks that the prompt in the repository is what this script
writes. NOTEBOOK defaults to the folder `POIESIS_LAB` names, then `~/Poiesis Lab`. The other challenger case with
conclusions and data, `challenger-synthetic-map`, is written by `synthetic_map.py` from made-up data.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "plugins" / "poiesis-insight" / "evals"
YEARS = [str(year) for year in range(2010, 2026)]

FRONT = """---
description: {description}
tags: [challenger, recorded-run]
runs: 1
max_turns: 20
timeout_seconds: 1500
allowed_tools: [Read, Glob, Grep, Skill, Agent]
---

"""
ASK = ("Run the `challenger` agent of poiesis-insight on the {n} conclusions below, with the data under them. "
       "Give it the conclusions and the data and nothing else: not what I expect, and no reasoning. Then give me "
       "its answer exactly as it came, one block per conclusion, with nothing added before the first block.\n\n")


def table(head: list[str], rows: list[list]) -> str:
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    lines += ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows]
    return "\n".join(lines) + "\n"


def conclusions(fixtures: Path, run: str) -> list[dict]:
    verdicts = json.loads((fixtures / "challenge-verdicts.json").read_text(encoding="utf-8"))
    return next(entry for entry in verdicts["runs"] if entry["run"] == run)["conclusions"]


def conclusion_lines(items: list[dict]) -> str:
    return "## Conclusions\n\n" + "".join(f"- **{item['id']}:** {item['claim']}\n" for item in items) + "\n"


def trend_scan(fixtures: Path) -> str:
    folder = fixtures / "trend-scan"
    series = json.loads((folder / "series.json").read_text(encoding="utf-8"))["rows"]
    corpus = json.loads((folder / "corpus.json").read_text(encoding="utf-8"))["rows"]
    analysis = json.loads((folder / "analysis.json").read_text(encoding="utf-8"))
    openalex = json.loads((folder / "openalex.json").read_text(encoding="utf-8"))
    areas = list(analysis)
    names = {row["area_id"]: row["area"] for row in series}
    by = {(row["area_id"], str(row["year"])): row for row in series}

    out = FRONT.format(description="The six first-pass conclusions of the lab's trend scan, put to the challenger "
                                   "agent with the run's numbers. Recorded verdicts: all six weakened.")
    out += ASK.format(n="six") + conclusion_lines(conclusions(fixtures, "trend-scan"))
    out += ("## Data\n\nOpenAlex, fetched " + openalex["fetched"] + ". Five areas, each a fixed set of search terms "
            "in titles and abstracts. 2026 is left out: the year was not over.\n\n")
    out += ("### The whole database, by year\n\nWorks of every type, and articles, reviews and preprints only, with "
            "each one's growth on the year before.\n\n")
    out += table(["year", "all works", "growth %", "articles, reviews, preprints", "growth %"],
                 [[row["year"], row["all_works"], row["all_growth_pct"], row["articles"], row["articles_growth_pct"]]
                  for row in corpus if 2018 <= row["year"] <= 2025])
    out += ("\n### Share of each area, per 100,000 works\n\n`all`: works of every type that match the area's terms, "
            "over all works. `art`: articles, reviews and preprints that match, over articles, reviews and "
            "preprints. The six conclusions were written from `all`.\n\n")
    out += table(["year"] + [f"{names[area]} {kind}" for area in areas for kind in ("all", "art")],
                 [[year] + [by[(area, year)][key] for area in areas for key in ("share_all", "share")]
                  for year in YEARS])
    out += ("\n### Growth of each area, four ways of counting\n\nGrowth is the natural log of a year over the year "
            "before. `mean` and `SD` are over 2013 to 2022. `z` is (growth - mean) / SD. `CAGR` is the yearly rate "
            "over five years. The four rows of an area: its share of all works; its share of articles, reviews and "
            "preprints; the same with the area's narrow terms only; and the raw count of articles, reviews and "
            "preprints.\n\n")
    kinds = (("ta", "share of all works"), ("t", "share of articles etc."), ("tn", "same, narrow terms"),
             ("tr", "raw count"))
    rows = []
    for area in areas:
        for key, label in kinds:
            test = analysis[area][key]
            rows.append([names[area], label, f"{test['m']:.3f}", f"{test['sd']:.3f}"]
                        + [f"{test['g'][year]:.3f}" for year in ("2023", "2024", "2025")]
                        + [f"{test['z'][year]:.1f}" for year in ("2023", "2024", "2025")]
                        + [f"{test['c1'] * 100:.1f}%", f"{test['c2'] * 100:.1f}%"])
    out += table(["area", "counted as", "mean", "SD", "growth 2023", "growth 2024", "growth 2025", "z 2023",
                  "z 2024", "z 2025", "CAGR 2015-20", "CAGR 2020-25"], rows)
    return out


def write(fixtures: Path) -> None:
    for name, build in (("challenger-trend-scan", trend_scan),):
        (EVALS / name).mkdir(parents=True, exist_ok=True)
        (EVALS / name / "prompt.md").write_text(build(fixtures), encoding="utf-8")
        print(f"wrote {name}/prompt.md")


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import helpers

    lab = Path(sys.argv[1]) / "fixtures" if len(sys.argv) > 1 else helpers.lab()
    if lab is None:
        sys.exit("the Poiesis Lab notebook was not found: pass its folder")
    write(lab)
