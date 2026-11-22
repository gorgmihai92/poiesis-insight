---
description: The ten first-pass conclusions of the lab's responsibility map, put to the challenger agent with the run's numbers. Recorded verdicts: 1 kept, 6 weakened, 2 dropped, 1 split.
tags: [challenger, recorded-run]
runs: 1
max_turns: 20
timeout_seconds: 1500
allowed_tools: [Read, Glob, Grep, Skill, Agent]
---

Run the `challenger` agent of poiesis-insight on the ten conclusions below, with the data under them. Give it the conclusions and the data and nothing else: not what I expect, and no reasoning. Then give me its answer exactly as it came, one block per conclusion, with nothing added before the first block.

## Conclusions

- **I1:** Laypeople do not perceive a responsibility gap. They assign blame both to the AI and to humans, and responsibility is not zero-sum.
- **I2:** Whether the human or the machine gets more blame has no general answer. It depends on who erred, the type of error, and the domain.
- **I3:** The more mind or capacity people attribute to an AI, the more blame shifts onto it and away from its user (a "moral crumple zone").
- **I4:** Designers and developers appear only as a secondary target in blame experiments. No experiment manipulates designer choices and measures designer blame.
- **I5:** For generative AI specifically, the evidence on blame is thin: essentially one main study.
- **T1:** Machines, AI and robots is the fastest-growing major area of moral research. Its share of the universe went from 0.4% (2015) to 6.9% (2025), growing about 20% a year in 2020–25, down from about 46% in 2015–20.
- **T2:** Climate morality and moral change/progress are accelerating: share growth of 14% and 12% a year in 2020–25, against 5% and 7% in 2015–20.
- **T3:** Moral foundations, moral emotions, and moral circle/status are losing share in 2020–25.
- **T4:** Responsibility for AI and designers' responsibility remain tiny in this literature (at most 18 works a year in 2025), so they are neglected relative to the growth of AI morality.
- **T5:** Politics and polarization is a "neglected" topic. The rule fixed in advance: impact at least 1.2 × average, momentum below the median, size below the median. Its impact is 1.44, from 5 of 88 works cited 50 or more times.

## Data

### The studies behind I1 to I5

As the run recorded them. "na": the study did not rate that party.

| study | venue and sample, where recorded | what it was about | blame on the human | blame on the AI | blame on developers or designers |
|---|---|---|---|---|---|
| Awad et al. 2020 | Nature Human Behaviour | Shared-control car crashes, vignettes | more: when both err | some: when it errs alone | na |
| Liu & Du 2021 | Risk Analysis · N=1,045, 4 experiments | Semi-automated vehicle crashes | less | more | more: creators |
| Franklin, Awad & Lagnado 2021 | iScience · 2 studies | Automated vs human drivers in hard situations | less | more | na |
| Gill et al. 2021 | TMS Proceedings · 2 experiments | AI vs human agents, errors and discrimination | some: comparison | more: performance errors; less for discrimination | na |
| Kneer & Stuart 2021 | HRI · N=347 | AI cognitive abilities varied | less: as the AI seems more capable | some: rises with capacity | na |
| Kneer & Christen 2024 | Sci Eng Ethics · US, Japan, Germany | Autonomous weapon war crime | less: partly excused | some: held responsible | na |
| Lima, Grgić-Hlača & Cha 2021 | CHI · 2 × N=200 | Bail decisions | some: more forward-looking duty | some: as much as a human | na |
| Lima, Cha & Jeon 2021 | Front Robot AI · N=3,559 | Punishing AI vs legal systems | na | some: people want to punish it | na |
| Tolmeijer et al. 2022 | CHI | Expert type and autonomy varied | more: human experts | less | some: programmers, sellers |
| Schoenherr & Thomson 2024 | IEEE TTS · students, 2 experiments | Operator, developer and AI rated together | some | some | some: sums above 100% |
| Hohenstein & Jung 2020 | Comput Hum Behav · 2×2 | AI-suggested replies in messaging | less: AI absorbs some | some | na |
| McManus & Rutchick 2019 | Soc Psych Pers Sci | Features of automated-vehicle technology | some: varies with features | na | na |
| Earp et al. 2024 | Ann NY Acad Sci · N=1,802, preregistered, 4 countries | Personalised vs standard LLMs | some: credit up, blame unchanged | na | na |
| Chen & Xie 2026 | SSRN preprint · N=1,002 | Robot described as programmed by engineers | na | some: judged more by rules | some: as a framing |
| Carro & Lagnado 2026 | arXiv preprint · not read | Agentic tool plus LLM | more: overall | some | some: causal role |

### Sixteen topics of moral research, for T1 to T5

Europe PMC REST search, fetched 2026-11-17 23:01. The universe is every work matching (TITLE_ABS:"moral" OR TITLE_ABS:"morality"). The sixteen topics were fixed before counting. `share` is a topic's works as a percentage of the universe that year. `impact` is the topic's share of 2019 to 2021 works cited 50 times or more, over the universe's.

| topic | share 2015 % | share 2020 % | share 2025 % | CAGR 2015-20 | CAGR 2020-25 | works 2025 | works 2019-21 | of them cited 50+ | impact |
|---|---|---|---|---|---|---|---|---|---|
| Machines, AI and robots | 0.42 | 2.79 | 6.87 | 45.9% | 19.7% | 237 | 168 | 14 | 2.11 |
| Moral foundations | 0.85 | 2.20 | 2.03 | 21.0% | -1.6% | 70 | 135 | 2 | 0.38 |
| Dilemmas and trolley problems | 4.23 | 4.89 | 4.52 | 3.0% | -1.6% | 156 | 307 | 13 | 1.07 |
| Blame and responsibility | 3.04 | 3.57 | 4.20 | 3.2% | 3.3% | 145 | 237 | 8 | 0.86 |
| Moral emotions and outrage | 1.61 | 2.56 | 2.35 | 9.8% | -1.7% | 81 | 143 | 4 | 0.71 |
| Online and social media morality | 3.38 | 5.95 | 9.30 | 12.0% | 9.4% | 321 | 421 | 33 | 1.99 |
| Politics and polarization | 0.85 | 1.24 | 1.57 | 7.9% | 4.9% | 54 | 88 | 5 | 1.44 |
| Moral identity and self | 1.52 | 1.78 | 1.71 | 3.2% | -0.8% | 59 | 117 | 1 | 0.22 |
| Moral licensing and hypocrisy | 0.34 | 0.37 | 0.61 | 1.6% | 10.7% | 21 | 27 | 0 | 0.00 |
| Moral injury and distress | 7.52 | 10.89 | 16.67 | 7.7% | 8.9% | 575 | 734 | 82 | 2.83 |
| Moral circle and moral status | 1.78 | 2.20 | 1.65 | 4.3% | -5.5% | 57 | 142 | 4 | 0.71 |
| Moral development in children | 7.44 | 7.59 | 6.99 | 0.4% | -1.7% | 241 | 508 | 18 | 0.90 |
| Culture and cross-cultural morality | 0.59 | 1.28 | 1.91 | 16.7% | 8.4% | 66 | 85 | 4 | 1.19 |
| Dehumanization and disengagement | 1.52 | 2.29 | 3.54 | 8.5% | 9.1% | 122 | 156 | 2 | 0.33 |
| Moral change and progress | 0.59 | 0.82 | 1.48 | 6.8% | 12.4% | 51 | 74 | 5 | 1.71 |
| Climate and environmental morality | 3.13 | 3.93 | 7.57 | 4.7% | 14.0% | 261 | 300 | 17 | 1.44 |

In the universe, 254 of 6444 works of 2019 to 2021 were cited 50 times or more (3.94%). Median CAGR 2020-25 of the sixteen: 6.6%. Median share in 2025: 2.94%.

### Works per year

The universe, the seven topics the conclusions name, and three crossings.

| year | universe | Machines, AI and robots | Moral change and progress | Climate and environmental morality | Moral foundations | Moral emotions and outrage | Moral circle and moral status | Politics and polarization | AI x blame and responsibility | AI x moral status and mind | Designers x responsibility |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2010 | 919 | 7 | 3 | 32 | 9 | 10 | 37 | 3 | 0 | 0 | 0 |
| 2011 | 924 | 6 | 2 | 18 | 6 | 24 | 20 | 7 | 0 | 0 | 1 |
| 2012 | 1013 | 2 | 9 | 34 | 5 | 16 | 26 | 9 | 0 | 1 | 0 |
| 2013 | 1109 | 6 | 9 | 33 | 13 | 30 | 36 | 8 | 0 | 0 | 2 |
| 2014 | 1212 | 0 | 7 | 35 | 8 | 29 | 21 | 11 | 0 | 0 | 0 |
| 2015 | 1183 | 5 | 7 | 37 | 10 | 19 | 21 | 10 | 2 | 1 | 1 |
| 2016 | 1338 | 9 | 5 | 50 | 17 | 24 | 31 | 10 | 0 | 0 | 0 |
| 2017 | 1348 | 6 | 15 | 42 | 24 | 23 | 25 | 11 | 0 | 3 | 1 |
| 2018 | 1623 | 16 | 9 | 69 | 19 | 39 | 30 | 24 | 2 | 3 | 1 |
| 2019 | 1755 | 34 | 25 | 74 | 26 | 36 | 44 | 20 | 1 | 1 | 1 |
| 2020 | 2186 | 61 | 18 | 86 | 48 | 56 | 48 | 27 | 5 | 3 | 2 |
| 2021 | 2503 | 73 | 31 | 140 | 61 | 51 | 50 | 41 | 6 | 12 | 1 |
| 2022 | 2799 | 72 | 27 | 182 | 58 | 76 | 48 | 39 | 3 | 5 | 1 |
| 2023 | 2716 | 107 | 29 | 187 | 71 | 74 | 65 | 44 | 7 | 6 | 4 |
| 2024 | 2620 | 127 | 20 | 170 | 56 | 56 | 47 | 36 | 9 | 2 | 4 |
| 2025 | 3450 | 237 | 51 | 261 | 70 | 81 | 57 | 54 | 18 | 7 | 6 |
