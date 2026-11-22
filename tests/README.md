# Tests

Tests for the scripts in `plugins/poiesis-insight/skills/insight/scripts`, for the page that describes the
challenge stamp, and for the eval cases. They need Python 3 only and never use the network.

```
python3 -I -m unittest discover -s tests
```

This folder is not part of the plugin, so it is not installed with it.

| File | What it checks |
|---|---|
| `test_challenge_stamp.py` | a verdict is written once; a changed sentence, a retyped verdict, a missing stamp and an altered line fail; the three test vectors; `stamp-format.md` against the script |
| `test_ids.py` | the next free id, the listing, and what is reported as stale when a verdict changes |
| `test_quote_gate.py` | quotes found, not found and on the wrong page; notes that could not be checked |
| `test_sample_check.py` | which lines of a report are claims, the draw and its seed, the log, and the bound |
| `test_evals.py` | the eval cases use only documented fields; one grader per recorded conclusion; the prompts are what `eval_data.py` writes |

## Fixtures
- `vectors/challenge-stamp.json`: three texts, each with the stamp it must give. The same three are in
  `stamp-format.md`.
- `fixtures/gate/`: three conclusions for the entry gate of poiesis-frontier, one kept and stamped, one dropped
  and stamped, one never challenged. The stamps were written by `challenge_stamp.py`, and a test writes them
  again and compares.
- `fixtures/trend-scan/challenge-rows.json`: six rows of the lab's published and corrected trend-scan pages, with
  only the id, the verdict shown and the restated claim, and the challenger's verdict for each. The published
  rows fail (one verdict was retyped), the corrected rows pass.
- `texts/`: a short text and three notes written for the quote tests. They are not real sources.
- `eval_data.py` writes the prompt of the trend-scan eval case from the notebook's fixtures;
  `synthetic_map.py` writes the prompt of the synthetic case from made-up data (synthetic, for the test).

## The lab notebook
Four tests also read `fixtures/` in the Poiesis Lab notebook, which is outside this repository: the stamp test on
the notebook's own two files, the check that the copied rows are still the notebook's, the check that the eval
prompts are what the notebook's numbers give, and nothing else. They look in the folder `POIESIS_LAB` names,
then in `~/Poiesis Lab`. Where neither holds the notebook they are skipped and say so; the same checks then run
on the copies in this folder.

`test_quote_gate.py` checks the quotes of `research/notes/` against the texts in `research/papers/`. Most of
those texts are not committed (closed licences), so on another machine those notes are reported as not checked.
