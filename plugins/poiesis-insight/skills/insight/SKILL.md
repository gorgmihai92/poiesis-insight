---
name: insight
description: Interpret research or data a project already has. Two kinds of request - insight (what the evidence means, connections, contradictions, patterns, implications) and foresight (weak signals, emerging patterns, scenarios, dated forecasts, uncommon conclusions). Every conclusion points to its evidence, names its rival explanations and what would prove it wrong, and survives a challenge. Use when the user asks for insights, patterns, implications, foresight, trends, scenarios or forecasts from research or data.
---

# Insight

Research reports what sources say; this skill interprets it. Two playbooks, one challenge step for both.

| The user wants… | Playbook | Agent for parallel work | Saved in |
|---|---|---|---|
| what the evidence means: connections, contradictions, patterns, implications | `playbooks/insight.md` | `insight-analyst` | `insights/` |
| what is emerging and what may come: signals, horizons, scenarios, forecasts | `playbooks/foresight.md` | `foresight-analyst` | `foresight/` |
| every conclusion above, before it is reported | `playbooks/challenge.md` | `challenger` | (marks each one kept / weakened / dropped) |

## Every request

1. **Input:** the research library (see "From poiesis-research" below) or data the user gives (see "Your own
   data"). Read `research/research.config.md` if it exists for what the project is. If the input is thin, say so
   before interpreting it.
2. **Evidence before meaning:** first collect what the input shows, with exact references (note and page, row,
   quote, time); only then build interpretations (rules.md, "Two loops").
3. **Pick the playbook.** A request can use both (insights first, then what they suggest about the future).
4. **Challenge** every conclusion with `playbooks/challenge.md` before reporting it. Report what survived, what was
   weakened and what was dropped, and why.
5. **Follow `rules.md`**, the same for every playbook.

## From poiesis-research

What insight reads from the research plugin, if the project has it (it works without it too):
- `research/README.md`: the index; start here to see what the library holds.
- `research/notes/<section>/<slug>.md`: one note per source, with claims and pages ("What it says"), evidence kind,
  and "What it means for the project". Cite insights back to the note and page.
- `research/funding/<call-id>.md`: funding calls, if the question is about funding.
Insight never edits these files; it writes only to `insights/` and `foresight/`.

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

Scripts are in `${CLAUDE_SKILL_DIR}/scripts` (called `$S`; if that path does not exist, Glob for
`**/insight/scripts/forecasts.py` under `~/.claude`). They need only Python 3; run them with `python3 -I`.
