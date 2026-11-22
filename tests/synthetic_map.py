"""Build the synthetic eval case `challenger-synthetic-map`: nine conclusions on a neutral subject (coastal flood
defence) and the data they are judged on.

  python3 -I tests/synthetic_map.py      writes challenger-synthetic-map/prompt.md

Synthetic, for the test. Every study and count below was made up for this case on 2026-11-26: the yearly counts
by a seeded draw around share paths chosen by hand, the rest by hand. They describe no real study and no real
database, and nothing here comes from the Poiesis Lab notebook or from a recorded run. Every derived number in the
prompt (shares, growth, impact, medians) is computed here from the raw counts, so none is typed twice.
`tests/test_evals.py` checks that the prompt in the repository is what this script writes, and that these data
decide the verdicts the graders expect (`EXPECTED`, `facts`).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASE = ROOT / "plugins" / "poiesis-insight" / "evals" / "challenger-synthetic-map"

# The verdicts these data are built to give, one per conclusion. The graders accept these and, where the data
# leave room, a neighbour (`graders/*.md`).
EXPECTED = {"I1": "weakened", "I2": "dropped", "I3": "weakened", "I4": "dropped", "T1": "kept",
            "T2": "weakened", "T3": "weakened", "T4": "dropped", "T5": "dropped"}

FRONT = """---
description: "Synthetic, for the test: nine conclusions on a neutral subject (coastal flood defence), put to the challenger agent. The studies and counts are made up by tests/synthetic_map.py and stand for nothing real; the graders expect the verdicts these data decide, which the tests check."
tags: [challenger, synthetic]
runs: 1
max_turns: 20
timeout_seconds: 1500
allowed_tools: [Read, Glob, Grep, Skill, Agent]
---

"""
ASK = ("Run the `challenger` agent of poiesis-insight on the nine conclusions below, with the data under them. "
       "Give it the conclusions and the data and nothing else: not what I expect, and no reasoning. Then give me "
       "its answer exactly as it came, one block per conclusion, with nothing added before the first block.\n\n")

# The studies: label, year, design and sample, where, and what each measured. "na": not measured.
STUDY_HEAD = ["study", "year", "design and sample", "where", "wave height behind a salt marsh",
              "behind a dune", "behind a seawall", "costs reported", "flood-insurance claims"]
STUDIES = [
    ["Study 1", 2016, "field · 12 storms", "one estuary", "lower by 30%", "na", "na", "none", "na"],
    ["Study 2", 2017, "wave flume · 40 runs", "laboratory", "lower by 45%", "na", "na", "none", "na"],
    ["Study 3", 2018, "field · one storm surge", "the estuary of study 1", "no change", "na", "lower by 20%",
     "building only", "na"],
    ["Study 4", 2019, "model · 3 coastlines", "three open coasts", "lower by 20%", "lower by 35%", "lower by 50%",
     "building only", "na"],
    ["Study 5", 2020, "field · 8 sites", "one open coast", "na", "lower by 40%", "lower by 25%", "none", "na"],
    ["Study 6", 2021, "field · 5 sites", "a second estuary", "lower by 25%", "na", "na", "none", "na"],
    ["Study 7", 2022, "wave flume · 24 runs", "laboratory", "na", "lower by 30%", "na", "building only", "na"],
    ["Study 8", 2023, "model · one bay", "one bay", "lower by 15%", "na", "na", "none", "na"],
    ["Study 9", 2025, "preprint · not read", "one estuary", "na", "na", "na", "none", "fewer after restoring"],
]

YEARS = list(range(2012, 2026))
UNIVERSE = [1480, 1565, 1702, 1838, 1971, 2154, 2290, 2533, 2716, 2948, 3197, 3342, 3618, 3951]
# Works per year, 2012 to 2025, of each of the twelve topics, and how many of its works of 2018 to 2020 were cited
# 40 times or more.
TOPICS = {
    "Nature-based defences": ([9, 11, 13, 17, 22, 30, 39, 53, 71, 89, 111, 135, 169, 213], 14),
    "Seawalls": ([110, 115, 123, 132, 134, 150, 156, 169, 172, 181, 184, 185, 187, 196], 21),
    "Living shorelines": ([20, 23, 25, 29, 33, 36, 41, 46, 51, 60, 73, 87, 103, 122], 8),
    "Storm-surge forecasting": ([45, 48, 50, 56, 63, 66, 72, 85, 87, 98, 103, 109, 119, 247], 13),
    "Groundwater salinisation": ([7, 7, 8, 9, 10, 11, 12, 13, 15, 16, 18, 19, 20, 23], 3),
    "Managed retreat": ([12, 14, 16, 18, 21, 26, 31, 40, 46, 56, 67, 78, 96, 122], 9),
    "Dune management": ([63, 68, 74, 83, 88, 94, 103, 113, 125, 133, 147, 164, 179, 198], 15),
    "Salt marshes": ([32, 36, 42, 46, 53, 56, 62, 75, 80, 93, 103, 112, 122, 147], 12),
    "Flood insurance": ([28, 30, 32, 36, 41, 46, 49, 61, 67, 73, 79, 80, 91, 97], 6),
    "Sediment transport": ([132, 139, 147, 160, 174, 183, 192, 204, 222, 227, 252, 250, 278, 300], 30),
    "Erosion monitoring": ([82, 90, 97, 106, 119, 128, 138, 157, 180, 192, 217, 221, 244, 272], 27),
    "Port infrastructure": ([41, 43, 48, 50, 53, 58, 61, 63, 70, 75, 77, 81, 86, 90], 7),
}
UNIVERSE_CITED = 377            # of the universe's works of 2018 to 2020, cited 40 times or more
NAMED = ["Nature-based defences", "Living shorelines", "Storm-surge forecasting", "Seawalls",
         "Groundwater salinisation", "Managed retreat"]
RULE = 1.2                      # the neglected rule, fixed before counting: impact at least 1.2 x the universe's


def count(topic: str, year: int) -> int:
    return TOPICS[topic][0][YEARS.index(year)]


def share(topic: str, year: int) -> float:
    """A topic's works as a percentage of the universe that year."""
    return 100 * count(topic, year) / UNIVERSE[YEARS.index(year)]


def growth(topic: str, start: int, end: int) -> float:
    """The yearly compound growth of the share from start to end, as a percentage."""
    return 100 * ((share(topic, end) / share(topic, start)) ** (1 / (end - start)) - 1)


def window(topic: str) -> int:
    return sum(count(topic, year) for year in (2018, 2019, 2020))


def universe_window() -> int:
    return sum(UNIVERSE[YEARS.index(year)] for year in (2018, 2019, 2020))


def impact(topic: str, cited: int | None = None) -> float:
    """The topic's share of 2018-20 works cited 40+ over the universe's; `cited` replaces the topic's count."""
    cited = TOPICS[topic][1] if cited is None else cited
    return (cited / window(topic)) / (UNIVERSE_CITED / universe_window())


def median(values: list[float]) -> float:
    ordered = sorted(values)
    middle = len(ordered) // 2
    return ordered[middle] if len(ordered) % 2 else (ordered[middle - 1] + ordered[middle]) / 2


def median_growth() -> float:
    return median([round(growth(topic, 2020, 2025), 1) for topic in TOPICS])


def median_share() -> float:
    return median([round(share(topic, 2025), 2) for topic in TOPICS])


def neglected(topic: str) -> bool:
    """The rule of T4, as stated in the conclusion: impact, then momentum and size below the median."""
    return (round(impact(topic), 2) >= RULE and round(growth(topic, 2020, 2025), 1) < median_growth()
            and round(share(topic, 2025), 2) < median_share())


def table(head: list[str], rows: list[list]) -> str:
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    lines += ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows]
    return "\n".join(lines) + "\n"


def conclusions() -> list[tuple[str, str]]:
    topic = "Groundwater salinisation"
    return [
        ("I1", "Salt marshes lower wave height in every study that measured them."),
        ("I2", "Dunes protect a coast better than seawalls do."),
        ("I3", "No one has studied what it costs to maintain a dune."),
        ("I4", "Restoring a salt marsh also lowers flood-insurance claims in the area it protects."),
        ("T1", "Nature-based defences grew faster than any other of the twelve topics, in 2015–20 and again in "
               "2020–25."),
        ("T2", "Living shorelines and storm-surge forecasting are both accelerating: each one's share grew faster "
               "a year in 2020–25 than in 2015–20."),
        ("T3", "Research on seawalls is in decline."),
        ("T4", f"{topic} is a neglected topic by the rule set before counting: impact at least {RULE} times the "
               f"universe's, share growth in 2020–25 and share in 2025 both below the median of the twelve. Its "
               f"impact is {impact(topic):.2f}, from {TOPICS[topic][1]} of its {window(topic)} works of 2018–20 "
               f"cited 40 times or more."),
        ("T5", "Managed retreat has overtaken seawalls as a subject of research."),
    ]


def prompt() -> str:
    out = FRONT + ASK + "## Conclusions\n\n"
    out += "".join(f"- **{id_}:** {claim}\n" for id_, claim in conclusions()) + "\n"
    out += ("## Data\n\nThe studies and the counts below are synthetic, made for this test: they describe no real "
            "study and no real database.\n\n")
    out += ("### Nine studies, for I1 to I4\n\nAs the notes recorded them. Wave height: how much lower it was "
            "behind the defence than in front of it. \"na\": the study did not measure it.\n\n")
    out += table(STUDY_HEAD, STUDIES)
    out += ("\n### Twelve topics of coastal flood research, for T1 to T5\n\nThe universe is every work on coastal "
            "flooding in one database. The twelve topics were fixed before counting. `share` is a topic's works as "
            "a percentage of the universe that year. `growth` is the yearly compound growth of the share over the "
            "period. `impact` is the topic's share of its 2018 to 2020 works cited 40 times or more, over the "
            "universe's.\n\n")
    out += table(["topic", "share 2015 %", "share 2020 %", "share 2025 %", "growth 2015-20", "growth 2020-25",
                  "works 2025", "works 2018-20", "of them cited 40+", "impact"],
                 [[topic, f"{share(topic, 2015):.2f}", f"{share(topic, 2020):.2f}", f"{share(topic, 2025):.2f}",
                   f"{growth(topic, 2015, 2020):.1f}%", f"{growth(topic, 2020, 2025):.1f}%", count(topic, 2025),
                   window(topic), TOPICS[topic][1], f"{impact(topic):.2f}"] for topic in TOPICS])
    out += (f"\nIn the universe, {UNIVERSE_CITED} of {universe_window()} works of 2018 to 2020 were cited 40 times "
            f"or more ({100 * UNIVERSE_CITED / universe_window():.2f}%). Median growth 2020-25 of the twelve: "
            f"{median_growth():.2f}%. Median share in 2025: {median_share():.2f}%.\n\n")
    out += "### Works per year\n\nThe universe and the six topics the conclusions name.\n\n"
    out += table(["year", "universe"] + NAMED,
                 [[year, UNIVERSE[i]] + [TOPICS[topic][0][i] for topic in NAMED] for i, year in enumerate(YEARS)])
    return out


def facts() -> dict[str, bool]:
    """What the data say about each conclusion, as the tests read it: each must be True for the expected verdicts
    to follow from the data."""
    studies = [dict(zip(STUDY_HEAD, row)) for row in STUDIES]
    marsh = [row["wave height behind a salt marsh"] for row in studies]
    marsh = [cell for cell in marsh if cell != "na"]
    both = [row for row in studies if row["behind a dune"] != "na" and row["behind a seawall"] != "na"]

    def pct(cell: str) -> int:
        return int(cell.split()[-1].rstrip("%"))

    insurance = [row for row in studies if row["flood-insurance claims"] != "na"]
    others = [topic for topic in TOPICS if topic != "Nature-based defences"]
    nature = [share("Nature-based defences", year) for year in YEARS]
    gw = "Groundwater salinisation"
    expected_cited = window(gw) * UNIVERSE_CITED / universe_window()
    return {
        # I1: one study of six that measured marshes found no change, so "every study" does not hold; most agree.
        "I1 one exception among the marsh studies": marsh.count("no change") == 1 and len(marsh) >= 5,
        # I2: the two studies that measured both disagree; the others measured one defence only.
        "I2 the two direct comparisons disagree": len(both) == 2 and (
            (pct(both[0]["behind a dune"]) > pct(both[0]["behind a seawall"]))
            != (pct(both[1]["behind a dune"]) > pct(both[1]["behind a seawall"]))),
        # I3: no study reports maintenance costs, so the absence is "none found among the nine", no more.
        "I3 no maintenance cost in the nine": not any("maint" in row["costs reported"] for row in studies),
        # I4: one study, a preprint not read, is the only item.
        "I4 rests on one unread item": len(insurance) == 1 and "not read" in insurance[0]["design and sample"],
        # T1: fastest in both windows, and the share rises every year (no single year carries it).
        "T1 fastest in both windows": all(growth("Nature-based defences", a, b) > growth(topic, a, b)
                                          for topic in others for a, b in ((2015, 2020), (2020, 2025))),
        "T1 share rises every year": all(later > earlier for earlier, later in zip(nature, nature[1:])),
        # T2: living shorelines accelerates even without 2025; forecasting's acceleration is 2025 alone.
        "T2 shorelines accelerate without 2025": growth("Living shorelines", 2020, 2024)
                                                  > growth("Living shorelines", 2015, 2020),
        "T2 forecasting accelerates only with 2025": (
            growth("Storm-surge forecasting", 2020, 2025) > growth("Storm-surge forecasting", 2015, 2020)
            >= growth("Storm-surge forecasting", 2020, 2024)
            and count("Storm-surge forecasting", 2025) >= 2 * count("Storm-surge forecasting", 2024)),
        # T3: the share falls while the count rises: "decline" holds for one of the two readings only.
        "T3 share falls, count rises": share("Seawalls", 2025) < share("Seawalls", 2020)
                                       and count("Seawalls", 2025) > count("Seawalls", 2020),
        # T4: the rule holds, but on about two works expected, and one fewer cited work fails it.
        "T4 meets the rule": neglected(gw),
        "T4 one fewer fails": round(impact(gw, TOPICS[gw][1] - 1), 2) < RULE,
        "T4 few expected": expected_cited < 3 and TOPICS[gw][1] - expected_cited < 1.5,
        # T5: managed retreat grows faster than seawalls but has fewer works in every year.
        "T5 fewer works every year": all(count("Managed retreat", year) < count("Seawalls", year) for year in YEARS),
        "T5 faster growth": growth("Managed retreat", 2020, 2025) > growth("Seawalls", 2020, 2025),
        "every topic within the universe": all(sum(TOPICS[t][0][i] for t in TOPICS) <= UNIVERSE[i]
                                               for i in range(len(YEARS))),
    }


if __name__ == "__main__":
    failed = [name for name, holds in facts().items() if not holds]
    if failed:
        sys.exit("the data do not decide the expected verdicts: " + "; ".join(failed))
    CASE.mkdir(parents=True, exist_ok=True)
    (CASE / "prompt.md").write_text(prompt(), encoding="utf-8")
    print("wrote challenger-synthetic-map/prompt.md")
