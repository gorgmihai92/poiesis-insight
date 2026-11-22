# Insight

What the evidence means: connections, contradictions, patterns, and what they imply for the project.

## Read first
- `rules.md`.
- The notes behind this playbook, with how much of each source was read: Klein & Jarosz 2011 (abstract only),
  Nosek et al. 2018 (abstract only), Benjamini & Hochberg 1995 (abstract only), Anscombe 1973 and Gelman & Loken
  2014 (not read: written from general knowledge, unverified). The rules that rest on them say so where they are
  stated. (Notes are in the plugin's repository, under `research/notes/`.)
- When the question is what a literature does not answer, `playbooks/questions.md`; when it is how a field
  studies its subject, `playbooks/methods.md`.

## Collect
1. Say the question in one line, and what the answer will be used for.
2. **Check the notes you will build on** (the entry gate, `rules.md`, "Before building on a note"):
   `python3 -I $S/quote_gate.py research/notes --papers research/papers`. A claim whose quote is `NOT FOUND` or
   on the `WRONG PAGE` is not used until the note is corrected. A note with `NO TEXT` or `NO QUOTES` was not
   checked: its claims are used as unchecked and named under "Not checked".
3. List the evidence items from the input (one line each, with reference). For data, describe what was measured,
   how much, which part was observed (coverage, gaps), and how it was collected (selection matters). If the data
   come from a tool, name the tool and its version.
4. Before looking for patterns, write down the slices you will compare (groups, periods, versions) and any natural
   replication the data offer (rules.md, "Data before patterns").
5. If the user wants patterns nobody planned for (hidden correlations, uncommon patterns), set aside a hold-out
   before looking: a random part of the rows, a later period or another source. It is not opened until step
   "Confirm leads".

## Look for insights along three paths (Klein & Jarosz 2011, abstract only)
- **Connections:** two items that, put together, say something neither says alone (across notes, sources, data
  slices).
- **Contradictions:** items that do not fit each other or the expected picture; an anomaly is a lead.
- **Impasse:** if the question seems stuck, name the assumption that makes it stuck and test dropping it.
Also count: frequencies, rates over what was observed, differences between the slices fixed above, with the numbers.
Plot or tabulate before summarizing: one number can hide a curve, clusters or a single outlier (Anscombe 1973,
not read: from general knowledge). An outlier is checked for a data error first. Also note what the data should
show and do not.

## Explore (only with a hold-out)
On the part not set aside, search freely: pairs of variables, groups, periods, interactions. Log every comparison
tried, with its count, and expect about 1 in 20 to look significant at p < .05 by chance alone; correct for how many
were tried (false discovery rate, Benjamini & Hochberg 1995, abstract only) and report the effect size with its
uncertainty, not only the p-value. Everything found here is a **lead**, not an insight (Nosek et al. 2018,
abstract only; Gelman & Loken 2014, not read: from general knowledge).

## Confirm leads
Test each lead once, as stated before opening the hold-out, on the hold-out. A lead that holds becomes a candidate
insight and goes to the challenge; one that does not is listed as dropped. With no hold-out possible, it stays a
lead in the report and names the data that would test it.

## Write each candidate
Use `templates/insight.md`: the claim in one sentence, evidence, rivals, why this one, rests on, would be wrong if,
confidence, and "so what" for the project.
- **Id:** the next free one, from `python3 -I $S/ids.py next IN`. A number is never used twice, and a dropped
  conclusion keeps its id.
- **From:** what the candidate rests on: the ids of other objects, the names of research notes, citation keys.
  Name what shaped it, not everything that was read.

Then run every candidate through `playbooks/challenge.md`, and record each verdict with a stamp.

## Save (see SKILL.md, "Saving")
`insights/<YYYY-MM-DD>-<topic>.md`: the question, a short description of the data (for your own data, see SKILL.md),
the evidence list, the insights that survived (with their
challenge result), the leads still untested, and those dropped with the reason. With it:
`insights/challenge-stamps.jsonl` (the stamps), and at thorough depth the challenger's answer in
`insights/challenges/`.
