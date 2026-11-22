"""The challenge stamp: a verdict is recorded once, and a changed sentence, a retyped verdict, a missing stamp or
an altered line fails."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import tempfile
import unicodedata
import unittest
from pathlib import Path

import helpers

stamp = helpers.load("challenge_stamp")

VECTORS = json.loads((helpers.TESTS / "vectors" / "challenge-stamp.json").read_text(encoding="utf-8"))
GATE = helpers.TESTS / "fixtures" / "gate"
ROWS = helpers.TESTS / "fixtures" / "trend-scan" / "challenge-rows.json"
NOTE = """# A report

## Kept

### Slow growth, with no detectable change in rate.

- **Id:** IN-001
- **Evidence:** the two five-year growth rates differ by about one standard error
- **Challenge:** weakened · the difference cannot be told apart from chance

### The share rose in five countries.

- **Id:** IN-002
- **Challenge:** not challenged

## Questions

### Does the rise hold on a base of articles only?

- **Id:** QN-001
- **From:** IN-002
"""


def by_the_description(text: str, id_: str, verdict: str, date: str) -> tuple[str, str]:
    """The hash and the seal, computed here from the format note's words and not with the script."""
    text = unicodedata.normalize("NFC", text)
    text = re.sub("[\t\n\x0b\x0c\r ]+", " ", text).strip(" ")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    sealed = "\n".join(["poiesis-challenge-stamp v1", id_, verdict, date, digest])
    return digest, hashlib.sha256(sealed.encode("utf-8")).hexdigest()


class Folder(unittest.TestCase):
    """A scratch project folder with a note in `insights/`."""

    def setUp(self):
        self.folder = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.folder, ignore_errors=True)
        (self.folder / "insights").mkdir()
        self.note = self.folder / "insights" / "2026-11-22-report.md"
        self.note.write_text(NOTE, encoding="utf-8")
        self.stamps = self.folder / "insights" / "challenge-stamps.jsonl"

    def run_stamp(self, *args):
        return helpers.run("challenge_stamp.py", *args, cwd=self.folder)

    def write(self, *args):
        return self.run_stamp("write", "--date", "2026-11-22", *args)

    def lines(self):
        return [json.loads(line) for line in self.stamps.read_text(encoding="utf-8").splitlines()]


class Normalising(unittest.TestCase):
    def test_layout_does_not_change_the_hash(self):
        plain = "Slow growth, with no detectable change in rate."
        for other in ("  Slow growth, with no\n  detectable change\tin rate.  ",
                      "Slow growth,  with no detectable change in rate.\r\n",
                      "Slow growth, with no\x0bdetectable change\x0cin rate."):
            self.assertEqual(stamp.text_hash(other), stamp.text_hash(plain), other)

    def test_a_letter_typed_as_base_plus_mark_hashes_like_the_single_letter(self):
        self.assertEqual(stamp.text_hash("vină"), stamp.text_hash("vină"))

    def test_words_capitals_punctuation_and_dashes_are_not_folded(self):
        plain = stamp.text_hash("Growth in 2024-25 was slow.")
        for other in ("Growth in 2024–25 was slow.",      # an en dash is another character
                      "growth in 2024-25 was slow.",
                      "Growth in 2024-25 was slow",
                      "Growth in 2024-25 was slow.",        # a no-break space is not folded
                      "Growth in 2024-25 was not slow."):
            self.assertNotEqual(stamp.text_hash(other), plain, other)

    def test_the_hash_is_of_the_utf8_bytes(self):
        self.assertEqual(stamp.text_hash("  café  "), hashlib.sha256("café".encode("utf-8")).hexdigest())


class Vectors(unittest.TestCase):
    """The three vectors of stamp-format.md."""

    def test_each_vector_gives_the_stamp_the_note_expects(self):
        self.assertEqual(len(VECTORS["vectors"]), 3)
        for vector in VECTORS["vectors"]:
            with self.subTest(vector["id"]):
                made = stamp.make_stamp(vector["id"], vector["verdict"], vector["date"], vector["text"])
                self.assertEqual(made, vector["stamp"])
                self.assertEqual(stamp.normalise(vector["text"]), vector["normalised"])

    def test_the_vectors_follow_from_the_description_alone(self):
        for vector in VECTORS["vectors"]:
            with self.subTest(vector["id"]):
                digest, sealed = by_the_description(vector["text"], vector["id"], vector["verdict"], vector["date"])
                self.assertEqual(digest, vector["stamp"]["text_sha256"])
                self.assertEqual(sealed, vector["stamp"]["seal"])

    def test_the_three_vectors_cover_the_three_verdicts(self):
        self.assertEqual(sorted(v["verdict"] for v in VECTORS["vectors"]), ["dropped", "kept", "weakened"])

    def test_the_third_vector_is_read_from_its_note(self):
        vector = VECTORS["vectors"][2]
        found, twice = stamp.conclusions(vector["note"])
        self.assertEqual(found[vector["id"]]["text"], vector["text"])
        self.assertEqual(found[vector["id"]]["shown"], {"dropped"})
        self.assertEqual(twice, [])

    def test_the_command_writes_the_same_line(self):
        with tempfile.TemporaryDirectory() as folder:
            for vector in VECTORS["vectors"]:
                helpers.run("challenge_stamp.py", "write", "--id", vector["id"], "--verdict", vector["verdict"],
                            "--text", vector["text"], "--date", vector["date"], cwd=folder)
            written = (Path(folder) / "insights" / "challenge-stamps.jsonl").read_text(encoding="utf-8")
        self.assertEqual([json.loads(line) for line in written.splitlines()],
                         [vector["stamp"] for vector in VECTORS["vectors"]])


class TheFormatPage(unittest.TestCase):
    """`stamp-format.md` is what other plugins verify from, so it has to say what the script does."""

    PAGE = (helpers.SKILL / "stamp-format.md").read_text(encoding="utf-8")

    def test_it_shows_each_vectors_stamp_as_the_script_writes_it(self):
        for vector in VECTORS["vectors"]:
            self.assertIn(stamp.stamp_line(vector["stamp"]), self.PAGE, vector["id"])

    def test_its_python_gives_the_scripts_hash_and_seal(self):
        blocks = re.findall(r"```python\n(.*?)```", self.PAGE, re.S)
        scope: dict = {}
        exec(blocks[0] + blocks[1], scope)      # the two snippets of the page, as a reader would paste them
        for vector in VECTORS["vectors"]:
            digest = scope["text_sha256"](vector["text"])
            self.assertEqual(digest, vector["stamp"]["text_sha256"])
            self.assertEqual(scope["seal"](vector["id"], vector["verdict"], vector["date"], digest),
                             vector["stamp"]["seal"])

    def test_the_patterns_it_gives_are_the_scripts(self):
        for pattern in (stamp.HEADING_RE, stamp.ID_LINE_RE, stamp.CHALLENGE_LINE_RE):
            self.assertIn("`" + pattern.pattern + "`", self.PAGE)
        self.assertIn(stamp.SEAL_HEAD, self.PAGE)
        self.assertIn("`" + stamp.DEFAULT_STAMPS + "`", self.PAGE)

    def test_its_example_lines_are_what_verify_prints(self):
        for line in ("OK IN-004 weakened 2026-11-22", "NO STAMP IN-009: no challenge is recorded",
                     'VERDICT RETYPED IN-004: shown "kept", stamped weakened on 2026-11-22',
                     "TEXT CHANGED IN-004: the sentence is not the one stamped weakened on 2026-11-22. Challenge it again"):
            self.assertIn(line, self.PAGE)


class Writing(Folder):
    def test_a_stamp_holds_the_id_the_verdict_the_date_and_the_hash_of_the_heading(self):
        done = self.write("--note", self.note, "--id", "IN-001", "--verdict", "weakened", "--by", "agent")
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        (line,) = self.lines()
        self.assertEqual((line["v"], line["id"], line["verdict"], line["date"]), (1, "IN-001", "weakened", "2026-11-22"))
        self.assertEqual(line["text_sha256"], stamp.text_hash("Slow growth, with no detectable change in rate."))
        self.assertEqual(line["by"], "agent")
        self.assertEqual(line["where"], "insights/2026-11-22-report.md")
        self.assertIn("STAMPED IN-001 weakened 2026-11-22", done.stdout)

    def test_a_verdict_is_written_once(self):
        self.write("--note", self.note, "--id", "IN-001", "--verdict", "weakened")
        before = self.stamps.read_bytes()
        for verdict in ("kept", "weakened"):
            again = self.write("--note", self.note, "--id", "IN-001", "--verdict", verdict)
            self.assertEqual(again.returncode, 1)
            self.assertIn("already has a stamp (weakened, 2026-11-22)", again.stdout)
        self.assertEqual(self.stamps.read_bytes(), before)

    def test_a_new_challenge_is_appended_with_its_reason_and_the_first_line_stays(self):
        self.write("--note", self.note, "--id", "IN-001", "--verdict", "weakened")
        first = self.stamps.read_text(encoding="utf-8")
        done = self.run_stamp("write", "--note", self.note, "--id", "IN-001", "--verdict", "dropped",
                              "--date", "2026-11-25", "--again", "the base changed to articles only")
        self.assertEqual(done.returncode, 0, done.stdout)
        text = self.stamps.read_text(encoding="utf-8")
        self.assertTrue(text.startswith(first))
        self.assertEqual([line["verdict"] for line in self.lines()], ["weakened", "dropped"])
        self.assertEqual(self.lines()[1]["again"], "the base changed to articles only")
        ledger = stamp.Ledger(self.stamps)
        self.assertEqual(ledger.current("IN-001")[0]["verdict"], "dropped")
        self.assertEqual(ledger.times("IN-001"), 2)

    def test_again_is_refused_for_a_conclusion_never_stamped(self):
        done = self.write("--note", self.note, "--id", "IN-001", "--verdict", "kept", "--again", "why")
        self.assertEqual(done.returncode, 1)
        self.assertFalse(self.stamps.exists())

    def test_only_the_three_verdicts_are_accepted(self):
        for verdict in ("split", "partly", "not challenged", ""):
            done = self.write("--id", "IN-009", "--verdict", verdict, "--text", "A sentence.")
            self.assertNotEqual(done.returncode, 0, verdict)
        self.assertFalse(self.stamps.exists())

    def test_an_id_that_is_not_in_the_note_is_refused(self):
        done = self.write("--note", self.note, "--id", "IN-404", "--verdict", "kept")
        self.assertEqual(done.returncode, 1)
        self.assertIn("has no conclusion with this id", done.stdout)

    def test_an_id_under_two_headings_is_refused(self):
        self.note.write_text(NOTE + "\n### Another sentence.\n\n- **Id:** IN-001\n", encoding="utf-8")
        done = self.write("--note", self.note, "--id", "IN-001", "--verdict", "kept")
        self.assertEqual(done.returncode, 1)
        self.assertIn("two headings", done.stdout)

    def test_a_label_in_the_note_that_differs_is_said_and_the_stamp_is_written(self):
        done = self.write("--note", self.note, "--id", "IN-001", "--verdict", "dropped")
        self.assertEqual(done.returncode, 0)
        self.assertIn('NOTE IN-001: the note shows "weakened" and the stamp says dropped', done.stdout)

    def test_a_wrong_command_line_or_an_unreadable_file_is_exit_code_2(self):
        self.assertEqual(self.write("--id", "IN-001").returncode, 2)
        self.assertEqual(self.write("--id", "IN-001", "--verdict", "kept").returncode, 2)
        self.assertEqual(self.write("--note", "no-such.md", "--id", "IN-001", "--verdict", "kept").returncode, 2)
        self.assertEqual(self.run_stamp("write", "--id", "IN-001", "--verdict", "kept", "--text", "x",
                                        "--date", "22 November").returncode, 2)

    def test_a_home_path_is_not_stored(self):
        outside = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, outside, ignore_errors=True)
        note = outside / "elsewhere.md"
        note.write_text(NOTE, encoding="utf-8")
        self.write("--note", note, "--id", "IN-001", "--verdict", "weakened")
        self.assertEqual(self.lines()[0]["where"], "elsewhere.md")

    def test_a_file_whose_last_line_has_no_line_end_is_not_joined_to_the_new_stamp(self):
        self.write("--id", "IN-001", "--verdict", "kept", "--text", "One.")
        self.stamps.write_bytes(self.stamps.read_bytes().rstrip(b"\n"))
        self.write("--id", "IN-002", "--verdict", "kept", "--text", "Two.")
        self.assertEqual([line["id"] for line in self.lines()], ["IN-001", "IN-002"])


class FromTheChallengersAnswer(Folder):
    ANSWER = """Two of two conclusions tested.

### IN-001
- **Verdict:** weakened
- **Narrower:** Slow growth, with no detectable
  change in rate.
- **Reason:** the two rates differ by about one standard error.

### IN-002 · the share in five countries
- **Verdict:** **Dropped**
- **Narrower:** none
- **Reason:** rests on one pass.

### Not checked
The data behind IN-002.
"""

    def answer(self, text=None):
        path = self.folder / "answer.md"
        path.write_text(text or self.ANSWER, encoding="utf-8")
        return path

    def test_ids_and_verdicts_are_read_from_the_answer(self):
        done = self.write("--note", self.note, "--verdicts", self.answer(), "--by", "agent")
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        self.assertEqual([(line["id"], line["verdict"]) for line in self.lines()],
                         [("IN-001", "weakened"), ("IN-002", "dropped")])

    def test_the_answer_form_of_the_challenger_agent_is_read(self):
        answer = ("I named nothing.\n\n### IN-002\n- **Claim:** The share rose in five countries.\n"
                  "- **Verdict:** kept\n- **Narrower:** none\n- **Reason:** Holds.\n\n"
                  "### IN-001\n- **Claim:** Slow growth with a modest acceleration.\n- **Verdict:** weakened\n"
                  "- **Narrower:** Slow growth, with no detectable\nchange in rate.\n"
                  "**Tally:** 1 kept, 1 weakened, 0 dropped.\n")
        self.assertEqual(stamp.answer_verdicts(answer), [
            {"id": "IN-002", "verdict": "kept", "as_written": "kept", "narrower": ""},
            {"id": "IN-001", "verdict": "weakened", "as_written": "weakened",
             "narrower": "Slow growth, with no detectable change in rate."}])
        done = self.write("--note", self.note, "--verdicts", self.answer(answer), "--by", "agent")
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        self.assertIn('NOTE IN-002: the note shows "not challenged" and the stamp says kept', done.stdout)

    def test_the_agents_own_file_shows_a_block_this_script_reads(self):
        agent = (helpers.PLUGIN / "agents" / "challenger.md").read_text(encoding="utf-8")
        block = agent.split("```")[1]
        for label in ("Claim", "Verdict", "Narrower", "Reason", "Parts", "Rivals added", "Checks", "Confidence",
                      "Not checked"):
            self.assertIn(f"- **{label}:**", block)
        filled = block.replace("<id>", "IN-001").replace("<kept, weakened or dropped>", "dropped")
        self.assertEqual([(v["id"], v["verdict"]) for v in stamp.answer_verdicts(filled)], [("IN-001", "dropped")])

    def test_a_weakened_conclusion_must_stand_in_the_note_as_the_narrower_claim(self):
        answer = self.ANSWER.replace("Slow growth, with no detectable\n  change in rate.", "Slow growth only.")
        done = self.write("--note", self.note, "--verdicts", self.answer(answer))
        self.assertEqual(done.returncode, 1)
        self.assertIn("REFUSED IN-001: weakened, and the note's heading is not the narrower claim", done.stdout)
        self.assertIn("Nothing was written.", done.stdout)
        self.assertFalse(self.stamps.exists())

    def test_a_verdict_for_an_id_the_note_does_not_have_stops_everything(self):
        done = self.write("--note", self.note, "--verdicts", self.answer(self.ANSWER.replace("IN-002", "IN-007")))
        self.assertEqual(done.returncode, 1)
        self.assertFalse(self.stamps.exists())

    def test_a_word_that_is_not_a_verdict_stops_everything(self):
        answer = self.ANSWER.replace("**Dropped**", "split")
        done = self.write("--note", self.note, "--verdicts", self.answer(answer))
        self.assertEqual(done.returncode, 1)
        self.assertIn('IN-002: the answer\'s verdict "split" is not one word of kept, weakened, dropped', done.stdout)
        self.assertFalse(self.stamps.exists())

    def test_an_answer_with_no_verdict_is_refused(self):
        done = self.write("--note", self.note, "--verdicts", self.answer("All fine.\n"))
        self.assertEqual(done.returncode, 1)

    def test_one_conclusion_already_stamped_stops_the_whole_answer(self):
        self.write("--note", self.note, "--id", "IN-002", "--verdict", "kept")
        done = self.write("--note", self.note, "--verdicts", self.answer())
        self.assertEqual(done.returncode, 1)
        self.assertEqual(len(self.lines()), 1)


class Verifying(Folder):
    def setUp(self):
        super().setUp()
        self.write("--note", self.note, "--id", "IN-001", "--verdict", "weakened")

    def verify(self, *args):
        return self.run_stamp("verify", *args)

    def test_an_untouched_conclusion_verifies(self):
        done = self.verify("--note", self.note, "--id", "IN-001")
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertEqual(done.stdout.splitlines(), ["OK IN-001 weakened 2026-11-22", "1 checked: 1 in order, 0 not."])

    def test_a_changed_sentence_fails(self):
        self.note.write_text(NOTE.replace("Slow growth, with no detectable", "Slow growth, with a detectable"),
                             encoding="utf-8")
        done = self.verify("--note", self.note, "--id", "IN-001")
        self.assertEqual(done.returncode, 1)
        self.assertIn("TEXT CHANGED IN-001", done.stdout)

    def test_the_same_sentence_wrapped_differently_still_verifies(self):
        done = self.verify("--id", "IN-001", "--text", "Slow growth,\n   with no detectable change in rate. ")
        self.assertEqual(done.returncode, 0, done.stdout)

    def test_a_retyped_verdict_fails(self):
        self.note.write_text(NOTE.replace("**Challenge:** weakened", "**Challenge:** Kept"), encoding="utf-8")
        done = self.verify("--note", self.note, "--id", "IN-001")
        self.assertEqual(done.returncode, 1)
        self.assertIn('VERDICT RETYPED IN-001: shown "Kept", stamped weakened on 2026-11-22', done.stdout)

    def test_the_label_is_compared_without_regard_to_capitals_or_bold(self):
        for label in ("Weakened", "**weakened**", "WEAKENED · narrower"):
            self.note.write_text(NOTE.replace("**Challenge:** weakened", f"**Challenge:** {label}"), encoding="utf-8")
            self.assertEqual(self.verify("--note", self.note, "--id", "IN-001").returncode, 0, label)

    def test_a_missing_stamp_fails(self):
        done = self.verify("--note", self.note, "--id", "IN-002")
        self.assertEqual(done.returncode, 1)
        self.assertIn("NO STAMP IN-002", done.stdout)

    def test_a_verdict_shown_with_no_stamp_behind_it_is_named(self):
        self.note.write_text(NOTE.replace("**Challenge:** not challenged", "**Challenge:** kept"), encoding="utf-8")
        done = self.verify("--note", self.note, "--id", "IN-002")
        self.assertEqual(done.returncode, 1)
        self.assertIn('"kept" is shown, and no stamp backs it', done.stdout)

    def test_a_stamp_whose_verdict_was_edited_by_hand_fails(self):
        self.stamps.write_text(self.stamps.read_text(encoding="utf-8").replace('"weakened"', '"kept"'),
                               encoding="utf-8")
        self.note.write_text(NOTE.replace("**Challenge:** weakened", "**Challenge:** kept"), encoding="utf-8")
        done = self.verify("--note", self.note, "--id", "IN-001")
        self.assertEqual(done.returncode, 1)
        self.assertIn("STAMP ALTERED IN-001", done.stdout)
        self.assertIn("does not match its seal", done.stdout)

    def test_an_altered_last_stamp_does_not_bring_back_the_one_before_it(self):
        self.run_stamp("write", "--note", self.note, "--id", "IN-001", "--verdict", "dropped",
                       "--date", "2026-11-25", "--again", "the base changed")
        lines = self.stamps.read_text(encoding="utf-8").splitlines()
        lines[1] = lines[1].replace("2026-11-25", "2026-11-26")
        self.stamps.write_text("\n".join(lines) + "\n", encoding="utf-8")
        done = self.verify("--note", self.note, "--id", "IN-001")
        self.assertEqual(done.returncode, 1)
        self.assertIn("STAMP ALTERED IN-001", done.stdout)

    def test_a_line_that_cannot_be_read_fails_every_conclusion(self):
        with self.stamps.open("a", encoding="utf-8") as handle:
            handle.write("<<<<<<< HEAD\n")
        done = self.verify("--note", self.note, "--id", "IN-001")
        self.assertEqual(done.returncode, 1)
        self.assertIn("the file cannot be trusted", done.stdout)
        refused = self.write("--id", "IN-050", "--verdict", "kept", "--text", "New.")
        self.assertEqual(refused.returncode, 1)

    def test_a_whole_note_checks_its_conclusions_and_skips_what_is_not_one(self):
        done = self.verify("--note", self.note)
        self.assertEqual(done.returncode, 1)
        self.assertEqual(done.stdout.splitlines(), [
            "OK IN-001 weakened 2026-11-22",
            "NO STAMP IN-002: no challenge is recorded",
            "SKIPPED QN-001: a research question with no Challenge line and no stamp; questions are not stamped",
            "2 checked: 1 in order, 1 not.",
        ])

    def test_an_id_that_is_not_in_the_note_fails(self):
        done = self.verify("--note", self.note, "--id", "IN-404")
        self.assertEqual(done.returncode, 1)
        self.assertIn("NOT IN NOTE IN-404", done.stdout)

    def test_no_stamp_file_at_all_is_a_missing_stamp_not_a_crash(self):
        self.stamps.unlink()
        done = self.verify("--note", self.note, "--id", "IN-001")
        self.assertEqual(done.returncode, 1)
        self.assertIn("NO STAMP IN-001", done.stdout)

    def test_a_dropped_conclusion_with_its_stamp_intact_verifies(self):
        self.write("--id", "IN-005", "--verdict", "dropped", "--text", "A dropped claim.")
        done = self.verify("--id", "IN-005", "--text", "A dropped claim.", "--verdict", "dropped")
        self.assertEqual(done.returncode, 0)
        self.assertIn("OK IN-005 dropped", done.stdout)

    def test_a_stamp_of_another_version_is_not_read_as_valid(self):
        line = json.loads(self.stamps.read_text(encoding="utf-8"))
        line["v"] = 2
        self.stamps.write_text(json.dumps(line) + "\n", encoding="utf-8")
        done = self.verify("--note", self.note, "--id", "IN-001")
        self.assertEqual(done.returncode, 1)
        self.assertIn("version 2", done.stdout)

    def test_listing_gives_the_stamp_in_force(self):
        self.run_stamp("write", "--note", self.note, "--id", "IN-001", "--verdict", "dropped",
                       "--date", "2026-11-25", "--again", "the base changed", "--by", "agent")
        done = self.run_stamp("list")
        self.assertEqual(done.returncode, 0)
        self.assertEqual(done.stdout.strip(),
                         "IN-001 dropped 2026-11-25 (by agent; challenged 2 times; again: the base changed)")


class TheReviewsCases(Folder):
    """Ways the first version failed open, found by the independent review of 2026-11-22."""

    def setUp(self):
        super().setUp()
        self.write("--note", self.note, "--id", "IN-001", "--verdict", "weakened")

    def with_label(self, label):
        self.note.write_text(NOTE.replace("- **Challenge:** weakened · the difference cannot be told apart from chance",
                                          label), encoding="utf-8")
        return self.run_stamp("verify", "--note", self.note, "--id", "IN-001")

    def test_a_label_retyped_in_another_form_still_fails(self):
        for label in ("- **Challenged:** kept", "- Challenge: **kept**", "**Challenge:** kept",
                      "- **Challenge:** weakened → kept after review", "- **Challenge:** Weakened? No: kept",
                      "- **Challenge:** not challenged"):
            done = self.with_label(label)
            self.assertEqual(done.returncode, 1, label)
            self.assertIn("VERDICT RETYPED IN-001", done.stdout, label)

    def test_the_stamped_word_in_another_form_still_passes(self):
        for label in ("- Challenge: weakened", "- **Challenge**: **Weakened** · was: \"kept as it stood\"",
                      "- **Challenge:** weakened, narrower"):
            self.assertEqual(self.with_label(label).returncode, 0, label)

    def test_an_insight_with_no_challenge_line_and_no_stamp_is_a_missing_stamp(self):
        self.note.write_text(NOTE.replace("- **Challenge:** not challenged\n", ""), encoding="utf-8")
        done = self.run_stamp("verify", "--note", self.note)
        self.assertEqual(done.returncode, 1)
        self.assertIn("NO STAMP IN-002", done.stdout)
        self.assertIn("SKIPPED QN-001", done.stdout)

    def test_a_note_in_which_nothing_is_recognised_fails(self):
        self.note.write_text("# Notes\n\nNo headings with ids here.\n", encoding="utf-8")
        done = self.run_stamp("verify", "--note", self.note)
        self.assertEqual(done.returncode, 1)
        self.assertIn("Nothing checked", done.stdout)

    def test_an_id_line_without_the_list_dash_is_read(self):
        self.note.write_text("### The share rose in five countries.\n\n**Id:** IN-009\n**Challenge:** kept\n",
                             encoding="utf-8")
        done = self.run_stamp("verify", "--note", self.note)
        self.assertEqual(done.returncode, 1)
        self.assertIn('NO STAMP IN-009: no challenge is recorded: "kept" is shown', done.stdout)

    def test_a_line_separator_in_a_field_does_not_break_the_file(self):
        for odd in ("\u2028", "\u2029", "\u0085", "\x0c"):
            done = self.run_stamp("write", "--note", self.note, "--id", "IN-001", "--verdict", "weakened",
                                  "--date", "2026-11-22", "--again", f"the base changed{odd}second part")
            self.assertEqual(done.returncode, 0, repr(odd))
        self.assertTrue(self.stamps.read_bytes().isascii())
        self.assertEqual(len(self.stamps.read_text(encoding="utf-8").split("\n")), 6)
        self.assertEqual(self.run_stamp("list").returncode, 0)
        self.assertEqual(self.run_stamp("verify", "--note", self.note, "--id", "IN-001").returncode, 0)

    def test_a_research_question_is_not_stamped(self):
        done = self.write("--note", self.note, "--id", "QN-001", "--verdict", "kept")
        self.assertEqual(done.returncode, 1)
        self.assertIn("a question is not stamped", done.stdout)

    def test_a_stamp_line_a_careful_reader_would_reject_is_rejected(self):
        line = self.lines()[0]
        for key, value in (("v", True), ("v", 1.0), ("date", "2026-99-99"), ("date", "２０２６-11-22")):
            self.stamps.write_text(stamp.stamp_line(dict(line, **{key: value})) + "\n", encoding="utf-8")
            done = self.run_stamp("verify", "--note", self.note, "--id", "IN-001")
            self.assertIn("STAMP ALTERED", done.stdout, (key, value))

    def test_an_id_inside_a_longer_code_fence_is_not_a_conclusion(self):
        note = "### Real.\n\n- **Id:** IN-001\n\n````\n```\n### Inside.\n- **Id:** IN-077\n```\n````\n"
        found, _ = stamp.conclusions(note)
        self.assertEqual(list(found), ["IN-001"])


class StrictAnswers(Folder):
    def answer(self, text):
        path = self.folder / "answer.md"
        path.write_text(text, encoding="utf-8")
        return self.write("--note", self.note, "--verdicts", path)

    def test_weakened_with_no_narrower_claim_is_refused(self):
        done = self.answer("### IN-001\n- **Verdict:** weakened\n- **Narrower:** none\n")
        self.assertEqual(done.returncode, 1)
        self.assertIn("gives no narrower claim", done.stdout)
        self.assertFalse(self.stamps.exists())

    def test_a_verdict_with_more_words_than_the_verdict_is_refused(self):
        done = self.answer("### IN-002\n- **Verdict:** kept — but only as a lead, really weakened\n")
        self.assertEqual(done.returncode, 1)
        self.assertFalse(self.stamps.exists())

    def test_a_verdict_line_without_the_dash_is_read_and_a_block_without_one_is_named(self):
        done = self.answer("### IN-002\n**Verdict:** dropped\n\n### IN-001\n- **Reason:** cannot tell\n")
        self.assertEqual(done.returncode, 1)
        self.assertIn("IN-001: the answer has a block for it and no Verdict line that could be read", done.stdout)
        self.assertFalse(self.stamps.exists())


class ReadingANote(unittest.TestCase):
    def test_a_heading_inside_a_code_block_is_not_a_conclusion(self):
        note = "### Real one.\n\n```python\n# not a heading\n- **Id:** IN-009\n```\n\n- **Id:** IN-001\n"
        found, _ = stamp.conclusions(note)
        self.assertEqual(list(found), ["IN-001"])
        self.assertEqual(found["IN-001"]["text"], "Real one.")

    def test_the_sentence_is_the_nearest_heading_above_the_id_line(self):
        note = "## Section\n\ntext\n\n#### The claim, as typed. \n- **Id:** IN-001\n## Next\n- **Id:** IN-002\n"
        found, _ = stamp.conclusions(note)
        self.assertEqual(stamp.normalise(found["IN-001"]["text"]), "The claim, as typed.")
        self.assertEqual(found["IN-002"]["text"], "Next")

    def test_the_id_line_is_read_in_the_forms_people_type(self):
        for line in ("- **Id:** IN-001", "* **Id:** IN-001", "- **ID:** IN-001", "- **Id**: IN-001", "  - **Id:**  IN-001  "):
            found, _ = stamp.conclusions(f"### S.\n{line}\n")
            self.assertEqual(list(found), ["IN-001"], line)

    def test_an_id_without_a_heading_above_it_is_not_a_conclusion(self):
        self.assertEqual(stamp.conclusions("- **Id:** IN-001\n")[0], {})


class TheLabsTrendScan(unittest.TestCase):
    """The pair `fixtures/README.md` in the notebook describes: the published page showed c6 as kept, and the
    challenger had said weakened. Each page is turned into a note (heading: the page's restated claim; Challenge
    line: the verdict the page shows), the challenger's verdicts are stamped on the page's sentences with
    `challenge_stamp.py write`, and each note is checked with `verify`. What this tests is the label: the page
    reworded the challenger's narrower claims, so the sentences stamped here are the page's, not the challenger's
    (the last test shows that the challenger's own sentences do not match the page)."""

    def note_of(self, rows: list[dict]) -> str:
        return "# Trend scan\n\n" + "".join(f"### {row['restated']}\n\n- **Id:** {row['id']}\n"
                                              f"- **Challenge:** {row['verdict']}\n\n" for row in rows)

    def run_pair(self, challenger: dict, published: list[dict], corrected: list[dict], sentences=None):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "insights").mkdir()
            for name, rows in (("published", published), ("corrected", corrected)):
                (root / "insights" / f"{name}.md").write_text(self.note_of(rows), encoding="utf-8")
            for row in corrected:
                if sentences:
                    args = ["--text", sentences[row["id"]]]
                else:
                    args = ["--note", "insights/corrected.md"]
                done = helpers.run("challenge_stamp.py", "write", "--id", row["id"], "--verdict",
                                   challenger[row["id"]], "--date", "2026-11-17", *args, cwd=root)
                self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
            return [helpers.run("challenge_stamp.py", "verify", "--note", f"insights/{name}.md", cwd=root)
                    for name in ("published", "corrected")]

    def test_the_published_verdicts_fail_and_the_corrected_ones_pass(self):
        rows = json.loads(ROWS.read_text(encoding="utf-8"))
        published, corrected = self.run_pair(rows["challenger"], rows["published"], rows["corrected"])
        self.assertEqual(published.returncode, 1)
        self.assertEqual([line for line in published.stdout.splitlines() if not line.startswith("OK ")],
                         ['VERDICT RETYPED c6: shown "kept", stamped weakened on 2026-11-17',
                          "6 checked: 5 in order, 1 not."])
        self.assertEqual(corrected.returncode, 0, corrected.stdout)
        self.assertEqual(corrected.stdout.splitlines()[-1], "6 checked: 6 in order, 0 not.")

    def test_the_same_on_the_notebooks_own_files(self):
        lab = helpers.lab()
        if lab is None:
            self.skipTest("the Poiesis Lab notebook is not on this machine (POIESIS_LAB, or ~/Poiesis Lab)")
        verdicts = json.loads((lab / "challenge-verdicts.json").read_text(encoding="utf-8"))
        run = next(run for run in verdicts["runs"] if run["run"] == "trend-scan")
        challenger = {c["id"].lower(): c["verdict"] for c in run["conclusions"]}
        pages = [json.loads((lab / "trend-scan" / f"challenge.{name}.json").read_text(encoding="utf-8"))["rows"]
                 for name in ("published", "corrected")]
        published, corrected = self.run_pair(challenger, *pages)
        self.assertIn('VERDICT RETYPED c6: shown "kept"', published.stdout)
        self.assertEqual(published.returncode, 1)
        self.assertEqual(corrected.returncode, 0, corrected.stdout)

    def test_the_challengers_own_sentences_are_not_the_pages(self):
        rows = json.loads(ROWS.read_text(encoding="utf-8"))
        _, corrected = self.run_pair(rows["challenger"], rows["published"], rows["corrected"],
                                     sentences=rows["challenger_narrower"])
        self.assertEqual(corrected.returncode, 1)
        self.assertEqual(sum(line.startswith("TEXT CHANGED") for line in corrected.stdout.splitlines()), 6)

    def test_the_copy_in_this_repository_is_the_notebooks(self):
        lab = helpers.lab()
        if lab is None:
            self.skipTest("the Poiesis Lab notebook is not on this machine (POIESIS_LAB, or ~/Poiesis Lab)")
        rows = json.loads(ROWS.read_text(encoding="utf-8"))
        verdicts = json.loads((lab / "challenge-verdicts.json").read_text(encoding="utf-8"))
        run = next(run for run in verdicts["runs"] if run["run"] == "trend-scan")
        self.assertEqual(rows["challenger"], {c["id"].lower(): c["verdict"] for c in run["conclusions"]})
        self.assertEqual(rows["challenger_narrower"], {c["id"].lower(): c["narrower"] for c in run["conclusions"]})
        for name in ("published", "corrected"):
            theirs = json.loads((lab / "trend-scan" / f"challenge.{name}.json").read_text(encoding="utf-8"))["rows"]
            self.assertEqual(rows[name], [{key: row[key] for key in ("id", "verdict", "restated")} for row in theirs])


class TheGateExample(unittest.TestCase):
    """Three conclusions for the entry gate of poiesis-frontier: one kept, one dropped, one never challenged."""

    NOTE = GATE / "insights" / "2026-11-17-gate-example.md"
    STAMPS = GATE / "insights" / "challenge-stamps.jsonl"

    def test_the_stamps_in_the_repository_are_what_the_script_writes(self):
        with tempfile.TemporaryDirectory() as folder:
            shutil.copytree(GATE / "insights", Path(folder) / "insights")
            (Path(folder) / "insights" / "challenge-stamps.jsonl").unlink()
            for id_, verdict in (("IN-001", "kept"), ("IN-002", "dropped")):
                done = helpers.run("challenge_stamp.py", "write", "--note", "insights/2026-11-17-gate-example.md",
                                   "--id", id_, "--verdict", verdict, "--by", "agent", "--date", "2026-11-17",
                                   cwd=folder)
                self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
            written = (Path(folder) / "insights" / "challenge-stamps.jsonl").read_text(encoding="utf-8")
        self.assertEqual(written, self.STAMPS.read_text(encoding="utf-8"))

    def test_one_is_kept_one_is_dropped_and_one_has_no_stamp(self):
        done = helpers.run("challenge_stamp.py", "verify", "--note", "insights/2026-11-17-gate-example.md", cwd=GATE)
        self.assertEqual(done.returncode, 1)
        self.assertEqual(done.stdout.splitlines(), [
            "OK IN-001 kept 2026-11-17",
            "OK IN-002 dropped 2026-11-17",
            "NO STAMP IN-003: no challenge is recorded",
            "3 checked: 2 in order, 1 not.",
        ])

    def test_the_stamps_follow_from_the_description_alone(self):
        found, _ = stamp.conclusions(self.NOTE.read_text(encoding="utf-8"))
        for line in self.STAMPS.read_text(encoding="utf-8").splitlines():
            entry = json.loads(line)
            digest, sealed = by_the_description(found[entry["id"]]["text"], entry["id"], entry["verdict"], entry["date"])
            self.assertEqual((entry["text_sha256"], entry["seal"]), (digest, sealed))

    def test_the_kept_conclusion_is_the_first_vector(self):
        found, _ = stamp.conclusions(self.NOTE.read_text(encoding="utf-8"))
        self.assertEqual(found["IN-001"]["text"], VECTORS["vectors"][0]["text"])


if __name__ == "__main__":
    unittest.main()
