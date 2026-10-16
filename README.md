# Poiesis Insight

A Claude Code plugin that interprets the research or data a project already has. It finds **insights** (what the
evidence means) and does **foresight** (what is emerging and what may come). Every conclusion carries its evidence,
its rival explanations and what would prove it wrong, and must survive a challenge before it is reported.

## The Poiesis toolkits

**Collect → connect → create.** Three toolkits, each usable on its own; together, each one builds on what the
previous one left in your project.

| Toolkit | You | What it does | Leaves in your project |
|---|---|---|---|
| [poiesis-research](https://github.com/gorgmihai92/poiesis-research) | **collect** | finds and cites sources: the literature on a topic, the evidence behind a claim, the grants that fit | `research/` |
| [poiesis-insight](https://github.com/gorgmihai92/poiesis-insight) | **connect** | interprets what was collected, or any data: insights and foresight, each conclusion challenged | `insights/`, `foresight/` |
| [poiesis-design](https://github.com/gorgmihai92/poiesis-design) | **create** | designs the interface and how the app behaves, and checks both before release | `.poiesis-design/`, your design tokens |

Research reports what sources say and stops there. Insight reads `research/` (or your own data) and says what it
means. Design decisions can then point to the insight or source behind them.

## What it covers

| You want to know | It returns | Saved in |
|---|---|---|
| **Insight:** what the evidence means | connections, contradictions and counted patterns, each with its evidence, rivals, confidence and what it means for the project | `insights/` |
| **Foresight:** what is emerging and what may come | weak signals, the three horizons, layered readings, scenarios (what holds across them, what depends on one) and dated forecasts | `foresight/` |
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

## What to ask Claude

Ask in plain language. The plugin comes in when the work is interpretation, and you can name its agents directly.

- *"What insights come out of our research library on onboarding?"*
- *"Here are 40 interview transcripts: what patterns do you see, and how sure are you?"*
- *"Here is the Google Forms export of our customer survey (responses.csv): what stands out?"*
- *"Which weak signals in these notes point to where the field is going? Give scenarios and forecasts."*
- *"Challenge this conclusion: users leave because the pricing page is confusing."*
- *"Run insight-analyst and foresight-analyst in parallel, then the challenger on both."*

## How it works

One skill, `insight`, is the entry point. It reads your research library (`research/`) or the data you give it,
collects the evidence first, then picks a **playbook**. Each playbook has an **agent** for parallel work.

| Playbook | Agent | What it does |
|---|---|---|
| insight | `insight-analyst` | lists the evidence and what was observed, fixes the comparisons in advance, then looks for connections, contradictions and counted patterns |
| foresight | `foresight-analyst` | logs signals (visibility, spread and meaning kept apart), places them on three horizons, reads the issue in four layers, builds scenarios, writes forecasts |
| challenge | `challenger` | tries to show why each conclusion is wrong: rivals, diagnostic evidence, independence, chance, sensitivity, consistency, denominators, replication |

- **Evidence before meaning.** What the input shows is collected first, each item with its reference; only then is
  it interpreted, and every conclusion points back to its items.
- **An independent challenge.** The `challenger` gets the conclusions and the data, not the reasoning that
  produced them, so it can find what the analyst missed.
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

## The rules

The same rules apply to every playbook (`skills/insight/rules.md`), each with its source:

- **Every conclusion carries** its evidence, rival explanations generated before judging, the evidence that favors
  it over the rivals, what it rests on, what would prove it wrong, and a confidence level with the reason.
- **One weighing rule, applied the same way to every rival.** Not a ritual matrix: in a controlled study the
  matrix did not improve accuracy, while consistency did.
- **Data before patterns.** Rates over what was actually observed, never over units chosen because they show the
  outcome; comparisons fixed before looking; natural replications checked first; and when the data are a tool's
  output, whether the tool could produce the pattern.
- **Hidden patterns are checked harder,** not reported sooner: independent support and a test against chance.
- **Interpretation is labelled** as interpretation, and nothing is added from memory without saying so.

## What it adds to your project

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
        insight.md            connections, contradictions, counted patterns
        foresight.md          signals, horizons, layers, scenarios, forecasts
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
- **Confidence not taken from feeling sure:** Kahneman & Klein 2009. Intuition is reliable only in regular,
  learnable settings with feedback.
- **Hidden patterns checked harder:** Whitson & Galinsky 2008, illusory pattern perception (contested by a small
  replication).
- **Weak signals (visibility, spread and meaning kept apart):** Hiltunen 2008.
- **Three horizons (H1, H2+, H2−, H3):** Sharpe et al. 2016.
- **Uncommon conclusions from deeper layers:** Inayatullah 1998, causal layered analysis.
- **Scenarios guide flexible choices, not predictions:** Phadnis et al. 2015.
- **Forecasts with probabilities and dates, scored later:** Mellers et al. 2015.

## Update or remove

```
/plugin marketplace update poiesis-insight
/plugin update poiesis-insight@poiesis-insight
/plugin uninstall poiesis-insight@poiesis-insight
```

## Changing the plugin

Edit the files under `plugins/poiesis-insight/`, run `claude plugin validate .`, bump the version in
`plugin.json`, `marketplace.json` and `CHANGELOG.md`, and push. Projects get it with the update commands above.

## License

MIT. Requires Python 3.
