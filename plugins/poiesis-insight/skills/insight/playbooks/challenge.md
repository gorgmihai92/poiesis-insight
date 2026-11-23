# Challenge

Every insight, pattern, gap, method pattern and uncommon conclusion goes through this before it is reported. The
goal is to find why it might be wrong, not to defend it. The verdict is then recorded once, with a stamp.

## Read first
- `rules.md`, and the notes behind the checks (named with each check; each note says how much of its source was
  read).
- For the stamp, the new challenge and "none found": `research/notes/poiesis-lab-2026-recorded-runs.md`, an
  observation of two runs. These three rules are product decisions built on it.
- For the sample a person checks: `research/notes/panickssery-2024-self-preference.md` and
  `research/notes/wataoka-2024-self-preference-bias.md`: both papers read in full, not the first one's
  appendixes.

(Notes are in the plugin's repository, under `research/notes/`.)

## Before
- Each conclusion is one sentence under its own heading, with its **Id** (`templates/insight.md`). One
  conclusion holds one claim: split a sentence that joins two before it is challenged.
- What is challenged is the sentence and the data, not the reasoning that led to it.

## The nine checks
For each conclusion:
1. **Rivals:** are the rival explanations complete? Add any missing, especially chance, selection (how the data were
   gathered), measurement, a confound, a single unusual source (Heuer 1999, p. 124; Nickerson 1998, p. 3).
2. **Diagnosticity:** does the evidence favor this conclusion over each rival, or would it appear under the rivals
   too? (Heuer 1999, p. 73, 129)
3. **Independence and count:** how many independent items support it? One source, one speaker, one week, or one
   vivid case is one item (Nickerson 1998, p. 9).
4. **Chance:** with this much data, how likely is a pattern like this by chance? For hidden patterns, ask what
   the data would look like if there were no pattern (Whitson & Galinsky 2008, abstract or secondary summaries only). If it came from a
   free search, how many comparisons were tried, and does it survive the correction for them? (Benjamini &
   Hochberg 1995, abstract only)
5. **Sensitivity:** remove the one to three items it rests on; does it still stand? (Heuer 1999, p. 125)
6. **Consistency:** was the same weighing rule applied to the conclusion and to its rivals? (Dhami et al. 2019, p. 6)
7. **Denominators, slices and groupings:** are rates computed over the units analyzed, not units selected by the
   outcome? Were slices and groupings fixed before looking, or does the result hold under other groupings?
   (Simmons et al. 2011, abstract only)
8. **Replication and instrument:** does it hold in another version, period, source or subset of the data, and
   what does that replication test (the tool, or the pattern)? If the data are a tool's output, could the tool
   produce it? A lead from a free search needs the hold-out: without it, the verdict is at most weakened, as a lead.
9. **Absence** (for a conclusion that says something does not exist, is missing or was never studied): what was
   searched, under which terms, and which databases answered? "Not found" is not "does not exist". The claim is
   narrowed to "none found in <where it was looked for>", and the words the field itself might use are tried
   before it is kept. (Observed: in the recorded run, "no experiment exists" became "none found".)

## Verdict
One word and one line of reason:
- **kept:** survives every check that applies; confidence stated.
- **weakened:** survives with lower confidence or as a narrower claim. The narrower claim is written out as one
  full sentence that can stand alone.
- **dropped:** a rival explains it as well or better, or it rests on one item, or chance explains it.

A conclusion with parts that deserve different verdicts is **weakened**: its narrower claim is what survives, and
each part is named with what happened to it. There is no fourth verdict (a product decision: the recorded run
had one "split").

Report kept and weakened conclusions, and list the dropped ones briefly: what was dropped teaches as much.

## Who challenges
- **Quick and standard depth:** the session, inline (`rules.md`, "Depth").
- **Thorough depth:** the `challenger` agent. It gets the conclusions, each with its id and its sentence, and the
  data. It does not get the reasoning. It answers with one block per conclusion, in the form its own file gives.
- **Save the challenger's answer as it came,** before anything else is done with it:
  `insights/challenges/<YYYY-MM-DD>-<topic>.md`. Copy it; do not tidy it or summarize it. (Observed: the answers of
  the recorded run were not saved, and the verdicts had to be transcribed from the session afterwards.)

## Record the verdict: the stamp
When the work is saved (`SKILL.md`, "Saving"):
1. **Bring the note in line with the verdicts.**
   - kept: the conclusion stays as it is. `- **Challenge:** kept · <reason>`
   - weakened: the heading becomes the narrower claim, word for word as the challenger gave it.
     `- **Challenge:** weakened · was: "<the first sentence>" · <reason>`
   - dropped: the conclusion moves under a "Dropped" heading with its sentence unchanged and its id.
     `- **Challenge:** dropped · <reason>`
   - never challenged (a lead, a conclusion added later): `- **Challenge:** not challenged`
2. **Write the stamps.** `$S` is the skill's `scripts` folder.
   - From the challenger's saved answer, so that no verdict is typed by hand. It refuses a kept or dropped
     conclusion whose heading is not the answer's Claim (or has no Claim), and a weakened one whose heading is not
     its Narrower:
     `python3 -I $S/challenge_stamp.py write --note insights/<note>.md --verdicts insights/challenges/<answer>.md --by agent`
   - After an inline challenge, one conclusion at a time:
     `python3 -I $S/challenge_stamp.py write --note insights/<note>.md --id IN-001 --verdict weakened --by inline`
3. **Verify:** `python3 -I $S/challenge_stamp.py verify --note insights/<note>.md`. Every challenged conclusion
   prints `OK`. Anything else is put right before the report goes out.

What a stamp is: one line in `insights/challenge-stamps.jsonl` with the id, the verdict, the day and a hash of
the conclusion's sentence. `verify` fails when the stamp is missing, when the sentence changed, when the verdict
shown is not the stamped one, or when the line was edited.

**A verdict is written once.** After the stamp nobody retypes, softens or upgrades it: not in the report, not in
a summary, not on a page built from the note. Wherever a verdict is shown, it is copied from
`python3 -I $S/challenge_stamp.py list`. (Observed: on the published page of the recorded run a `weakened`
verdict had become `kept` when it was retyped.)

The stamp is a seal against drift. It is not a signature: it makes a change visible and does not prevent one.
When nothing is saved there is no stamp: say "not stamped: nothing was saved".

## A new challenge
An earlier verdict no longer covers a conclusion when, after the stamp:
- **the method changed:** another base, filter, grouping, time window or version of a tool;
- **the data changed:** new rows, corrected values, another source;
- **the sentence changed:** `verify` prints `TEXT CHANGED`, even for a rewording that seems to mean the same.

Challenge it again, in full, then record the new verdict with the reason:
`python3 -I $S/challenge_stamp.py write --note insights/<note>.md --id IN-001 --verdict <verdict> --again "<what changed>"`

The earlier stamp stays in the file as history. Then run `python3 -I $S/ids.py stale`: it lists what was built on
the conclusion before the new verdict. (Observed: in the recorded run the base changed after the challenge, the
numbers on the page moved, and the first verdicts stayed on them.)

## A person checks a sample
The challenger is a model of the same family as the session that wrote the conclusions. In one study, three
models favoured summaries they had written over those of other models and of people (Panickssery et al. 2024,
p. 2). In another, models acting as judges rated answers that were familiar to them higher than people did
(Wataoka et al. 2024, p. 1, 6, 7). Those studies are about rating summaries and chat answers. They did not test
checking a claim against its source, and in the cases the second study's authors looked at, the bias was about
styles of answering more than clear factual errors (Wataoka et al. 2024, p. 7). So this step is a precaution and a product decision, not a finding: someone who is not the model looks at
a few claims.

For every saved report:
1. `python3 -I $S/sample_check.py pick insights/<report>.md` draws five lines that point to a source and adds
   them to `insights/human-checks.md`. The script draws them, not the session, so the easy ones are not chosen.
2. The person opens each source and writes `ok` or `wrong` in the row. The session never fills a result.
3. `python3 -I $S/sample_check.py score` says what the checks so far allow. Five clean checks rule out little:
   up to 45.1% of claims could still be wrong. Thirty clean checks bring that under 10% (9.5%). These are the
   script's own numbers, the exact binomial bound at 95%. The checks are judged on their total across reports,
   not report by report.
4. A claim found wrong: correct the note, challenge again the conclusions that rest on it, and stamp them with
   `--again`.

The report's "Not checked" line says whether the sample was drawn and whether a person has filled it in.
