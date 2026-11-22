# Rules (every playbook)

## Depth
Some rules hold at every depth; the rest are defaults, scaled to what is at stake. The user picks the depth, or the
project sets it with a `Depth:` line in its `CLAUDE.md` (read in every session, by every Poiesis plugin);
otherwise **standard**.
- **Always:** evidence items with their references; interpretation labelled as interpretation; rates over the units
  analyzed; rivals named for every conclusion; a free search only with a hold-out (otherwise what it finds stays a
  lead); nothing from memory unmarked; "none found" where something was looked for and not found, never "does not
  exist"; a verdict that is saved is stamped and is not retyped afterwards.
- **Quick:** planned comparisons only; each conclusion checked inline for rivals and chance (challenge checks 1 and
  4), and for absence when it says something does not exist (check 9).
- **Standard:** the notes checked before they are built on (the entry gate); the full challenge, all nine checks,
  inline; for a saved report, five claims drawn for a person to check.
- **Thorough:** the same, with the challenge by the independent `challenger` agent, given the conclusions and the
  data but not the reasoning, its answer saved as it came and the stamps written from it; a free search with a
  hold-out when patterns nobody planned for are wanted.

A default may be skipped at any depth if the report says which one and why. Every report ends with **Not
checked:** what was skipped, or "nothing". These rules limit what is reported as true, never what may be explored.

## Two loops
Collect the evidence first (what the input shows, each item with its reference), then make sense of it (schemas,
hypotheses, conclusions), and go back to the evidence when a hypothesis needs it. Every conclusion points back to
its evidence items. (Pirolli & Card 2005, abstract only)

## Every conclusion carries
- **Evidence:** the items it rests on, each with its reference. A single memorable case is not a pattern: count
  cases (Nickerson 1998, p. 9).
- **Rivals:** the other explanations, generated before judging, including the boring ones (chance, selection,
  measurement, a confound, reverse cause, regression to the mean (Barnett et al. 2005, not read: from general knowledge), a pattern that reverses
  inside subgroups (Simpson 1951, abstract only)). People generate too few hypotheses and then see the data through the first one
  (Heuer 1999, p. 124; Nickerson 1998, p. 3).
- **Why this one:** the diagnostic evidence, that is the items that favor this explanation over its rivals.
  Evidence consistent with every rival does not count (Heuer 1999, p. 73, 129).
- **Rests on:** the one to three items the conclusion would fall without (Heuer 1999, p. 125).
- **Would be wrong if:** what observation would disprove it, and what to watch for (Heuer 1999, p. 125).
- **Confidence:** high / medium / low, with the reason. Not from how convincing it feels: intuition is reliable
  only in regular, learnable environments with feedback (Kahneman & Klein 2009, abstract only).

## Weighing
- One rule for weighing evidence, applied the same way to every rival. Analysts who applied their rule
  consistently were right 80% of the time vs 31% (Dhami et al. 2019, p. 6). Do not run the full matrix procedure
  as a ritual: it did not improve accuracy and produced more ties (same, p. 1, 6).
- Say which explanation is more likely and why, or say plainly that the evidence cannot separate them.

## Data before patterns
- **Coverage and denominators:** say what part of the material was observed (which units, contiguous or not) and
  compare rates over what was observed, never raw counts across unequal coverage. The denominator is the units
  analyzed, never units selected because they show the outcome (e.g. "minutes with at least one mark"); if the data
  do not list the analyzed units, say so and ask for them.
- **Slices fixed in advance:** choose groups, periods and comparisons before looking for the pattern, and report
  every slice tried, not only the one that showed something (Simmons et al. 2011, abstract only); a free search is allowed only with a hold-out (see
  "Hidden patterns").
- **Natural replications first:** if the data have another version, period, source or subset, check the pattern
  there before reporting it. A pattern that holds in one only is a lead, not an insight. Know what a replication
  tests: the same material re-measured by a changed tool tests robustness to the tool; new material tests the
  pattern; independent (e.g. human) measurement tests the tool.
- **Groupings:** when categories are grouped (e.g. several labels into one family), fix the grouping in advance or
  show the result holds under a broader and a narrower grouping.
- **Instrument or subject:** when the data are the output of a tool (a model's labels, a survey instrument, a
  classifier), say whether a pattern could come from the tool rather than from what it measures; a change in the
  tool that moves the pattern means the tool explains it at least in part.
- Repeats of one item by one source count once.

## Hidden patterns and uncommon conclusions
- These are where illusory patterns appear (Whitson & Galinsky 2008, abstract only; contested by a small
  replication). A pattern
  is reported only with independent support (more than one source or data slice) and after asking whether chance or
  the way the data were collected would produce it.
- Uncommon is a reason to check harder, not a reason to report.
- Searching freely is allowed only with a hold-out set aside first: what the search finds is a lead until it holds
  on data that were not searched (Nosek et al. 2018, abstract only). Report how many comparisons were tried, and
  correct for them (Benjamini & Hochberg 1995, abstract only).

## Separation of roles
- Interpretation is labelled as interpretation: "the notes say" vs "this suggests".
- Facts come from the input; nothing is added from memory without marking it "from general knowledge, unverified".

## Before building on a note
Each plugin checks what it is given, so that none needs another to be installed. Before an insight is built on a
research note, each quote in the note is looked for in the source's text:
`python3 -I $S/quote_gate.py research/notes --papers research/papers`.
- `FOUND`: the words are in the source, on the page the note gives. That shows the words are there. It does not
  show that a claim built on them follows.
- `NOT FOUND`, `WRONG PAGE`: the claim is not used until the note is corrected.
- `NO TEXT`, `NO QUOTES`: nothing was checked. The note's claims are used as unchecked, with how much of the source
  the note says was read, and the note is named under "Not checked".
- In a Texere vault, a line the owner annotated, such as `#claim text [@key, p. N]`, counts as checked by a
  person. Cite it the same way and do not edit the owner's notes.
(A product decision of the lab's protocol. Observed in the recorded runs: rules of this kind existed and nothing
applied them.)

## Ids and From
- Every saved conclusion and question carries an id on its own line under its heading: `- **Id:** IN-001` for an
  insight, `- **Id:** QN-001` for a research question. `python3 -I $S/ids.py next IN` gives the next free one.
  Numbers run across the whole project and are never used twice; a dropped conclusion keeps its id.
- `- **From:**` names what the object rests on: ids of other objects, names of research notes, citation keys,
  separated by commas. It names what shaped the object, not everything that was read: having used a source does
  not make the result a derivation of it (W3C PROV-DM 2013, section 2.1.2; the note says which sections were
  read).
- An object is **stale** when something in its From was dropped, weakened or challenged again after the object
  was written. `python3 -I $S/ids.py stale` lists stale objects and changes nothing. What to do with each is
  decided by a person or in the next session: challenge it again, rewrite it, or leave it and say so.
- A conclusion whose sentence changes is another version of it, and the earlier verdict does not cover it.
(Product decisions of the lab's protocol; PROV-DM supplies the words, not the rule on staleness.)

## A verdict is written once
The challenge step records each verdict with `challenge_stamp.py` (`playbooks/challenge.md`). Nothing after it
retypes, softens or upgrades a verdict. Where a verdict is shown, it is copied from the stamp, and a conclusion
with no stamp is shown as not challenged. (Observed in a recorded run: a `weakened` verdict became `kept` when
it was retyped.)

## Not found is not does not exist
A search that returns nothing shows that nothing was found where it looked. Say what was searched, under which
terms, and which databases answered; write "none found", and try the words another field would use. (Observed in
a recorded run: "no experiment exists" had to become "none found".)

## How much of each source was read
A rule names its source, and the source's note says how much of it was read. Where a source was read only as an
abstract, or not read at all, the rule says so in its brackets. Sources with page numbers were read in the pages
given. Notes are in the plugin's repository, under `research/notes/`.
