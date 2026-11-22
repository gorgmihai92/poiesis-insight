---
description: The six first-pass conclusions of the lab's trend scan, put to the challenger agent with the run's numbers. Recorded verdicts: all six weakened.
tags: [challenger, recorded-run]
runs: 1
max_turns: 20
timeout_seconds: 1500
allowed_tools: [Read, Glob, Grep, Skill, Agent]
---

Run the `challenger` agent of poiesis-insight on the six conclusions below, with the data under them. Give it the conclusions and the data and nothing else: not what I expect, and no reasoning. Then give me its answer exactly as it came, one block per conclusion, with nothing added before the first block.

## Conclusions

- **C1:** Synthetic biology shows a break in 2024–2025: its share growth is above its own 2013–2022 range (z 2.2 and 3.0, same in narrow terms) after a decade of slow growth.
- **C2:** Quantum computing is the largest and fastest-growing of the five by share (about 102 per 100k works in 2025), accelerating steadily (share CAGR 20% in 2015–20, 26% in 2020–25), but with no year beyond its usual variation.
- **C3:** Solid-state battery research is slowing: share growth fell from 23%/yr (2015–20) to 11%/yr (2020–25), and its share dropped in 2025.
- **C4:** Neuromorphic computing grows steadily (~19%/yr in share) within its usual variation, slightly slower than in 2015–20.
- **C5:** Brain-computer interfaces grow slowly with a modest acceleration (share CAGR 2.7% → 9.3%), within usual variation.
- **C6:** Raw counts overstate 2025 growth in all five areas, because the OpenAlex corpus itself grew about 29% in 2025.

## Data

OpenAlex, fetched 2026-11-17 22:24. Five areas, each a fixed set of search terms in titles and abstracts. 2026 is left out: the year was not over.

### The whole database, by year

Works of every type, and articles, reviews and preprints only, with each one's growth on the year before.

| year | all works | growth % | articles, reviews, preprints | growth % |
|---|---|---|---|---|
| 2018 | 9619421 | -0.4 | 5702952 | -0.9 |
| 2019 | 10108929 | 5.1 | 5994899 | 5.1 |
| 2020 | 10710227 | 5.9 | 6397095 | 6.7 |
| 2021 | 10257354 | -4.2 | 6099087 | -4.7 |
| 2022 | 9930832 | -3.2 | 5798956 | -4.9 |
| 2023 | 10693671 | 7.7 | 6109094 | 5.3 |
| 2024 | 11003303 | 2.9 | 6656456 | 9.0 |
| 2025 | 14226691 | 29.3 | 7846617 | 17.9 |

### Share of each area, per 100,000 works

`all`: works of every type that match the area's terms, over all works. `art`: articles, reviews and preprints that match, over articles, reviews and preprints. The six conclusions were written from `all`.

| year | Quantum computing all | Quantum computing art | Solid-state batteries all | Solid-state batteries art | Brain-computer interfaces all | Brain-computer interfaces art | Neuromorphic computing all | Neuromorphic computing art | Synthetic biology all | Synthetic biology art |
|---|---|---|---|---|---|---|---|---|---|---|
| 2010 | 10.97 | 9.94 | 4.06 | 4.65 | 14.16 | 10.64 | 3.87 | 2.35 | 8.02 | 8.19 |
| 2011 | 11.29 | 9.76 | 3.86 | 4.41 | 16.26 | 11.3 | 4.72 | 2.79 | 9.3 | 9.0 |
| 2012 | 12.65 | 11.06 | 4.7 | 5.4 | 16.02 | 11.55 | 4.81 | 3.22 | 10.75 | 11.68 |
| 2013 | 13.01 | 12.0 | 5.92 | 6.71 | 20.74 | 15.01 | 5.66 | 3.64 | 12.18 | 12.05 |
| 2014 | 12.89 | 12.08 | 6.97 | 6.95 | 19.8 | 14.71 | 5.98 | 4.13 | 14.2 | 14.06 |
| 2015 | 12.95 | 12.63 | 7.67 | 7.98 | 20.4 | 15.43 | 7.29 | 5.18 | 13.73 | 14.19 |
| 2016 | 13.5 | 13.34 | 10.4 | 10.41 | 22.5 | 16.26 | 8.69 | 6.45 | 15.25 | 17.02 |
| 2017 | 17.04 | 17.29 | 12.48 | 15.49 | 21.69 | 17.38 | 11.87 | 8.86 | 15.28 | 17.73 |
| 2018 | 22.88 | 23.86 | 16.15 | 21.13 | 24.63 | 20.74 | 15.27 | 13.38 | 16.46 | 19.25 |
| 2019 | 27.13 | 26.69 | 20.51 | 25.24 | 23.83 | 20.35 | 18.54 | 17.23 | 16.62 | 19.07 |
| 2020 | 32.39 | 33.37 | 21.87 | 28.51 | 23.27 | 22.14 | 21.84 | 21.56 | 16.91 | 20.21 |
| 2021 | 43.48 | 46.5 | 23.05 | 32.66 | 26.85 | 25.23 | 25.54 | 26.91 | 17.09 | 21.84 |
| 2022 | 49.29 | 54.23 | 28.56 | 40.09 | 28.1 | 27.75 | 33.31 | 36.35 | 18.44 | 23.19 |
| 2023 | 60.84 | 66.0 | 30.43 | 43.89 | 28.66 | 29.91 | 37.79 | 41.53 | 17.72 | 23.72 |
| 2024 | 83.17 | 84.16 | 38.47 | 48.76 | 33.14 | 32.72 | 46.33 | 49.41 | 21.45 | 27.24 |
| 2025 | 102.39 | 113.6 | 37.08 | 52.02 | 36.37 | 39.83 | 52.07 | 61.61 | 27.22 | 38.62 |

### Growth of each area, four ways of counting

Growth is the natural log of a year over the year before. `mean` and `SD` are over 2013 to 2022. `z` is (growth - mean) / SD. `CAGR` is the yearly rate over five years. The four rows of an area: its share of all works; its share of articles, reviews and preprints; the same with the area's narrow terms only; and the raw count of articles, reviews and preprints.

| area | counted as | mean | SD | growth 2023 | growth 2024 | growth 2025 | z 2023 | z 2024 | z 2025 | CAGR 2015-20 | CAGR 2020-25 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Quantum computing | share of all works | 0.136 | 0.116 | 0.211 | 0.313 | 0.208 | 0.6 | 1.5 | 0.6 | 20.1% | 25.9% |
| Quantum computing | share of articles etc. | 0.159 | 0.118 | 0.196 | 0.243 | 0.300 | 0.3 | 0.7 | 1.2 | 21.5% | 27.8% |
| Quantum computing | same, narrow terms | 0.165 | 0.132 | 0.289 | 0.359 | 0.361 | 0.9 | 1.5 | 1.5 | 21.6% | 35.6% |
| Quantum computing | raw count | 0.165 | 0.105 | 0.248 | 0.329 | 0.464 | 0.8 | 1.6 | 2.9 | 23.2% | 33.1% |
| Solid-state batteries | share of all works | 0.180 | 0.086 | 0.063 | 0.234 | -0.037 | -1.4 | 0.6 | -2.5 | 23.3% | 11.1% |
| Solid-state batteries | share of articles etc. | 0.200 | 0.104 | 0.090 | 0.105 | 0.065 | -1.1 | -0.9 | -1.3 | 29.0% | 12.8% |
| Solid-state batteries | same, narrow terms | 0.316 | 0.124 | 0.180 | 0.112 | 0.152 | -1.1 | -1.7 | -1.3 | 47.3% | 20.6% |
| Solid-state batteries | raw count | 0.206 | 0.094 | 0.142 | 0.191 | 0.229 | -0.7 | -0.2 | 0.2 | 30.8% | 17.5% |
| Brain-computer interfaces | share of all works | 0.056 | 0.100 | 0.020 | 0.145 | 0.093 | -0.4 | 0.9 | 0.4 | 2.7% | 9.3% |
| Brain-computer interfaces | share of articles etc. | 0.088 | 0.086 | 0.075 | 0.090 | 0.197 | -0.1 | 0.0 | 1.3 | 7.5% | 12.5% |
| Brain-computer interfaces | same, narrow terms | 0.100 | 0.089 | 0.113 | 0.077 | 0.202 | 0.1 | -0.3 | 1.1 | 8.3% | 14.2% |
| Brain-computer interfaces | raw count | 0.094 | 0.091 | 0.127 | 0.176 | 0.361 | 0.4 | 0.9 | 2.9 | 9.0% | 17.2% |
| Neuromorphic computing | share of all works | 0.194 | 0.071 | 0.126 | 0.204 | 0.117 | -1.0 | 0.1 | -1.1 | 24.5% | 19.0% |
| Neuromorphic computing | share of articles etc. | 0.242 | 0.087 | 0.133 | 0.174 | 0.221 | -1.3 | -0.8 | -0.3 | 33.0% | 23.4% |
| Neuromorphic computing | same, narrow terms | 0.406 | 0.237 | 0.235 | 0.160 | 0.297 | -0.7 | -1.0 | -0.5 | 70.7% | 26.8% |
| Neuromorphic computing | raw count | 0.248 | 0.075 | 0.185 | 0.260 | 0.385 | -0.8 | 0.2 | 1.8 | 34.9% | 28.5% |
| Synthetic biology | share of all works | 0.054 | 0.061 | -0.040 | 0.191 | 0.238 | -1.5 | 2.2 | 3.0 | 4.2% | 10.0% |
| Synthetic biology | share of articles etc. | 0.069 | 0.060 | 0.022 | 0.138 | 0.349 | -0.8 | 1.2 | 4.7 | 7.3% | 13.8% |
| Synthetic biology | same, narrow terms | 0.072 | 0.063 | 0.036 | 0.154 | 0.360 | -0.6 | 1.3 | 4.6 | 7.5% | 14.7% |
| Synthetic biology | raw count | 0.075 | 0.069 | 0.074 | 0.224 | 0.514 | -0.0 | 2.2 | 6.4 | 8.9% | 18.6% |
