# Changelog

## 1.4.3
- Suggestions of another Poiesis plugin, from the skill or its agents, give the plugin's link and name the skill or
  agent to use.

## 1.4.2
- Saving: files only at standard or thorough depth, when asked, when the folder already exists, or for a
  forecast; otherwise the answer stays in the chat.
- "Files": the paths and fields shared with the other Poiesis plugins, as a contract (changed only in a major
  version), in the skill and the README; other plugins' files are read tolerantly.

## 1.4.1
- Depth is set with a `Depth:` line in the project's `CLAUDE.md`, so it works without poiesis-research.

## 1.4.0
- Depth: quick, standard (default) or thorough, per request or `Depth:` in `research.config.md`. A few rules hold
  at every depth; the rest are defaults, skippable if the report says why. Every report ends with "Not checked".
  Rules limit what is reported as true, never what may be explored.
- The challenge runs inline at quick and standard depth, by the `challenger` agent at thorough.
- Answers short and direct, the answer first; agents only for independent parallel parts or the thorough check;
  each agent has a word limit.
- "Other Poiesis plugins": when another one would change the result, Claude suggests it once and installs it only
  if the user agrees.
- README: the four toolkits, their roles, agents, what each reads and leaves, and how they connect.

## 1.3.0
- Insight: a free search for hidden correlations and uncommon patterns, allowed only with a hold-out set aside
  first; findings are leads, corrected for the number of comparisons tried, until they hold on the hold-out.
  Plot before summarizing; outliers checked for errors first; what the data should show and do not.
- Foresight: trends in time-ordered data, checked against the series' noise (control charts) and the base rate of
  similar changes, with their shape; extrapolation only as a dated forecast.
- Rivals now include reverse cause, regression to the mean and reversal inside subgroups; the challenge checks the
  comparison count and the hold-out. Insight template: "Found by" line.
- Eight new research notes.

## 1.2.0
- Your own data: `to_text.py` converts Excel, Word and CSV/TSV into CSV or TXT and masks emails and phone numbers;
  steps for personal data and for describing the data before interpreting it.
- What insight reads from poiesis-research: the index, the notes (cite back to note and page), funding calls.

## 1.1.0
- Rules for denominators (units analyzed, never units selected by the outcome), groupings fixed in advance, and
  what a replication tests.

## 1.0.0
- `insight` skill with three playbooks: insight, foresight, challenge; shared rules, each naming its source.
- Rules "Data before patterns": coverage and denominators, comparisons fixed in advance, natural replications,
  instrument or subject.
- Agents: insight-analyst, foresight-analyst, challenger.
- `forecasts.py` scores a forecast log with the Brier score.
