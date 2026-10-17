# Poiesis Insight

A Claude Code plugin that interprets the research or data a project already has. It finds **insights** (what the
evidence means) and does **foresight** (what is emerging and what may come). Every conclusion carries its evidence,
its rival explanations and what would prove it wrong, and must survive a challenge before it is reported.

For anyone with research notes, interviews, surveys or usage data who needs conclusions that hold up. Install it
below and ask in plain language.

## The Poiesis toolkits

**Collect → connect → explore → create.** Four toolkits. Each works on its own; together, each reads what the others
left in your project, as plain files.

| Toolkit | Role | Agents | Reads | Leaves in your project |
|---|---|---|---|---|
| [poiesis-research](https://github.com/gorgmihai92/poiesis-research) | **collect:** the literature on a topic, the evidence for and against a claim, the grants that fit | `paper-scout`, `evidence-scout`, `funding-scout` | the web's scholarly databases, official funding pages | `research/` |
| [poiesis-insight](https://github.com/gorgmihai92/poiesis-insight) | **connect:** what the evidence or your data mean, and what is emerging; every conclusion challenged | `insight-analyst`, `foresight-analyst`, `challenger` | `research/`, your own data, `frontier/results/` | `insights/`, `foresight/` |
| [poiesis-frontier](https://github.com/gorgmihai92/poiesis-frontier) | **explore:** new concepts, each with the smallest experiment that could kill it | `experimentalist` | `insights/`, `foresight/`, `research/` | `frontier/` |
| [poiesis-design](https://github.com/gorgmihai92/poiesis-design) | **create:** how the interface looks, behaves and what it says, checked before release | `ui-auditor`, `ux-tester`, `copy-reviewer` | your code, `.poiesis-design/` | `.poiesis-design/`, design tokens, components |

```
research ──► insight ──► frontier ──► design
               ▲            │
               └─ results ◄─┘   (experiment results go back to insight as data)
```

- **One job each.** Research says what sources say; insight says what it means; frontier proposes what could be
  and how to test it; design builds and checks. None does another's job.
- **None needs another.** When one would really improve the answer, Claude says so once, in one line, and offers
  to install it. You can say no; the work goes on and the report says what was left out.
- **Depth you choose:** quick, standard (the default) or thorough, per request or as a line in your project's
  `CLAUDE.md`, e.g. `Depth: quick`. A few rules hold at every depth (nothing invented, sources cited, interpretation
  labelled); the rest scale with what is at stake, and every report ends with what was **not checked**.
- **Short answers.** The answer first; the full work goes in the saved file. Agents are used only for independent
  parts in parallel, or for an independent check at thorough depth.
- **Rules limit what is reported as true, never what may be explored.**

## Three kinds of question: what it means, what is coming, whether it holds

| You want to know | It returns | Saved in |
|---|---|---|
| **Insight:** what the evidence means | connections, contradictions and counted patterns, and, on request, hidden correlations from a free search confirmed on held-out data; each with its evidence, rivals, confidence and what it means for the project | `insights/` |
| **Foresight:** what is emerging and what may come | weak signals, trends in your data (checked against noise and base rates), the three horizons, layered readings, scenarios (what holds across them, what depends on one) and dated forecasts | `foresight/` |
| **Challenge:** whether a conclusion holds | for each conclusion: kept, weakened (with the narrower claim) or dropped, and why | in the report |

Every conclusion from insight or foresight goes through the challenge before you see it. The input is your
[poiesis-research](https://github.com/gorgmihai92/poiesis-research) library, your own data (forms, tables,
documents), or both.

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
- *"Which weak signals in these notes point to where the field is going? Give scenarios and forecasts."*
- *"Search this usage log for correlations we haven't thought of."*
- *"Is the drop in weekly signups a real trend or noise?"*
- *"Challenge this conclusion: users leave because the pricing page is confusing."*
- *"Run insight-analyst and foresight-analyst in parallel, then the challenger on both."*

## Evidence first, then meaning, then a challenge

One skill, `insight`, is the entry point. It reads your research library (`research/`) or the data you give it,
collects the evidence first, then picks a **playbook**. Each playbook has an **agent** for parallel work.

| Playbook | Agent | What it does |
|---|---|---|
| insight | `insight-analyst` | lists the evidence and what was observed, fixes the comparisons in advance, then looks for connections, contradictions and counted patterns; for hidden correlations, searches freely and confirms leads on held-out data |
| foresight | `foresight-analyst` | logs signals (visibility, spread and meaning kept apart), checks trends in data against noise and base rates, places them on three horizons, reads the issue in four layers, builds scenarios, writes forecasts |
| challenge | `challenger` | tries to show why each conclusion is wrong: rivals, diagnostic evidence, independence, chance, sensitivity, consistency, denominators, replication |

- **Evidence before meaning.** What the input shows is collected first, each item with its reference; only then is
  it interpreted, and every conclusion points back to its items.
- **An independent challenge at thorough depth.** The `challenger` gets the conclusions and the data, not the
  reasoning that produced them, so it can find what the analyst missed. At quick and standard depth the challenge
  runs inline, which costs less.
- **Forecasts are scored.** A foresight claim that can be checked later becomes a forecast: a precise question, a
  probability and a date, logged in `foresight/forecasts.md`. `forecasts.py` scores the log (Brier score) once the
  dates pass, so you learn which reasoning to trust.

## Working with poiesis-research and your own data

**From poiesis-research** (if the project has it): insight starts from `research/README.md`, the library's
index, and reads the notes in `research/notes/`, one per source, with each claim and its page. Insights cite back
to the note and page. Insight never edits the research files; it writes only to `insights/` and `foresight/`.

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
- **Trends in data** are reported only when the change exceeds the series' usual noise, starting from how often
  similar changes continued.
- **Interpretation is labelled** as interpretation, and nothing is added from memory without saying so.

## Reports stay in `insights/` and `foresight/`

```
insights/<date>-<topic>.md     the question, the evidence, the insights that survived (with their challenge
                               result) and the ones dropped, with the reason
foresight/<date>-<topic>.md    signals, horizons, layers, scenarios and what survived the challenge
foresight/forecasts.md         the forecast log: question, probability, date made, date to resolve, outcome
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
    skills/insight/           the skill: what Claude follows when you ask for insights or foresight
      SKILL.md                entry point: reads the input (research library or your data), picks the playbook
      rules.md                what every conclusion carries, weighing, data before patterns; with sources
      playbooks/
        insight.md            connections, contradictions, counted patterns, free search with a hold-out
        foresight.md          signals, trends in data, horizons, layers, scenarios, forecasts
        challenge.md          the eight checks and the verdict
      scripts/                Python 3; Excel and Word libraries install themselves on first use
        to_text.py            convert Excel, Word and CSV into CSV or TXT, masking emails and phone numbers
        forecasts.py          score the forecast log (Brier score)
      templates/
        insight.md            one insight with everything it carries
        signal.md             one signal: observed, visibility, spread, interpretation, horizon
        forecasts.md          the forecast log
    agents/
      insight-analyst.md      insights for one question
      foresight-analyst.md    foresight for one issue
      challenger.md           tests conclusions before they are reported
research/                     the sources behind the rules: one note per source
CHANGELOG.md                  what changed in each version
LICENSE                       MIT
```

## Where the rules come from

Each rule names its source; there is one note per source in `research/notes`.

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
- **Weak signals (visibility, spread and meaning kept apart):** Hiltunen 2008.
- **Three horizons (H1, H2+, H2−, H3):** Sharpe et al. 2016.
- **Uncommon conclusions from deeper layers:** Inayatullah 1998, causal layered analysis.
- **Scenarios guide flexible choices, not predictions:** Phadnis et al. 2015.
- **Forecasts with probabilities and dates, scored later:** Mellers et al. 2015.
- **Trends: signal or noise:** Benneyan, Lloyd & Plsek 2003, control charts.
- **Trends: start from the base rate:** Kahneman & Lovallo 1993, the outside view.

## Files shared with the other toolkits

Writes `insights/<date>-<topic>.md`, each insight with **Evidence**, **Confidence**, **Found by**, **Challenge** (kept / weakened / dropped) and **So what**, read by frontier; `foresight/` scenarios and the forecast log `foresight/forecasts.md`. It reads research notes and frontier's results.

The paths and fields the other toolkits read are a contract: they change only in a major version, noted in the
changelog. Every plugin reads the others' files tolerantly: a missing file or field is reported as unknown, never
an error. The full list is in each skill's `SKILL.md`, so Claude knows it too.

## Update or remove

```
/plugin marketplace update poiesis-insight
/plugin update poiesis-insight@poiesis-insight
/plugin uninstall poiesis-insight@poiesis-insight
```

## Changing the plugin

Edit the files under `plugins/poiesis-insight/`, run `claude plugin validate .`, bump the version (major if a field under "Files" changes) in
`plugin.json`, `marketplace.json` and `CHANGELOG.md`, and push. Projects get it with the update commands above.

## License

MIT.
