# Changelog

## 2.0.0
A major version: foresight leaves this plugin, and two paths of the files contract are no longer written here.

- **Foresight moved to [poiesis-foresight](https://github.com/gorgmihai92/poiesis-foresight)** (0.1.0, its `main`
  at `874fab3`, checked 2026-11-22). Removed from here, and where each went there:
  - `playbooks/foresight.md` → the playbooks `horizons`, `layers`, `forecasts` and `trends` of its `foresight`
    skill (every rule sentence is there word for word);
  - `scripts/forecasts.py` → `skills/foresight/scripts/forecasts.py` (the same output on the lab's test log);
  - `agents/foresight-analyst.md` → its `foresight-analyst` agent;
  - `templates/forecasts.md` and `templates/signal.md` → its templates of the same names;
  - the notes of Hiltunen 2008, Sharpe et al. 2016 (with its open text), Inayatullah 1998, Phadnis et al. 2015,
    Mellers et al. 2015, Benneyan et al. 2003 and Kahneman & Lovallo 1993 → its `research/notes/`.
- **Files contract:** this plugin no longer writes `foresight/<date>-<topic>.md` or `foresight/forecasts.md`;
  poiesis-foresight writes them with the same columns. `ids.py` still reads `foresight/` to follow **From** lines.
- Every remaining mention of foresight points to the new plugin; the READMEs count five products.
- **The challenge stamp.** `challenge_stamp.py` records each verdict once, in `insights/challenge-stamps.jsonl`,
  with the conclusion's id, the day and a hash of its sentence. `verify` fails on a missing stamp, a changed
  sentence, a retyped verdict or an altered line. `stamp-format.md` describes the format so that poiesis-frontier
  and poiesis-studio can verify a stamp with their own code.
- **Ids and From.** Each insight carries `- **Id:** IN-001`, each research question `- **Id:** QN-001`, and a
  `- **From:**` line that names what it rests on. `ids.py` gives the next free id, lists what rests on what, and
  reports what went stale when a verdict changed. It changes nothing.
- **The entry gate.** `quote_gate.py` looks for each quote of a research note in the source's text before an
  insight is built on the note, and names the notes it could not check.
- **Playbook `questions`:** a gap described by where and why the evidence falls short, the kind of gap checked,
  then the assumptions behind it contested on five types. Template `question.md`.
- **Playbook `methods`:** a field's designs, samples and measures tabled study by study, method patterns as
  counted conclusions, and the field's findings re-read against them. Template `methods.md`.
- **Playbook `challenge`:** a ninth check, absence ("none found" is not "does not exist"); the stamp; a new
  challenge when the method, the data or the sentence changes after a verdict; five claims per saved report
  drawn by `sample_check.py` for a person to check, with what the checks so far allow.
- **`challenger` agent:** one structured block per conclusion (claim, verdict, narrower claim, reason, parts,
  rivals added, checks, confidence, not checked). The word limit is gone; it still runs on Sonnet. Its answer is
  saved as it came, in `insights/challenges/`, and the stamps are written from that file.
- **Rules:** each rule whose source was read only as an abstract, or not read, says so. New sections on the entry
  gate, ids and From, "a verdict is written once" and "not found is not does not exist". A step with no playbook
  or script is named as missing, not improvised.
- **Eleven research notes**, each with how much of its source was read; tests for every script (`tests/`); six
  eval cases (`plugins/poiesis-insight/evals/`), written and not run.
- Files contract, additions only: the **Id** and **From** lines, `insights/challenge-stamps.jsonl`,
  `insights/challenges/`, `insights/human-checks.md`. `- **Challenge:**` may now read `not challenged`.

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
