---
description: "Synthetic, for the test: nine conclusions on a neutral subject (coastal flood defence), put to the challenger agent. The studies and counts are made up by tests/synthetic_map.py and stand for nothing real; the graders expect the verdicts these data decide, which the tests check."
tags: [challenger, synthetic]
runs: 1
max_turns: 20
timeout_seconds: 1500
allowed_tools: [Read, Glob, Grep, Skill, Agent]
---

Run the `challenger` agent of poiesis-insight on the nine conclusions below, with the data under them. Give it the conclusions and the data and nothing else: not what I expect, and no reasoning. Then give me its answer exactly as it came, one block per conclusion, with nothing added before the first block.

## Conclusions

- **I1:** Salt marshes lower wave height in every study that measured them.
- **I2:** Dunes protect a coast better than seawalls do.
- **I3:** No one has studied what it costs to maintain a dune.
- **I4:** Restoring a salt marsh also lowers flood-insurance claims in the area it protects.
- **T1:** Nature-based defences grew faster than any other of the twelve topics, in 2015–20 and again in 2020–25.
- **T2:** Living shorelines and storm-surge forecasting are both accelerating: each one's share grew faster a year in 2020–25 than in 2015–20.
- **T3:** Research on seawalls is in decline.
- **T4:** Groundwater salinisation is a neglected topic by the rule set before counting: impact at least 1.2 times the universe's, share growth in 2020–25 and share in 2025 both below the median of the twelve. Its impact is 1.50, from 3 of its 40 works of 2018–20 cited 40 times or more.
- **T5:** Managed retreat has overtaken seawalls as a subject of research.

## Data

The studies and the counts below are synthetic, made for this test: they describe no real study and no real database.

### Nine studies, for I1 to I4

As the notes recorded them. Wave height: how much lower it was behind the defence than in front of it. "na": the study did not measure it.

| study | year | design and sample | where | wave height behind a salt marsh | behind a dune | behind a seawall | costs reported | flood-insurance claims |
|---|---|---|---|---|---|---|---|---|
| Study 1 | 2016 | field · 12 storms | one estuary | lower by 30% | na | na | none | na |
| Study 2 | 2017 | wave flume · 40 runs | laboratory | lower by 45% | na | na | none | na |
| Study 3 | 2018 | field · one storm surge | the estuary of study 1 | no change | na | lower by 20% | building only | na |
| Study 4 | 2019 | model · 3 coastlines | three open coasts | lower by 20% | lower by 35% | lower by 50% | building only | na |
| Study 5 | 2020 | field · 8 sites | one open coast | na | lower by 40% | lower by 25% | none | na |
| Study 6 | 2021 | field · 5 sites | a second estuary | lower by 25% | na | na | none | na |
| Study 7 | 2022 | wave flume · 24 runs | laboratory | na | lower by 30% | na | building only | na |
| Study 8 | 2023 | model · one bay | one bay | lower by 15% | na | na | none | na |
| Study 9 | 2025 | preprint · not read | one estuary | na | na | na | none | fewer after restoring |

### Twelve topics of coastal flood research, for T1 to T5

The universe is every work on coastal flooding in one database. The twelve topics were fixed before counting. `share` is a topic's works as a percentage of the universe that year. `growth` is the yearly compound growth of the share over the period. `impact` is the topic's share of its 2018 to 2020 works cited 40 times or more, over the universe's.

| topic | share 2015 % | share 2020 % | share 2025 % | growth 2015-20 | growth 2020-25 | works 2025 | works 2018-20 | of them cited 40+ | impact |
|---|---|---|---|---|---|---|---|---|---|
| Nature-based defences | 0.92 | 2.61 | 5.39 | 23.1% | 15.6% | 213 | 163 | 14 | 1.72 |
| Seawalls | 7.18 | 6.33 | 4.96 | -2.5% | -4.8% | 196 | 497 | 21 | 0.84 |
| Living shorelines | 1.58 | 1.88 | 3.09 | 3.5% | 10.5% | 122 | 138 | 8 | 1.16 |
| Storm-surge forecasting | 3.05 | 3.20 | 6.25 | 1.0% | 14.3% | 247 | 244 | 13 | 1.07 |
| Groundwater salinisation | 0.49 | 0.55 | 0.58 | 2.4% | 1.1% | 23 | 40 | 3 | 1.50 |
| Managed retreat | 0.98 | 1.69 | 3.09 | 11.6% | 12.8% | 122 | 117 | 9 | 1.54 |
| Dune management | 4.52 | 4.60 | 5.01 | 0.4% | 1.7% | 198 | 341 | 15 | 0.88 |
| Salt marshes | 2.50 | 2.95 | 3.72 | 3.3% | 4.8% | 147 | 217 | 12 | 1.11 |
| Flood insurance | 1.96 | 2.47 | 2.46 | 4.7% | -0.1% | 97 | 177 | 6 | 0.68 |
| Sediment transport | 8.71 | 8.17 | 7.59 | -1.3% | -1.5% | 300 | 618 | 30 | 0.97 |
| Erosion monitoring | 5.77 | 6.63 | 6.88 | 2.8% | 0.8% | 272 | 475 | 27 | 1.14 |
| Port infrastructure | 2.72 | 2.58 | 2.28 | -1.1% | -2.4% | 90 | 194 | 7 | 0.72 |

In the universe, 377 of 7539 works of 2018 to 2020 were cited 40 times or more (5.00%). Median growth 2020-25 of the twelve: 1.40%. Median share in 2025: 4.34%.

### Works per year

The universe and the six topics the conclusions name.

| year | universe | Nature-based defences | Living shorelines | Storm-surge forecasting | Seawalls | Groundwater salinisation | Managed retreat |
|---|---|---|---|---|---|---|---|
| 2012 | 1480 | 9 | 20 | 45 | 110 | 7 | 12 |
| 2013 | 1565 | 11 | 23 | 48 | 115 | 7 | 14 |
| 2014 | 1702 | 13 | 25 | 50 | 123 | 8 | 16 |
| 2015 | 1838 | 17 | 29 | 56 | 132 | 9 | 18 |
| 2016 | 1971 | 22 | 33 | 63 | 134 | 10 | 21 |
| 2017 | 2154 | 30 | 36 | 66 | 150 | 11 | 26 |
| 2018 | 2290 | 39 | 41 | 72 | 156 | 12 | 31 |
| 2019 | 2533 | 53 | 46 | 85 | 169 | 13 | 40 |
| 2020 | 2716 | 71 | 51 | 87 | 172 | 15 | 46 |
| 2021 | 2948 | 89 | 60 | 98 | 181 | 16 | 56 |
| 2022 | 3197 | 111 | 73 | 103 | 184 | 18 | 67 |
| 2023 | 3342 | 135 | 87 | 109 | 185 | 19 | 78 |
| 2024 | 3618 | 169 | 103 | 119 | 187 | 20 | 96 |
| 2025 | 3951 | 213 | 122 | 247 | 196 | 23 | 122 |
