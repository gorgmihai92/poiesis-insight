# Questions

Research questions that come out of what a body of evidence does not answer. First each gap is described, then
the assumptions behind it are contested. A question is not a conclusion and gets no verdict. The gap it rests on
is a conclusion and gets one.

## Read first
- `rules.md` and `playbooks/challenge.md` (check 9, absence).
- `research/notes/robinson-2011-research-gaps-framework.md`: a gap described by where and why the evidence falls
  short. Read in part: the report's abstract, its framework and its limits; the journal article was not read.
- `research/notes/sandberg-2011-gap-spotting.md`: three kinds of gap. Read in part: the typology and its tables.
- `research/notes/alvesson-2011-problematization.md`: five types of assumption and six principles for contesting
  them. Read in full.
- The project's evidence table, when poiesis-research made one (`research/maps/<name>.md`, one row per study:
  population, what was varied, compared with, what was measured, setting, design, how much was read). Without
  one, the notes in `research/notes/`.

(Notes are in the plugin's repository, under `research/notes/`.)

## 1. Say what was looked at
- The question the evidence was collected for.
- How many sources, and how much of each was read. A gap found in abstracts is a gap in what the abstracts say.
- What was searched: the terms, and which databases answered (the "Coverage" line poiesis-research prints, when
  there is one).

## 2. Describe each gap (Robinson et al. 2011)
A gap has two parts.

**Where** the evidence falls short. Name only the elements that are not covered:
- **population:** who was studied, and who was not;
- **what was varied** (the intervention), and what it was **compared with**;
- **what was measured** (the outcomes);
- **setting:** where, and in what conditions.

**Why** no conclusion can be drawn: the one reason that most prevents it.
- **A. insufficient or imprecise information:** no studies, few studies, or samples too small to give a direction;
- **B. biased information:** the studies' methods or designs limit what they show (`playbooks/methods.md`);
- **C. inconsistency or unknown consistency:** results point different ways, or there is only one study;
- **D. not the right information:** another population or setting, a measure that is not the one that matters,
  or too short a time.

Two choices are made once per project and kept, because two people applying the framework split on both:
- how fine a gap is: one per question, or one per comparison;
- which reason "one study only" gets. Here: C, unknown consistency.

A gap that does not fit the five elements is written in plain words: in the framework's own pilot about two gaps
in fifteen did not fit. Reading "intervention" as "what was varied" for work outside health care is a product
decision; the framework was built for systematic reviews in health care.

## 3. Name the kind of gap, and check that kind (Sandberg & Alvesson 2011)
- **Contradictory evidence:** count the studies on each side, and say what else differs between them (wording,
  sample, country, year) before calling it a contradiction.
- **Little research**, or little evidence for a widely used idea: give the count, and what it is small against.
- **None found:** this is a claim of absence. Write "none found", say what was searched, and try the words
  another field would use for the same thing. The `prior-art` playbook of
  [poiesis-research](https://github.com/gorgmihai92/poiesis-research) does this search; suggest it once.
- **A missing perspective:** name the theory or view that is absent, and what it would change in the answer.

These four kinds come from the three modes of gap-spotting Sandberg & Alvesson found in 52 management articles:
confusion spotting (contradictory evidence), neglect spotting (split here into little research and none found,
their "overlooked area") and application spotting (a missing perspective). They are used here as words for the
claim being made, not as a finding about other fields.

## 4. The gap is a conclusion
Write each gap with `templates/insight.md`, with an id (`python3 -I $S/ids.py next IN`). Challenge it and stamp
the verdict (`playbooks/challenge.md`). A dropped gap stays in the note under "Dropped" and no question is built
on it.

## 5. Contest the assumptions behind a gap (Alvesson & Sandberg 2011)
For a gap that was kept or weakened. This step is interpretation and is labelled as such.

**Pick the texts** the gap is defined against, few and read in depth: the study that set the path, one or a few
summaries, or a few recent influential pieces. Say which were read in full.

**Ask what those texts take for granted** that makes the gap look the way it does. Go through the five types;
"none seen" is an answer.

| Type | What it is | Where to look |
|---|---|---|
| in-house | what one school of thought accepts without question | the debates among authors who cite each other |
| root metaphor | the image of the subject behind the texts | name the image, then put a confronting one beside it |
| paradigm | what counts as real, as knowledge and as method | read the texts from another view of the world; for method, `playbooks/methods.md` |
| ideology | the interests and values taken as given | take the view of someone with other interests; treat what is taken as good as a problem, or the reverse |
| field | what several schools share | what opposed schools agree on and never debate; how another field sees the subject |

Turn what the texts state as fact into an assumption that could be otherwise.

**Then, for each assumption found:**
1. Is it worth contesting: what could be learned, and is there evidence that it is shaky? Cite the evidence. Not
   every assumption is worth it.
2. Write an alternative that goes beyond positions the field already argues about.
3. Say who holds the assumption, and whether the alternative would strike them as obvious, absurd or
   interesting. Aim between obvious and absurd. Trying it on someone from that audience is the owner's step:
   say that it was not done.
4. Check that nobody has already offered the alternative ("none found", with what was searched).

Skip this step when the gap is plain and worth filling as it is, and say so: the method's own authors keep
gap-spotting as a valid route and warn against contesting everything.

## 6. Write each question
`templates/question.md`, with an id (`python3 -I $S/ids.py next QN`) and a **From** line that names the gap.
Order the questions by what an answer would change for the project, not by how interesting they sound. For a
study design, suggest [poiesis-frontier](https://github.com/gorgmihai92/poiesis-frontier) once.

## Save (see SKILL.md, "Saving")
`insights/<YYYY-MM-DD>-<topic>.md`: what was looked at, the gaps with their verdicts, the questions, and "Not
checked". When a gap's verdict changes later, `python3 -I $S/ids.py stale` lists the questions that rest on it.

## Limits
- Contesting assumptions was shown by its authors on one article in management studies. Whether it gives better
  questions than a plain gap was not tested; they write that there are "no guarantees" (Alvesson & Sandberg
  2011, p. 20). Its aim is a question worth asking, not a true statement.
- The gap framework was tried on two reports by people who had not written them, and was not compared with
  other ways of finding gaps.
