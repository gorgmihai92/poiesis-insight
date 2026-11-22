# The challenge stamp: format 1

How poiesis-insight records a challenge verdict, and how anything that builds on a conclusion checks it. This
page is enough to verify a stamp with your own code: no Poiesis plugin needs another to be installed, so the
plugins that consume stamps (poiesis-frontier 1.2.0 and poiesis-studio 0.1.0, not released yet) are built from
this description, not from this plugin's script.

Format 1, written 2026-11-22. A change to the fields, to the text that is hashed or to the seal is a new format
number and a major version of the plugin. Everything marked **P** is a product decision.

Changed on 2026-11-22, after an independent review, without changing the format: the rules for reading a note
are stricter (an `Id` or `Challenge` line may be written without the list dash; the label passes only when its
one verdict word is the stamped one; a conclusion with no Challenge line is skipped only when it is a research
question), the script escapes everything outside ASCII when it writes a line, and lines are split at line feeds
only. Stamps written before still verify.

## In short

After the challenge, the main session records each verdict once, as one line in a file. The line holds the
conclusion's id, the verdict, the date and a hash of the conclusion's sentence. Whoever builds on a conclusion
looks up its line and checks three things: the line is intact, the sentence is still the one that was challenged,
and the verdict shown next to the sentence is the recorded one.

## Where a stamp lives (P)

`insights/challenge-stamps.jsonl`, relative to the project's root. One stamp per line, as JSON. UTF-8, lines end
with a line feed, and a line is split there only: the script writes every character outside ASCII as a `\u`
escape, so no character inside a field (U+2028, for one) can end a line.

- The file is only ever appended to. A line is meant never to be edited or removed: the seal shows an edit, and
  nothing but the file's git history shows a removed line (see the end of this page).
- **The last line for an id is its stamp in force.** Earlier lines for the same id are the history: a conclusion
  that was challenged again has more than one line.
- Stamps for every kind of object go in this one file, whatever folder the object's note is in.
- Why a separate file and not a line in the note: the label in the note is what drifted in the recorded run, so
  the record is kept apart from the label and the two are compared. Why JSON Lines and not a Markdown table: a
  table cell cannot hold `|`, and Obsidian does not show a `.jsonl` file, so nobody edits it by accident.

## Fields

```json
{"v": 1, "id": "IN-004", "verdict": "weakened", "date": "2026-11-22", "text_sha256": "c54c859e8f85c160dac9ba94d4066d6a8eec8686ced2d25c485c08fc24acb95c", "seal": "3fe815f110e58f56a0c527f53ad71cbc3e34291bb547d15859f92f6e8c110cc5", "by": "agent", "where": "insights/2026-11-22-trends.md"}
```

| Field | Required | Value |
|---|---|---|
| `v` | yes | written `1` in the line (the script rejects `true` and `1.0`; a reader whose JSON parser cannot tell `1.0` from `1` may check the raw text) |
| `id` | yes | the conclusion's id, exactly as in the note: a letter or digit, then up to 63 letters, digits, `.`, `_` or `-`. Compared as typed: `c6` is not `C6` |
| `verdict` | yes | `kept`, `weakened` or `dropped`, in lower case. Nothing else |
| `date` | yes | the day of the challenge, `YYYY-MM-DD` in ASCII digits and a real date, local time. It is not checked against today: a date in the future is accepted |
| `text_sha256` | yes | 64 lower-case hexadecimal digits: the hash of the sentence (next section) |
| `seal` | yes | 64 lower-case hexadecimal digits: the hash of the other four (section "The seal") |
| `by` | no | `agent` (the `challenger` agent gave the verdict) or `inline` (the session challenged its own conclusion) |
| `again` | no | on a later stamp for the same id: why the conclusion was challenged again |
| `where` | no | the note's path as the writer saw it. A hint, and it goes stale when a note is renamed |

`by`, `again` and `where` are not covered by the seal. Ignore any field you do not know: adding one is not a
format change.

## Which text is hashed, and how it is normalised

**The text is the conclusion's sentence as it stands after the challenge.** For a kept or a dropped conclusion
that is the claim that was challenged. For a weakened one it is the narrower claim the challenger gave, which
replaces the first claim in the note.

In a note the sentence is the **heading** above the conclusion's `Id` line (section "Reading a note"). Only the
heading is hashed: not the evidence, the rivals or the confidence under it.

Normalise, then hash:

1. Take the text as Unicode characters. A byte-order mark at the start of a file is not part of it.
2. Apply Unicode normalisation form **NFC**.
3. Replace every run of these six characters with one space (U+0020): tab U+0009, line feed U+000A, vertical tab
   U+000B, form feed U+000C, carriage return U+000D, space U+0020.
4. Remove the spaces (U+0020) at the start and at the end.
5. Encode as UTF-8 and take the SHA-256. Write it as 64 lower-case hexadecimal digits.

Nothing else is folded. Capitals, punctuation, straight and curly quotes, `-` and `–`, Markdown marks such as
`**`, and the no-break space U+00A0 all stay as typed, so changing any of them changes the hash.

```python
import hashlib, re, unicodedata

def text_sha256(text):
    text = unicodedata.normalize("NFC", text)
    text = re.sub("[\t\n\x0b\x0c\r ]+", " ", text).strip(" ")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
```

```js
import { createHash } from 'node:crypto';

const textSha256 = (text) =>
  createHash('sha256')
    .update(text.normalize('NFC').replace(/[\t\n\v\f\r ]+/g, ' ').replace(/^ +| +$/g, ''), 'utf8')
    .digest('hex');
```

Do not use `\s` for step 3: it matches different characters in Python and in JavaScript.

## The seal

The seal shows that a line was not edited by hand after it was written. It is the SHA-256, as 64 lower-case
hexadecimal digits, of the UTF-8 bytes of these five lines joined by a line feed (U+000A), with no line feed
after the last:

```
poiesis-challenge-stamp v1
<id>
<verdict>
<date>
<text_sha256>
```

```python
def seal(id_, verdict, date, text_sha256):
    lines = ["poiesis-challenge-stamp v1", id_, verdict, date, text_sha256]
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()
```

The seal is a guard against drift and retyping, not a signature. Whoever can run the script can write a new
stamp, so the seal makes a change visible and does not prevent one.

## Reading a note

A conclusion in a Markdown note is a heading with an `Id` line under it:

```markdown
### Slow growth, with no detectable change in rate.

- **Id:** IN-004
- **Challenge:** weakened · the two growth rates differ by about one standard error
```

- Split the note at line feeds only, and drop a carriage return before one.
- Skip the lines of fenced code blocks: a line that starts with three or more backticks or tildes (after spaces
  or tabs) opens one, and it is closed only by a line of the same character, at least as many, and nothing
  else after them.
- **A heading** is a line matching `^#{1,6}[ \t]+(.*)$`. The sentence is group 1, taken whole and then
  normalised. A block runs from a heading to the line before the next heading of any level.
- **The id** is on the first line of the block matching, without regard to case,
  `^[ \t]*(?:[-*+][ \t]+(?:\*\*)?|\*\*)id(?:\*\*)?[ \t]*:(?:\*\*)?[ \t]*(\S+)[ \t]*$`. A block with no such line is not an object.
- **The label shown** is on the first line of the block matching, without regard to case,
  `^[ \t]*(?:[-*+][ \t]+(?:[*_]{1,2})?|[*_]{1,2})challenge[a-z ]*?(?:[*_]{1,2})?[ \t]*(?::(?:[*_]{1,2})?|(?:[*_]{1,2})?:|[*_]{2}[ \t])[ \t]*(.*)$` (`Challenge`, `Challenged`, `Challenge result`,
  after a list dash or bold or `_` marks; a plain line that only starts with "Challenge:" is prose). Take group 1
  up to its first `·`, and find in it every whole word `kept`, `weakened` or `dropped`, without regard to case. If
  it holds one and also a word of negation (`not`, `no`, `never`, or a word starting with `un`), it holds no
  verdict. `**Kept** · …` gives {kept}; `weakened → kept after review` gives {weakened, kept};
  `not challenged` gives nothing.
- An id under two headings is an error: neither can be verified.
- Insight writes its conclusions in `insights/<date>-<topic>.md`. To find a conclusion by id, read the notes in
  `insights/`; `where` may save the search.

## How to verify one conclusion

Read the file and keep, for the id, its **last** line. Then, in this order:

| Step | Check | If it fails |
|---|---|---|
| 1 | every non-empty line of the file is a JSON object with an `id` of the form under "Fields" | the file is damaged (a merge conflict, a cut line): nothing in it can be trusted to be the last word on any id |
| 2 | the id has a line | **no stamp**: the conclusion was never challenged |
| 3 | the last line for the id has `v` equal to 1, a verdict among the three, a date, a 64-digit `text_sha256`, and a `seal` equal to the one you compute | **stamp altered**. Do not fall back to an earlier line for the id: it may be a verdict that was since replaced |
| 4 | `text_sha256` equals the hash of the sentence as it stands now | **text changed**: the sentence is not the one that was challenged |
| 5 | if the block has a label, the verdict words in it are exactly one, and it is `verdict` | **verdict retyped**: the label drifted, says two verdicts, or says none (such as "not challenged" on a stamped conclusion). The stamp is the record, not the label |

`verify` only says whether the record is intact. A dropped conclusion with an intact stamp verifies; what a
dropped verdict means for your object is your gate's decision.

How the two plugins that consume stamps can read them. Each gate is its own plugin's to decide:

- **Frontier.** `kept` or `weakened` with steps 1 to 4 passing: the id is in order. `dropped` with steps 1 to 4
  passing: stop. No stamp: provisional. Stamp altered, text changed or file damaged: the conclusion as it stands
  was not challenged, so provisional, with the reason.
- **Studio's report.** Show `verdict` from the stamp, never the note's label. No stamp, stamp altered or text
  changed: show "not challenged", with the reason where there is one.

## Command lines

`$S` is the skill's `scripts` folder. Run from the project's root, or pass `--stamps PATH`.

```
python3 -I $S/challenge_stamp.py write  --note insights/<file>.md --id IN-004 --verdict weakened [--by agent|inline]
python3 -I $S/challenge_stamp.py write  --note insights/<file>.md --verdicts <the challenger's saved answer>.md
python3 -I $S/challenge_stamp.py write  --id IN-004 --verdict weakened (--text "…" | --text-file FILE)
python3 -I $S/challenge_stamp.py write  … --again "why it was challenged again"
python3 -I $S/challenge_stamp.py verify --note insights/<file>.md [--id IN-004 …]
python3 -I $S/challenge_stamp.py verify --id IN-004 (--text "…" | --text-file FILE) [--verdict weakened]
python3 -I $S/challenge_stamp.py list
```

`--date YYYY-MM-DD` on `write` sets the day of the challenge (default: today). `--stamps PATH` on every command
names another stamp file.

| Exit code | `write` | `verify` | `list` |
|---|---|---|---|
| 0 | the stamp was appended | everything checked is in order | every line is intact |
| 1 | refused, and nothing was written: the id already has a stamp and `--again` was not given; the verdict is not one of the three; the id is not in the note or is there twice; the stamp file is damaged | at least one conclusion does not verify | a line is altered or damaged |
| 2 | a wrong command line, or a file that cannot be read | the same | the same |

What `verify` prints, one line per conclusion and a count at the end. The first words are fixed:

```
OK IN-004 weakened 2026-11-22
NO STAMP IN-009: no challenge is recorded
TEXT CHANGED IN-004: the sentence is not the one stamped weakened on 2026-11-22. Challenge it again
VERDICT RETYPED IN-004: shown "kept", stamped weakened on 2026-11-22
STAMP ALTERED IN-004: line 1 of insights/challenge-stamps.jsonl does not match its seal: it was changed after it was written
NOT IN NOTE IN-404: insights/x.md has no conclusion with this id
SKIPPED QN-001: a research question with no Challenge line and no stamp; questions are not stamped
2 checked: 1 in order, 1 not.
```

With `--note` and no `--id`, a research question (`QN-…`) with no `Challenge` line and no stamp is skipped and
does not count. Any other object with no stamp is `NO STAMP`, with a Challenge line or without one. A note that
holds only research questions gives `0 checked`, exit code 0. A note in which nothing at all can be read fails:
`Nothing checked: … Nothing verifies.`, exit code 1.

## A worked example

Run on 2026-11-22 in an empty folder holding `insights/2026-11-22-trends.md` with the conclusion shown under
"Reading a note". The output is copied, not retyped.

```
$ python3 -I $S/challenge_stamp.py write --note insights/2026-11-22-trends.md --id IN-004 --verdict weakened --by agent --date 2026-11-22
STAMPED IN-004 weakened 2026-11-22 c54c859e8f85
Saved: insights/challenge-stamps.jsonl
[exit 0]

$ cat insights/challenge-stamps.jsonl
{"v": 1, "id": "IN-004", "verdict": "weakened", "date": "2026-11-22", "text_sha256": "c54c859e8f85c160dac9ba94d4066d6a8eec8686ced2d25c485c08fc24acb95c", "seal": "3fe815f110e58f56a0c527f53ad71cbc3e34291bb547d15859f92f6e8c110cc5", "by": "agent", "where": "insights/2026-11-22-trends.md"}

$ python3 -I $S/challenge_stamp.py verify --note insights/2026-11-22-trends.md
OK IN-004 weakened 2026-11-22
1 checked: 1 in order, 0 not.
[exit 0]
```

By hand: the heading is `Slow growth, with no detectable change in rate.` (47 bytes in UTF-8), and its SHA-256 is
`c54c859e…b95c`. The seal is the SHA-256 of
`poiesis-challenge-stamp v1\nIN-004\nweakened\n2026-11-22\nc54c859e…b95c`.

A second verdict for the same id is refused:

```
$ python3 -I $S/challenge_stamp.py write --note insights/2026-11-22-trends.md --id IN-004 --verdict kept --date 2026-11-22
REFUSED IN-004 already has a stamp (weakened, 2026-11-22). A verdict is written once. To record a new challenge, pass --again with the reason.
[exit 1]
```

The label in the note retyped from `weakened` to `kept`:

```
$ python3 -I $S/challenge_stamp.py verify --note insights/2026-11-22-trends.md
VERDICT RETYPED IN-004: shown "kept", stamped weakened on 2026-11-22
1 checked: 0 in order, 1 not.
[exit 1]
```

The label put back, and the heading changed to "Slow growth, with a modest acceleration.":

```
$ python3 -I $S/challenge_stamp.py verify --note insights/2026-11-22-trends.md
TEXT CHANGED IN-004: the sentence is not the one stamped weakened on 2026-11-22. Challenge it again
1 checked: 0 in order, 1 not.
[exit 1]
```

## Three test vectors

Also as JSON, with the texts escaped character by character, in `tests/vectors/challenge-stamp.json` of the
plugin's repository. Each was checked three ways on 2026-11-22: with the script, with `shasum -a 256` on the normalised text typed by hand, and with the JavaScript
above in Node 24.

**1. Plain: one line, with an en dash and a per cent sign that stay as typed**

- id `IN-001`, verdict `kept`, date `2026-11-22`
- text: `Machines, AI and robots is the fastest-growing major area of moral research. Its share of the universe went from 0.4% (2015) to 6.9% (2025), growing about 20% a year in 2020–25, down from about 46% in 2015–20.`
  (the two dashes are U+2013; 213 bytes in UTF-8)

```json
{"v": 1, "id": "IN-001", "verdict": "kept", "date": "2026-11-22", "text_sha256": "455c151ffde4f720c2f17a2b42f0dd0b46a60d725abcb10cf267a84a1368c31c", "seal": "ba58912e7b2f843f530cf374b5b959123e9363d221c07d8d96d69ce1ec22bcbf"}
```

**2. Layout and accents: wrapped lines, a tab, double spaces, a carriage return, and letters typed as a base
letter plus a combining mark**

- id `IN-002`, verdict `weakened`, date `2026-11-22`
- text as found, written as a JSON string:
  `"  Studiile despre vină folosesc aproape numai viniete,\r\n  nu măsurători\tale comportamentului:  un tipar de metodă, nu o concluzie despre oameni. "`
- text after normalising (142 bytes in UTF-8):
  `Studiile despre vină folosesc aproape numai viniete, nu măsurători ale comportamentului: un tipar de metodă, nu o concluzie despre oameni.`
  The sentence is test input, not a finding.

```json
{"v": 1, "id": "IN-002", "verdict": "weakened", "date": "2026-11-22", "text_sha256": "1fd56d068a53325003345415dc4f543c9becf658587fe9a39c6ea7ad92cddcf7", "seal": "26364cd21ce3c162adba549468b49f9748eaf190e242c97870bde6dc0fd57a38"}
```

**3. From a note: the sentence is the heading above the `Id` line**

- id `IN-003`, verdict `dropped`, date `2026-11-22`
- the note:

  ```markdown
  ## Dropped

  ### Politics and polarization is a "neglected" topic.

  - **Id:** IN-003
  - **Challenge:** dropped · 5 of 88 against an expected 3.5 is within chance
  ```
- text: `Politics and polarization is a "neglected" topic.` (straight quotes; 49 bytes in UTF-8)

```json
{"v": 1, "id": "IN-003", "verdict": "dropped", "date": "2026-11-22", "text_sha256": "67b9ccd455c43ccaccca975356b643f5486519c0de7411c14ba4ce7c3baf6748", "seal": "27eb4fddaea15a7b8a06445de16650487dcdac80192ce8a023a9d2a4cec4ca45"}
```

## Three stamped conclusions for the gate test

In `tests/fixtures/gate/` of the plugin's repository:

```
insights/2026-11-17-gate-example.md     three conclusions
insights/challenge-stamps.jsonl         two stamps, written by challenge_stamp.py
```

| Id | Verdict | Stamp | `verify` says |
|---|---|---|---|
| `IN-001` | kept | yes, 2026-11-17 | `OK IN-001 kept 2026-11-17` |
| `IN-002` | dropped | yes, 2026-11-17 | `OK IN-002 dropped 2026-11-17` |
| `IN-003` | none: never challenged | no | `NO STAMP IN-003: no challenge is recorded` |

`IN-001` and `IN-002` are T1 and T5 of the lab's recorded run (`fixtures/challenge-verdicts.json` in the
notebook), with the challenger's verdicts. `IN-003` is a finding of a second pass that no challenge covers. The
sentence of `IN-001` is the text of vector 1, so its `text_sha256` is the same and its seal differs with the date.

## Related

- **Ids and `From`.** `- **Id:** IN-001` and `- **From:** IN-001, QN-002, some-note`, each one line under the
  object's heading. `ids.py stale` reads those lines and the stamps, and lists the objects whose sources were
  dropped, weakened or challenged again after they were written.
- **A research question (`QN-001`) is not stamped.** It names the gap it rests on in `From`, and the gap is a
  conclusion with a stamp.
- **A split verdict.** A stamp has three verdicts and no fourth: a conclusion with parts is recorded as
  `weakened`, and its sentence becomes what survives (**P**).
- There is no hook. Nothing runs `verify` by itself.
- **What a stamp cannot show.** Nothing links one line to the next, so a removed last line for an id brings
  the earlier verdict back unseen, and a line lost in a merge is not detected. Keep the stamp file in git, where
  a removed line shows in the history. A research question is refused by `write`: stamp the gap it rests on.
