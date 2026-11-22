"""Build the two eval cases that put the lab's 16 recorded conclusions to the `challenger` agent.

  python3 -I tests/eval_data.py [NOTEBOOK]      writes both prompt.md files from the notebook's fixtures

The conclusions and every number in the prompts are copied from the Poiesis Lab notebook's `fixtures/` by this
script, so nothing is retyped. `tests/test_evals.py` checks that the prompts in the repository are what this
script writes. NOTEBOOK defaults to the folder `POIESIS_LAB` names, then `~/Poiesis Lab`.
"""
from __future__ import annotations

import json
import re
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


def responsibility_map(fixtures: Path) -> str:
    folder = fixtures / "responsibility-map"
    analysis = json.loads((folder / "analysis.json").read_text(encoding="utf-8"))
    epmc = json.loads((folder / "epmc.json").read_text(encoding="utf-8"))
    page = json.loads((folder / "page_data.json").read_text(encoding="utf-8"))
    html = (folder / "page.html").read_text(encoding="utf-8")

    out = FRONT.format(description="The ten first-pass conclusions of the lab's responsibility map, put to the "
                                   "challenger agent with the run's numbers. Recorded verdicts: 1 kept, 6 "
                                   "weakened, 2 dropped, 1 split.")
    out += ASK.format(n="ten") + conclusion_lines(conclusions(fixtures, "responsibility-map"))
    out += "## Data\n\n### The studies behind I1 to I5\n\nAs the run recorded them. \"na\": the study did not rate that party.\n\n"
    start = html.index("const STUDIES")
    block = html[start: html.index("];", start)]
    studies = []
    for entry in re.findall(r"\{id:.*?\}(?=,\s*\{id:|\s*$)", block, re.S):
        def text(key: str) -> str:
            found = re.search(key + r':\s*"([^"]*)"', entry)
            return found.group(1) if found else ""

        def party(key: str) -> str:
            found = re.search(key + r":\s*\[([^\]]*)\]", entry)
            return ": ".join(re.findall(r'"([^"]*)"', found.group(1))) if found else ""
        studies.append([text("cite"), text("venue"), text("what"), party("human"), party("ai"), party("dev")])
    out += table(["study", "venue and sample, where recorded", "what it was about", "blame on the human",
                  "blame on the AI", "blame on developers or designers"], studies)

    out += ("\n### Sixteen topics of moral research, for T1 to T5\n\n" + epmc["source"] + ", fetched "
            + epmc["fetched"] + ". The universe is every work matching " + epmc["base"] + ". The sixteen topics "
            "were fixed before counting. `share` is a topic's works as a percentage of the universe that year. "
            "`impact` is the topic's share of 2019 to 2021 works cited 50 times or more, over the universe's.\n\n")
    out += table(["topic", "share 2015 %", "share 2020 %", "share 2025 %", "CAGR 2015-20", "CAGR 2020-25",
                  "works 2025", "works 2019-21", "of them cited 50+", "impact"],
                 [[row["topic"], f"{row['share_2015']:.2f}", f"{row['share_2020']:.2f}", f"{row['share_2025']:.2f}",
                   f"{row['cagr_prev'] * 100:.1f}%", f"{row['cagr'] * 100:.1f}%", row["n_2025"], row["n_1921"],
                   row["cited_1921"], f"{row['impact']:.2f}"] for row in analysis["rows"]])
    out += (f"\nIn the universe, {epmc['uni_cited']} of {epmc['uni_1921']} works of 2019 to 2021 were cited 50 "
            f"times or more ({analysis['uni_cited_rate'] * 100:.2f}%). Median CAGR 2020-25 of the sixteen: "
            f"{analysis['median_momentum'] * 100:.1f}%. Median share in 2025: {analysis['median_size']:.2f}%.\n")
    named = ["ai", "progress", "climate", "found", "emotion", "circle", "politics"]
    topic = {row["id"]: row["topic"] for row in analysis["rows"]}
    out += "\n### Works per year\n\nThe universe, the seven topics the conclusions name, and three crossings.\n\n"
    cross = page["cross"]
    out += table(["year", "universe"] + [topic[key] for key in named] + [item["name"] for item in cross],
                 [[year, epmc["universe"][year]] + [epmc["series"][key][year] for key in named]
                  + [item["counts"][index] for item in cross] for index, year in enumerate(YEARS)])
    return out


def write(fixtures: Path) -> None:
    for name, build in (("challenger-trend-scan", trend_scan), ("challenger-responsibility-map", responsibility_map)):
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
