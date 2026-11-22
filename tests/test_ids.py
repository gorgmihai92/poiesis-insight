"""Ids and From: the next free id, the listing, and what went stale when a verdict changed."""
from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

import helpers

ids = helpers.load("ids")

INSIGHTS = """# Report

### The share rose in five countries.

- **Id:** IN-001
- **From:** walters-2023-citation-accuracy, [@smith2020, p. 4]
- **Challenge:** kept

### Raw counts overstate growth by about 16 points.

- **Id:** IN-002
- **Challenge:** weakened

### Solid-state batteries declined in 2025.

- **Id:** IN-003
- **Challenge:** dropped

## Questions

### Does the rise hold on a base of articles only?

- **Id:** QN-001
- **From:** IN-002, IN-001
"""
CONCEPTS = """# Concepts

### A counter that shows the base it divides by

- **Id:** CN-001
- **From:** QN-001

### A battery tracker

- **Id:** CN-002
- **From:** IN-003

### An older idea, added to this note later

- **Id:** CN-003
- **Written:** 2026-11-10
- **From:** IN-001
"""


class Project(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        (self.root / "insights").mkdir()
        (self.root / "frontier").mkdir()
        (self.root / "insights" / "2026-11-17-trends.md").write_text(INSIGHTS, encoding="utf-8")
        (self.root / "frontier" / "2026-11-20-concepts.md").write_text(CONCEPTS, encoding="utf-8")

    def stamp(self, id_, verdict, date, *more):
        done = helpers.run("challenge_stamp.py", "write", "--note", "insights/2026-11-17-trends.md", "--id", id_,
                           "--verdict", verdict, "--date", date, *more, cwd=self.root)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)

    def ids(self, *args):
        return helpers.run("ids.py", *args, cwd=self.root)

    def first_challenge(self):
        self.stamp("IN-001", "kept", "2026-11-17")
        self.stamp("IN-002", "weakened", "2026-11-17")
        self.stamp("IN-003", "dropped", "2026-11-17")


class NextId(Project):
    def test_the_next_id_follows_the_highest_one_in_the_notes(self):
        self.assertEqual(self.ids("next", "IN").stdout.strip(), "IN-004")
        self.assertEqual(self.ids("next", "QN").stdout.strip(), "QN-002")
        self.assertEqual(self.ids("next", "SC").stdout.strip(), "SC-001")

    def test_a_number_is_not_reused_after_its_note_is_gone(self):
        self.first_challenge()
        (self.root / "frontier" / "2026-11-20-concepts.md").write_text(
            "### One\n\n- **Id:** CN-009\n- **From:** IN-007\n", encoding="utf-8")
        (self.root / "insights" / "2026-11-17-trends.md").unlink()
        self.assertEqual(self.ids("next", "IN").stdout.strip(), "IN-008")      # IN-007 is named in a From line
        (self.root / "frontier" / "2026-11-20-concepts.md").unlink()
        self.assertEqual(self.ids("next", "IN").stdout.strip(), "IN-004")      # IN-003 is still in the stamps

    def test_a_prefix_has_to_be_capital_letters(self):
        self.assertEqual(self.ids("next", "in-1").returncode, 2)
        self.assertEqual(self.ids("next").returncode, 2)


class Listing(Project):
    def test_each_object_is_listed_with_its_note_day_verdict_and_from(self):
        self.first_challenge()
        lines = self.ids("list").stdout.splitlines()
        self.assertEqual(lines[0], "IN-001 | insights/2026-11-17-trends.md | 2026-11-17 | kept 2026-11-17 | From: "
                                   "walters-2023-citation-accuracy, [@smith2020, p. 4] | The share rose in five countries.")
        self.assertIn("QN-001 | insights/2026-11-17-trends.md | 2026-11-17 | no stamp | From: IN-002, IN-001 | ",
                      lines[3])
        self.assertIn("CN-003 | frontier/2026-11-20-concepts.md | 2026-11-10 | no stamp | From: IN-001", lines[-2])
        self.assertEqual(lines[-1], "7 objects in research, insights, foresight, frontier, design.")

    def test_a_prefix_limits_the_listing(self):
        lines = self.ids("list", "--prefix", "CN").stdout.splitlines()
        self.assertEqual([line.split(" | ")[0] for line in lines[:-1]], ["CN-001", "CN-002", "CN-003"])

    def test_an_id_under_two_headings_is_said(self):
        with (self.root / "frontier" / "2026-11-20-concepts.md").open("a", encoding="utf-8") as handle:
            handle.write("\n### Again\n\n- **Id:** CN-001\n")
        self.assertIn("TWICE CN-001", self.ids("list").stdout)


class Stale(Project):
    def test_nothing_is_stale_right_after_the_first_challenge(self):
        self.stamp("IN-001", "kept", "2026-11-17")
        self.stamp("IN-002", "weakened", "2026-11-17")
        done = self.ids("stale")
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertEqual(done.stdout.strip(), "7 objects read, 5 with a From line: 0 findings.")

    def test_an_object_built_on_a_dropped_conclusion_is_named(self):
        self.first_challenge()
        done = self.ids("stale")
        self.assertEqual(done.returncode, 1)
        self.assertIn("DROPPED SOURCE CN-002 (frontier/2026-11-20-concepts.md, 2026-11-20): IN-003 was dropped on "
                      "2026-11-17, on or before the object's day", done.stdout)

    def test_a_new_challenge_after_the_object_was_written_makes_it_stale_and_travels_on(self):
        self.first_challenge()
        self.stamp("IN-002", "dropped", "2026-11-25", "--again", "the base changed to articles only")
        done = self.ids("stale")
        self.assertEqual(done.returncode, 1)
        self.assertIn("STALE QN-001 (insights/2026-11-17-trends.md, 2026-11-17): IN-002 was challenged again "
                      "(dropped) on 2026-11-25: the base changed to articles only", done.stdout)
        self.assertIn("THROUGH CN-001 (frontier/2026-11-20-concepts.md, 2026-11-20): rests on QN-001, which is stale",
                      done.stdout)
        self.assertNotIn("CN-003", done.stdout)

    def test_a_first_verdict_that_arrives_after_the_object_was_written(self):
        self.stamp("IN-001", "weakened", "2026-11-21")
        done = self.ids("stale")
        self.assertIn("STALE CN-003 (frontier/2026-11-20-concepts.md, 2026-11-10): IN-001 was weakened on 2026-11-21",
                      done.stdout)
        self.assertIn("STALE QN-001", done.stdout)

    def test_a_first_verdict_of_kept_changes_nothing(self):
        self.stamp("IN-001", "kept", "2026-11-21")
        self.assertEqual(self.ids("stale").returncode, 0)

    def test_challenged_again_and_kept_is_still_said(self):
        self.stamp("IN-001", "kept", "2026-11-17")
        self.stamp("IN-001", "kept", "2026-11-25", "--again", "new data")
        self.assertIn("STALE QN-001", self.ids("stale").stdout)

    def test_a_new_challenge_on_the_objects_own_day_is_not_judged(self):
        self.stamp("IN-001", "kept", "2026-11-09")
        self.stamp("IN-001", "weakened", "2026-11-10", "--again", "a second look")
        done = self.ids("stale")
        self.assertIn("SAME DAY CN-003", done.stdout)
        self.assertNotIn("STALE CN-003", done.stdout)

    def test_an_object_with_no_day_is_named_not_guessed(self):
        (self.root / "frontier" / "concepts.md").write_text("### Undated\n\n- **Id:** CN-010\n- **From:** IN-001\n",
                                                            encoding="utf-8")
        self.stamp("IN-001", "weakened", "2026-11-17")
        self.assertIn("NO DATE CN-010 (frontier/concepts.md, no date)", self.ids("stale").stdout)

    def test_it_changes_nothing(self):
        self.first_challenge()
        before = {path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        self.ids("stale")
        self.ids("list")
        self.ids("next", "IN")
        self.assertEqual(before, {path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()})

    def test_a_damaged_stamp_file_is_said_and_is_not_exit_code_0(self):
        self.first_challenge()
        with (self.root / "insights" / "challenge-stamps.jsonl").open("a", encoding="utf-8") as handle:
            handle.write("not json\n")
        done = self.ids("stale")
        self.assertEqual(done.returncode, 1)
        self.assertIn("DAMAGED line 4", done.stdout)

    def test_a_project_with_no_notes_and_no_stamps_is_not_an_error(self):
        empty = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, empty, ignore_errors=True)
        done = helpers.run("ids.py", "stale", cwd=empty)
        self.assertEqual(done.returncode, 0)
        self.assertEqual(done.stdout.strip(), "0 objects read, 0 with a From line: 0 findings.")


class TheReviewsCases(Project):
    def test_an_altered_stamp_is_a_finding_not_silence(self):
        self.stamp("IN-001", "kept", "2026-11-17")
        path = self.root / "insights" / "challenge-stamps.jsonl"
        path.write_text(path.read_text(encoding="utf-8").replace("2026-11-17", "2026-11-16"), encoding="utf-8")
        done = self.ids("stale")
        self.assertEqual(done.returncode, 1)
        self.assertIn("STAMP ALTERED QN-001", done.stdout)
        self.assertEqual(self.ids("list").returncode, 1)

    def test_a_dropped_source_travels_along_from(self):
        self.first_challenge()
        (self.root / "frontier" / "2026-11-21-more.md").write_text(
            "### Built on the tracker\n\n- **Id:** CN-004\n- **From:** CN-002\n", encoding="utf-8")
        self.assertIn("THROUGH CN-004", self.ids("stale").stdout)

    def test_a_folder_that_does_not_exist_is_exit_code_2(self):
        self.assertEqual(helpers.run("ids.py", "stale", "--root", "no/such/folder", cwd=self.root).returncode, 2)

    def test_next_counts_numbers_in_log_tables_too(self):
        (self.root / "foresight").mkdir()
        (self.root / "foresight" / "forecasts.md").write_text(
            "| id | question |\n|---|---|\n| F-001 | one |\n| F-002 | two |\n", encoding="utf-8")
        self.assertEqual(self.ids("next", "F").stdout.strip(), "F-003")

    def test_a_written_line_moves_the_objects_day(self):
        self.stamp("IN-001", "kept", "2026-11-17")
        self.stamp("IN-001", "weakened", "2026-11-25", "--again", "new data")
        concepts = self.root / "frontier" / "2026-11-20-concepts.md"
        concepts.write_text(concepts.read_text(encoding="utf-8").replace("- **Written:** 2026-11-10",
                                                                          "- **Written:** 2026-11-26"), encoding="utf-8")
        self.assertNotIn("STALE CN-003", self.ids("stale").stdout)


class TheRecheckCases(Project):
    def test_a_number_in_prose_does_not_move_next(self):
        (self.root / "insights" / "2026-11-21-prose.md").write_text("# Prose\n\nIN-2024 was a year of change.\n",
                                                                    encoding="utf-8")
        self.assertEqual(self.ids("next", "IN").stdout.strip(), "IN-004")


class FromLine(unittest.TestCase):
    def test_ids_note_names_and_citations_are_separated(self):
        self.assertEqual(ids.from_items("IN-001, `QN-002`; walters-2023, [@smith2020, p. 4]"),
                         ["IN-001", "QN-002", "walters-2023", "[@smith2020, p. 4]"])
        self.assertEqual(ids.from_items(""), [])


if __name__ == "__main__":
    unittest.main()
