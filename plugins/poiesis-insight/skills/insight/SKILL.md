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

1. **Input:** the project's research library (`research/notes`, `research/README.md`, via the research plugin) or
   data the user gives (tables, transcripts, interviews, logs). Read `research/research.config.md` if it exists for
   what the project is. If the input is thin, say so before interpreting it.
2. **Evidence before meaning:** first collect what the input shows, with exact references (note and page, row,
   quote, time); only then build interpretations (rules.md, "Two loops").
3. **Pick the playbook.** A request can use both (insights first, then what they suggest about the future).
4. **Challenge** every conclusion with `playbooks/challenge.md` before reporting it. Report what survived, what was
   weakened and what was dropped, and why.
5. **Follow `rules.md`**, the same for every playbook.

Scripts are in `${CLAUDE_SKILL_DIR}/scripts` (if that path does not exist, Glob for
`**/insight/scripts/forecasts.py` under `~/.claude`). They need only Python 3; run them with `python3 -I`.
