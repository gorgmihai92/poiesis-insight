---
name: insight
description: Interpret research or data a project already has. Insight (what the evidence means, connections, contradictions, patterns, implications), research questions (gaps described, assumptions contested) and the methods of a field. Every conclusion points to its evidence, names its rival explanations and what would prove it wrong, and survives a challenge whose verdict is recorded once. Use when the user asks for insights, patterns, implications, research questions or gaps, or how a field studies something, from research or data, or wants a conclusion challenged. Foresight (signals, trends, scenarios, forecasts) is the poiesis-foresight plugin.
---

# Insight

Research reports what sources say; this skill interprets it. Three playbooks, one challenge step for all.

| The user wants… | Playbook | Agent for parallel work | Saved in |
|---|---|---|---|
| what the evidence means: connections, contradictions, patterns, implications | `playbooks/insight.md` | `insight-analyst` | `insights/` |
| what the evidence does not answer: gaps and research questions | `playbooks/questions.md` | `insight-analyst` | `insights/` |
| how a field studies its subject, and what that lets it say | `playbooks/methods.md` | `insight-analyst` | `insights/` |
| every conclusion above, before it is reported | `playbooks/challenge.md` | `challenger` | a stamp per verdict (kept / weakened / dropped) |

## Every request

1. **Input:** the research library (see "From poiesis-research" below) or data the user gives (see "Your own
   data"). Read `research/research.config.md` if it exists for what the project is. If the input is thin, say so
   before interpreting it.
2. **Check what you build on** (the entry gate): before an insight rests on a research note, the note's quotes
   are looked for in the source's text with `quote_gate.py` (rules.md, "Before building on a note").
3. **Evidence before meaning:** first collect what the input shows, with exact references (note and page, row,
   quote, time); only then build interpretations (rules.md, "Two loops").
4. **Pick the playbook.** A request can use several (insights first, then the questions they leave open). What is
   emerging and what may come (signals, trends, scenarios, forecasts) is [poiesis-foresight](https://github.com/gorgmihai92/poiesis-foresight)'s
   `foresight` skill: suggest it once ("Other Poiesis plugins"). Each playbook starts with "Read first".
5. **Challenge** every conclusion with `playbooks/challenge.md` before reporting it, at the depth chosen (rules.md,
   "Depth"). Report what survived, what was weakened and what was dropped, and why.
6. **Record each verdict once** with `challenge_stamp.py` when the work is saved, and do not retype it afterwards.
7. **Follow `rules.md`**, the same for every playbook.

When a step has no playbook or script here, stop and say what is missing. Offer the choices: an existing step
used more narrowly, building the tool first, or leaving the step out and naming it under "Not checked".

## From poiesis-research

What insight reads from the research plugin, if the project has it (it works without it too):
- `research/README.md`: the index; start here to see what the library holds.
- `research/notes/<section>/<slug>.md`: one note per source, with claims and pages ("What it says"), quotes with
  pages ("Quotes"), how much was read (**Read**) and "What it means for the project". Cite insights back to the
  note and page.
- `research/maps/<name>.md`: an evidence table, one row per study, when one was made. The `questions` and
  `methods` playbooks start from it.
- `research/papers/`: the sources' texts, with a `[p. N]` line before each page. `quote_gate.py` reads them.
- `research/funding/<call-id>.md`: funding calls, if the question is about funding.
Insight never edits these files; it writes only to `insights/`.

## Your own data (forms, tables, documents)

1. **Convert** what Claude cannot read directly: `python3 -I $S/to_text.py <file> --out <work folder> --mask` turns
   Excel (.xlsx, .xls; one CSV per sheet), Word (.docx, .doc, .rtf, .odt) and CSV/TSV into CSV or TXT, and masks
   emails and phone numbers. A Google Forms export is already CSV. The original file is not changed.
2. **Personal data:** drop or replace columns that identify people (names, addresses, IDs, free text that names
   someone) before analysis; keep the originals and the converted files out of git and out of any public place.
3. **Describe the data first**, in a few lines at the top of the insight report: source and how it was collected
   (form, who received it, when), number of responses, which questions are optional, what is missing or empty,
   duplicates or test responses, and what each column means if it is not obvious. These are the units and
   denominators the rules ask for.

## Scripts

Scripts are in `${CLAUDE_SKILL_DIR}/scripts` (called `$S`; if that path does not exist, Glob for
`**/insight/scripts/challenge_stamp.py` under `~/.claude`). They need only Python 3 and its standard library, except `to_text.py`, which installs the Excel
and Word libraries once, on first use, into a private cache (a network request); run them with `python3 -I`,
from the project's folder. Each prints its own help with `--help`.

| Script | What it does |
|---|---|
| `quote_gate.py research/notes --papers research/papers` | the entry gate: each quote of a note looked for in the source's text |
| `ids.py next IN` · `ids.py list` · `ids.py stale` | the next free id; what rests on what; what went stale when a verdict changed. It changes nothing |
| `challenge_stamp.py write` · `verify` · `list` | record a verdict once; check a note against its stamps; the verdict in force for each conclusion |
| `sample_check.py pick <report>` · `score` | draw five claims for a person to check; what the checks so far allow |
| `to_text.py <file> --out <folder> --mask` | convert Excel, Word and CSV into CSV or TXT |

## Saving
Save the work (paths in the playbooks) when any of these holds: the depth is standard or thorough; the user asks;
the project already has the folder (`insights/`), so it keeps a record; or something must be tracked later (a verdict to
stamp, a sample for a person to check).
Otherwise (quick depth, a one-off question) answer in the chat only, and end with one line offering to save it.
Never create a folder the user did not want. A verdict is stamped only when the work is saved: in a chat-only
answer say "not stamped: nothing was saved".

## Answers
Short and direct: the answer first, then what it rests on, in bullets or a table; no preamble, no recap. When the
work is saved, the chat gets the summary, the "Not checked" line and the file's path. Use an agent
only for independent parts that can run in parallel, or for the independent check at thorough depth; otherwise
work inline. An agent's rows and verdicts are copied into the report as they came, not retyped.

## Other Poiesis plugins
This plugin works alone. Suggest another one only when it would change the result: once, in one line, and go
on without it if the user says no (say what was left out). Check with `claude plugin list`; install only after
the user agrees, with `claude plugin marketplace add gorgmihai92/<repo>` and then
`claude plugin install <plugin>@<repo>` (it works after Claude Code restarts).
Every suggestion, from the skill or an agent, gives the plugin's link (below) and names the skill or agent
to use, e.g. "[poiesis-foresight](https://github.com/gorgmihai92/poiesis-foresight), `foresight-analyst`".
- **[poiesis-research](https://github.com/gorgmihai92/poiesis-research)**: when a conclusion needs sources the project does not have, the
  evidence for a claim is thin, or "none found" needs a search under other terms (its `prior-art` playbook).
- **[poiesis-foresight](https://github.com/gorgmihai92/poiesis-foresight)**: when the user wants what is emerging and what may come: weak signals, trends in
  data, horizons, scenarios, dated forecasts (its `foresight` skill and `foresight-analyst` agent). Since 2.0.0 this
  plugin no longer does foresight.
- **[poiesis-frontier](https://github.com/gorgmihai92/poiesis-frontier)**: when the user wants what to build or try next, not only what the
  evidence means, or a study that would answer a research question; frontier starts from the insights kept here.

## Files shared with other Poiesis plugins
These paths and fields are a contract between the Poiesis plugins: rename or remove one only in a major version,
and say so in the changelog; adding fields is free. Read other plugins' files tolerantly: a missing file or field
means "unknown", said in the report, never an error.
- Writes `insights/<date>-<topic>.md`: each insight with **Id** (`IN-001`), **From**, **Evidence**,
  **Confidence**, **Found by**, **Challenge** (`kept` / `weakened` / `dropped`, or `not challenged`) and **So
  what**; each research question with **Id** (`QN-001`) and **From**. Frontier starts from kept and weakened
  insights.
- Writes `insights/challenge-stamps.jsonl`: one line per verdict, only ever appended to. Its fields, the text that
  is hashed and how another plugin verifies a stamp with its own code are in `stamp-format.md`, next to this
  file. A verdict is read from the stamp, not from the note's label; a conclusion with no stamp was
  not challenged.
- Writes `insights/challenges/<date>-<topic>.md` (the challenger's answer as it came) and
  `insights/human-checks.md` (claims drawn for a person to check, and what the person found).
- Reads `research/notes/` (poiesis-research: **Source**, **Read**, "What it says" with pages, "Quotes", "Later
  work"), `research/maps/`, `research/papers/` and `frontier/results/<id>.md` (poiesis-frontier: "What
  happened", "Against the kill criterion", **Raw data**) as your own data.
- Reads **Id** and **From** lines in the notes of `research/`, `insights/`, `frontier/`, `design/` and `foresight/`
  (the folder [poiesis-foresight](https://github.com/gorgmihai92/poiesis-foresight) writes), to list what rests on what (`ids.py`). It writes nothing
  there.
- Until 1.4.3 this plugin also wrote `foresight/<date>-<topic>.md` and `foresight/forecasts.md`. Since 2.0.0
  [poiesis-foresight](https://github.com/gorgmihai92/poiesis-foresight) writes them.
