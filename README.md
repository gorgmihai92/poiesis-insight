# Poiesis Insight

Interpretation that survives a challenge, in Claude Code. Poiesis Insight interprets the research or data a project
already has. It finds **insights** (what the evidence means), writes **research questions** from what the evidence
does not answer, and reads a field's findings against its **methods**. Every conclusion carries its evidence, its rival explanations and what would prove it wrong, and
must survive a challenge before it is reported. The verdict of that challenge is recorded once and cannot drift.

For anyone with research notes, interviews, surveys or usage data who needs conclusions that hold up. Poiesis
Insight is one of the five products in the [Poiesis Toolkit](#part-of-the-poiesis-toolkit) and works on its own, as
one plugin. Install it below and ask in plain language.

## Part of the Poiesis Toolkit

The Poiesis Toolkit is five products for Claude Code, one for each step from a question to a finished product:
**Research** collects, **Insight** connects, **Foresight** anticipates, **Frontier** explores, **Design** creates.
Each installs and works on its own. Insight, Foresight and Frontier also read what the other steps left in your
project, as plain files, and Design builds a Frontier concept when you ask.

Until version 1.4.3 Poiesis Insight also did foresight. Since 2.0.0 that is [Poiesis Foresight](https://github.com/gorgmihai92/poiesis-foresight), which holds
everything Insight had for it (signals, trends in data, horizons, layered readings, scenarios, the forecast log
and `foresight-analyst`) and more.

| Product | What it does | Plugins | Agents | Reads | Leaves in your project |
|---|---|---|---|---|---|
| [Poiesis Research](https://github.com/gorgmihai92/poiesis-research) | **collect:** the literature on a topic, the evidence for and against a claim, the grants that fit | `poiesis-research` | `paper-scout`, `evidence-scout`, `funding-scout` | the web's scholarly databases, official funding pages | `research/` |
| [Poiesis Insight](https://github.com/gorgmihai92/poiesis-insight) | **connect:** what the evidence or your data mean, what it leaves unanswered, how a field studies its subject; every conclusion challenged and its verdict recorded | `poiesis-insight` | `insight-analyst`, `challenger` | `research/`, your own data, `frontier/results/` | `insights/` |
| [Poiesis Foresight](https://github.com/gorgmihai92/poiesis-foresight) | **anticipate:** signals, trends, scenarios, forecasts, signposts | `poiesis-foresight` | `foresight-analyst`, `forecaster` | `research/`, `insights/`, your own data | `foresight/` |
| [Poiesis Frontier](https://github.com/gorgmihai92/poiesis-frontier) | **explore:** new concepts, each with the smallest experiment that could kill it | `poiesis-frontier` | `experimentalist` | `insights/`, `foresight/`, `research/` | `frontier/` |
| [Poiesis Design](https://github.com/gorgmihai92/poiesis-design) | **create:** how the interface looks, behaves and what it says, built from components that already pass, checked before release | `poiesis-ui`, `poiesis-ux`, `poiesis-copy`, `poiesis-components` | `ui-auditor`, `ux-tester`, `copy-reviewer` | your code, `.poiesis-design/` | `.poiesis-design/`, design tokens, components |

```
Research ──► Insight ──► Foresight ──► Frontier ──► Design
               ▲                          │
               └──────── results ◄────────┘   (experiment results go back to Insight as data)
```

- **One job each.** Research says what sources say; Insight says what it means; Foresight reads it forward;
  Frontier proposes what could be and how to test it; Design builds and checks. None does another's job.
- **None needs another.** When another product would really improve the answer, Claude says so once, in one line,
  and offers to install it. You can say no; the work goes on and the report says what was left out.
- **Depth you choose:** quick, standard (the default) or thorough, per request or as a line in your project's
  `CLAUDE.md`, e.g. `Depth: quick`. A few rules hold at every depth (nothing invented, sources cited, interpretation
  labelled); the rest scale with what is at stake, and every report ends with what was **not checked**.
- **Short answers.** The answer first; the full work goes in the saved file. Agents are used only for independent
  parts in parallel, or for an independent check at thorough depth.
- **Rules limit what is reported as true, never what may be explored.**

## Four kinds of question: what it means, what is missing, how a field works, whether it holds

| You want to know | It returns | Saved in |
|---|---|---|
| **Insight:** what the evidence means | connections, contradictions and counted patterns, and, on request, hidden correlations from a free search confirmed on held-out data; each with its evidence, rivals, confidence and what it means for the project | `insights/` |
| **Questions:** what the evidence does not answer | each gap described by where and why the evidence falls short, challenged like any conclusion; then research questions, with the assumption each one contests | `insights/` |
| **Methods:** how a field studies its subject | a table of designs, samples and measures, study by study; method patterns as counted conclusions; the field's findings re-read with the method in the sentence | `insights/` |
| **Challenge:** whether a conclusion holds | for each conclusion: kept, weakened (with the narrower claim) or dropped, and why; the verdict recorded with a stamp | `insights/challenge-stamps.jsonl` |

Every conclusion goes through the challenge before you see it. The input is your
[Poiesis Research](https://github.com/gorgmihai92/poiesis-research) library, your own data (forms, tables,
documents), or both. For what is emerging and what may come, ask [Poiesis Foresight](https://github.com/gorgmihai92/poiesis-foresight): Insight suggests it
once when a question needs it.

## Install

In Claude Code:

```
/plugin marketplace add gorgmihai92/poiesis-insight
/plugin install poiesis-insight@poiesis-insight
```

It needs **Python 3**, which macOS and most Linux systems already have. No keys, no setup.

## Ask in plain language

The plugin comes in when the work is interpretation, and you can name its agents directly.

- *"What insights come out of our research library on onboarding?"*
- *"Here are 40 interview transcripts: what patterns do you see, and how sure are you?"*
- *"Here is the Google Forms export of our customer survey (responses.csv): what stands out?"*
- *"Search this usage log for correlations we haven't thought of."*
- *"Is the drop in weekly signups a real trend or noise?"*
- *"Challenge this conclusion: users leave because the pricing page is confusing."*
- *"What does this literature not answer? Describe the gaps, then give me research questions."*
- *"How do the studies in my evidence table measure recall? What does that let them say?"*
- *"I changed the base of the shares. What in my notes is out of date now?"*
- *"Draw five claims from this report for me to check against the sources."*
- *"Run insight-analyst on the two studies in parallel, then the challenger on both."*

## Evidence first, then meaning, then a challenge

One skill, `insight`, is the entry point. It reads your research library (`research/`) or the data you give it,
collects the evidence first, then picks a **playbook**. Each playbook has an **agent** for parallel work.

| Playbook | Agent | What it does |
|---|---|---|
| insight | `insight-analyst` | lists the evidence and what was observed, fixes the comparisons in advance, then looks for connections, contradictions and counted patterns; for hidden correlations, searches freely and confirms leads on held-out data |
| questions | `insight-analyst` | describes each gap by the part of the question the studies do not cover and the reason no conclusion can be drawn, checks the kind of gap, then contests the assumptions behind it on five types |
| methods | `insight-analyst` | tables each study's design, sample and measures with how much of it was read, counts the patterns, and reads the field's findings against them |
| challenge | `challenger` | tries to show why each conclusion is wrong: rivals, diagnostic evidence, independence, chance, sensitivity, consistency, denominators, replication, and absence ("none found" is not "does not exist"); returns one structured verdict per conclusion |

- **Evidence before meaning.** What the input shows is collected first, each item with its reference; only then is
  it interpreted, and every conclusion points back to its items.
- **An independent challenge at thorough depth.** The `challenger` gets the conclusions and the data, not the
  reasoning that produced them, so it can find what the analyst missed. At quick and standard depth the challenge
  runs inline, which costs less.
- **Sources are checked before they are built on.** Before an insight rests on a research note, each quote in
  the note is looked for in the source's text. A note that could not be checked is used as unchecked, and the
  report says so.

## A verdict is recorded once

In two recorded runs of these plugins, 15 of 16 first conclusions did not survive the challenge as written. One
verdict then changed from weakened to kept when it was retyped onto a page, and numbers moved after the challenge
while the first verdicts stayed on them. Version 2.0.0 closes those gaps in code:

- **The stamp.** After the challenge, `challenge_stamp.py` writes one line per conclusion in
  `insights/challenge-stamps.jsonl`: its id, the verdict, the day and a hash of the conclusion's sentence. The
  check fails when the stamp is missing, when the sentence changed, when the verdict shown is not the stamped one,
  or when the line was edited. It makes a change visible; it does not prevent one.
- **Ids and From.** Each conclusion and question has an id (`IN-001`, `QN-001`) and a line that names what it
  rests on. When a verdict changes, `ids.py stale` lists everything that was built on it before. It reports and
  changes nothing.
- **A new challenge.** When the method, the data or the sentence changes after a verdict, the conclusion is
  challenged again and the new verdict is recorded next to the old one.
- **A person checks a sample.** The challenger is a model of the same family as the session that wrote the
  conclusions. For each saved report, `sample_check.py` draws five claims at random for you to check against
  their sources, and says what your checks so far allow: five clean checks still leave up to 45% of claims
  possibly wrong, thirty bring that under 10%.

Poiesis Frontier and Poiesis Studio read the stamps with their own code, from the description in
`plugins/poiesis-insight/skills/insight/stamp-format.md`.

## Working with Poiesis Research and your own data

**From Poiesis Research** (if the project has it): Poiesis Insight starts from `research/README.md`, the library's
index, and reads the notes in `research/notes/`, one per source, with each claim and its page, and the evidence
table in `research/maps/` when there is one. Insights cite back to the note and page. Insight never edits the
research files; it writes only to `insights/`.

**Your own data:**

1. **Convert** what Claude can't read directly. `to_text.py` turns Excel (one CSV per sheet), Word (.docx, .doc,
   .rtf, .odt) and CSV/TSV into CSV or TXT, and with `--mask` hides emails and phone numbers. A Google Forms export
   is already CSV. Your original file is never changed.
2. **Personal data:** columns that identify people (names, addresses, IDs) are dropped or replaced before
   analysis. Originals and converted files stay out of git and out of public places. Anything you give Claude is
   processed by the model, so share only data you're allowed to share.
3. **The data is described first**, at the top of the report: source, how and when it was collected, number of
   responses, optional questions, what is missing, duplicates or test answers. These are the denominators every
   conclusion is measured against.

Ask, for example: *"Convert survey.xlsx, mask personal data, describe it, then give me insights."*

## The same rules for every conclusion

The same rules apply to every playbook (`skills/insight/rules.md`), each with its source:

- **Every conclusion carries** its evidence, rival explanations generated before judging, the evidence that favors
  it over the rivals, what it rests on, what would prove it wrong, and a confidence level with the reason.
- **One weighing rule, applied the same way to every rival.** Not a ritual matrix: in a controlled study the
  matrix did not improve accuracy, while consistency did.
- **Data before patterns.** Rates over what was actually observed, never over units chosen because they show the
  outcome; comparisons fixed before looking; natural replications checked first; and when the data are a tool's
  output, whether the tool could produce the pattern.
- **Hidden patterns are checked harder,** not reported sooner: independent support and a test against chance.
- **Free search only with a hold-out.** Part of the data is set aside first; what the search finds is a lead,
  corrected for how many comparisons were tried, until it holds on the part set aside.
- **"None found" is not "does not exist".** A search that returns nothing says what was searched and which
  databases answered.
- **Interpretation is labelled** as interpretation, and nothing is added from memory without saying so.
- **Each rule says how much of its source was read.** A rule that rests on an abstract, or on an observation of
  one run, says so where it is stated.

## Reports stay in `insights/`

```
insights/<date>-<topic>.md     the question, the evidence, the insights that survived (with their challenge
                               result) and the ones dropped, with the reason; gaps, questions, method tables
insights/challenge-stamps.jsonl   one line per verdict, only ever added to
insights/challenges/           the challenger's answers, as they came
insights/human-checks.md       claims drawn for you to check, and what you found
```

## What's in this repository

The repository is a Claude Code **marketplace** holding one **plugin**, plus the research behind its rules.

```
.claude-plugin/
  marketplace.json            the marketplace: its name and the plugins it lists (here, one)
plugins/
  poiesis-insight/            the plugin
    .claude-plugin/
      plugin.json             name, version, description
    skills/insight/           the skill: what Claude follows when you ask for insights or research questions
      SKILL.md                entry point: reads the input (research library or your data), picks the playbook
      rules.md                what every conclusion carries, weighing, data before patterns; with sources
      stamp-format.md         the challenge stamp, described so that another plugin can verify one
      playbooks/
        insight.md            connections, contradictions, counted patterns, free search with a hold-out
        questions.md          gaps described, assumptions contested, research questions
        methods.md            a field's designs, samples and measures, and what they let it say
        challenge.md          the nine checks, the verdict, the stamp, the sample a person checks
      scripts/                Python 3; Excel and Word libraries install themselves on first use
        challenge_stamp.py    record a verdict once; check a note against its stamps
        ids.py                the next free id; what rests on what; what went stale
        quote_gate.py         look for each quote of a research note in the source's text
        sample_check.py       draw claims for a person to check; what the checks allow
        to_text.py            convert Excel, Word and CSV into CSV or TXT, masking emails and phone numbers
      templates/
        insight.md            one insight with everything it carries
        question.md           one research question and the gap it rests on
        methods.md            the method table of a field
    agents/
      insight-analyst.md      insights for one question
      challenger.md           tests conclusions and returns one structured verdict for each
    evals/                    six cases for `claude plugin eval`; written, not run
research/                     the sources behind the rules: one note per source, with how much was read
tests/                        tests for the scripts and the eval cases; they need Python 3 and no network
CHANGELOG.md                  what changed in each version
LICENSE                       MIT
```

## Where the rules come from

Each rule names its source; there is one note per source in `research/notes`, and each note says how much of the
source was read. The sources added in 2.0.0:

- **A gap described by where and why the evidence falls short:** Robinson, Saldanha & Mckoy 2011 (the report's
  framework and its limits were read; the journal article was not).
- **Three kinds of gap:** Sandberg & Alvesson 2011 (the typology was read, not the whole article).
- **Five types of assumption to contest:** Alvesson & Sandberg 2011 (read in full). Shown by its authors on one
  article; whether it gives better questions was not tested.
- **A person checks a sample:** Panickssery, Bowman & Feng 2024 and Wataoka, Takahashi & Ri 2024 (both read in
  full). They show that a model rating text favours its own and familiar text. They did not test checking a claim
  against its source, so the check is a precaution.
- **The challenger is measured, not assumed to work:** Du et al. 2023, Wang et al. 2024 and Smit et al. 2024
  (abstracts only) disagree on whether a second model pass helps.
- **Ids and what an object rests on:** W3C PROV-DM 2013 (the sections on entities and derivation).
- **The stamp, the new challenge, "none found", the method table:** the lab's two recorded runs. Observations of
  two runs, not rates.

The earlier sources:

- **Three paths to an insight (connections, contradictions, impasses):** Klein & Jarosz 2011.
- **Evidence first, then sensemaking:** Pirolli & Card 2005. Analysts forage for evidence and make sense of it in
  two loops, so every conclusion points back to its evidence.
- **Diagnostic evidence and competing hypotheses:** Heuer 1999. Evidence counts only if it favors one explanation
  over its rivals; try to disprove, report every hypothesis's likelihood, name what to watch.
- **One weighing rule, not a ritual matrix:** Dhami, Belton & Mandel 2019. The competing-hypotheses matrix did not
  improve accuracy; analysts who weighed evidence consistently were right 80% of the time against 31%.
- **Rival explanations before judging:** Nickerson 1998, confirmation bias.
- **Comparisons fixed in advance:** Simmons, Nelson & Simonsohn 2011. Flexible analysis makes false patterns likely.
- **Free search as leads, tested on a hold-out:** Nosek et al. 2018 (generating vs testing hypotheses); Gelman &
  Loken 2014 (forking paths).
- **Correcting for many comparisons:** Benjamini & Hochberg 1995, the false discovery rate.
- **Plot before summarizing:** Anscombe 1973.
- **Reversal inside subgroups and regression to the mean as rivals:** Simpson 1951; Barnett, van der Pols & Dobson 2005.
- **Confidence not taken from feeling sure:** Kahneman & Klein 2009. Intuition is reliable only in regular,
  learnable settings with feedback.
- **Hidden patterns checked harder:** Whitson & Galinsky 2008, illusory pattern perception (contested by a small
  replication).

The sources behind the foresight rules (Hiltunen 2008, Sharpe et al. 2016, Inayatullah 1998, Phadnis et al. 2015,
Mellers et al. 2015, Benneyan et al. 2003, Kahneman & Lovallo 1993) moved with those rules to
[Poiesis Foresight](https://github.com/gorgmihai92/poiesis-foresight), whose notes say how much of each was read.

## Files shared with the other products

Writes `insights/<date>-<topic>.md`, each insight with **Id**, **From**, **Evidence**, **Confidence**, **Found by**, **Challenge** (kept / weakened / dropped) and **So what**, read by Frontier; `insights/challenge-stamps.jsonl`, the verdicts as recorded, read by Frontier and Studio. Until 1.4.3 it also wrote `foresight/`; since 2.0.0 [Poiesis Foresight](https://github.com/gorgmihai92/poiesis-foresight) does. It reads Research notes, quotes and evidence tables, and Frontier's results.

The paths and fields the other products read are a contract: they change only in a major version, noted in the
changelog. Every plugin reads the others' files tolerantly: a missing file or field is reported as unknown, never
an error. The full list is in each skill's `SKILL.md`, so Claude knows it too.

## Update or remove

```
/plugin marketplace update poiesis-insight
/plugin update poiesis-insight@poiesis-insight
/plugin uninstall poiesis-insight@poiesis-insight
```

## Changing the plugin

Edit the files under `plugins/poiesis-insight/`, run `python3 -I -m unittest discover -s tests` and
`claude plugin validate plugins/poiesis-insight` (at the repository's root the command checks only the
marketplace file), bump the version (major if a field under "Files" changes) in `plugin.json`, `marketplace.json`
and `CHANGELOG.md`, and push. Projects get it with the update commands above.

## License

MIT.
