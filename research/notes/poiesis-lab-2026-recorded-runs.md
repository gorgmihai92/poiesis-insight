# Two recorded runs of the Poiesis plugins (Poiesis Lab notebook, 2026)

- **Source:** the lab notebook's `fixtures/` folder (two runs of 2026-11-17, copied there on 2026-11-21) and its plan, `lab/plan.md`. The notebook is the owner's and is not public.
- **File:** none in this repository. Six rows are copied in `tests/fixtures/trend-scan/challenge-rows.json`.
- **Licence:** the owner's own material.
- **Evidence:** observation · what happened in two runs, as the files record it. One project, one day, one model family: these are cases, not rates.
- **Read:** `fixtures/README.md`, `fixtures/challenge-verdicts.json`, `fixtures/trend-scan/challenge.published.json` and `challenge.corrected.json` in full; the structure and some values of the two runs' `analysis.json`; the list of studies inside the second run's `page.html`. Not read: the other data files, the two pages as pages. From the plan: the sections on the protocol, on poiesis-insight 2.0.0, the limits, the phases, the verification and the sources · 2026-11-22

## What the files show
- **Fifteen of sixteen first-pass conclusions did not survive as written.** The challenger kept 1, weakened 12, dropped 2 and split 1 into a dropped part and a weakened part (`challenge-verdicts.json`).
- **A verdict label drifted when it was retyped.** The published page showed conclusion `c6` as `kept`; the challenger had said `weakened` (`challenge.published.json` against `challenge-verdicts.json`; `fixtures/README.md`).
- **The method changed after the challenge and nothing was challenged again.** The page's rows come from "a second pass with an article-only base" (its own `meta` line). For `c6` the challenger's narrower claim was "about 16 percentage points, not 29"; the page says "about 18 points, not 29". The claims on the page are also reworded against the ones sent to the challenger.
- **A claim of absence was narrowed.** A sentence that no experiment varies one factor became "none found" (conclusion I4).
- **One conclusion was dropped on chance alone:** its count was within what chance would give (conclusion T5).
- **The agents' answers were not saved as files.** The verdicts were transcribed from the session four days later (`fixtures/README.md`, "Not here").
- **Each study's method was not recorded.** The plan records, as observed in the session, that every study of the second run's table used one design. The saved page lists 15 studies and gives a design for one of them. So the pattern cannot be checked from the files: what the files show is that the table had no column for method.

## What it means for the plugin
- A verdict is recorded once by a script, with a hash of the sentence, and the label shown is compared with it (`challenge_stamp.py`).
- The challenger's answer is saved as it came, and the stamps are written from that file.
- A change of method, data or wording after a challenge calls for a new challenge.
- A claim that something does not exist is written as "none found", with what was searched.
- A field's methods are tabled study by study before anything is said about the field (`playbooks/methods.md`).
- Limit: two runs. The observations say what can go wrong, not how often it does.
