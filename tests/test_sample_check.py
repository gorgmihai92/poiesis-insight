"""The human check: claims drawn at random, and what the checks so far allow."""
from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

import helpers

sample = helpers.load("sample_check")

REPORT = """# Report

Twelve studies were read (see [the map](../research/maps/blame.md)).

### People blame both the user and the tool.

- **Id:** IN-001
- **From:** example-2023, [@smith2020, p. 4]
- **Evidence:** blame was above zero for both in 9 of 12 studies — example-2023 (p. 7); a second sample agrees [@smith2020, p. 4]
- **Challenge:** kept · holds in two samples

| study | design |
|---|---|
| Example 2023 (p. 2) | vignette |

1. One study measured behaviour: [[example-2024-field-study]].
2. The largest sample is 412 people (p. 9), in doi 10.1000/example.7.
3. A line with a pipe | in it, from https://example.org/paper.
4. A line with no pointer to a source.

```
- a line in a code block (p. 1)
```
"""


class Claims(unittest.TestCase):
    def test_only_lines_that_point_to_a_source_are_claims(self):
        found = sample.claims_of(REPORT)
        self.assertEqual([number for number, _ in found], [3, 9, 16, 17, 18])

    def test_field_lines_table_rows_headings_and_code_are_left_out(self):
        text = " ".join(line for _, line in sample.claims_of(REPORT))
        for absent in ("**From:**", "**Challenge:**", "Example 2023 (p. 2)", "code block", "no pointer"):
            self.assertNotIn(absent, text)


class Bound(unittest.TestCase):
    def test_five_clean_checks_leave_up_to_45_per_cent(self):
        self.assertAlmostEqual(sample.upper_bound(5, 0), 1 - 0.05 ** (1 / 5), places=9)
        self.assertEqual(round(sample.upper_bound(5, 0) * 100, 1), 45.1)

    def test_thirty_clean_checks_bring_it_under_10_per_cent(self):
        self.assertEqual(round(sample.upper_bound(30, 0) * 100, 1), 9.5)
        self.assertGreater(sample.upper_bound(28, 0), 0.10)
        self.assertLess(sample.upper_bound(29, 0), 0.10)

    def test_the_bound_solves_the_binomial_equation(self):
        for checked, wrong in ((10, 1), (30, 2), (50, 5)):
            share = sample.upper_bound(checked, wrong)
            tail = sum(sample.math.comb(checked, k) * share ** k * (1 - share) ** (checked - k)
                       for k in range(wrong + 1))
            self.assertAlmostEqual(tail, 0.05, places=9)

    def test_an_error_raises_the_bound_and_more_checks_lower_it(self):
        self.assertGreater(sample.upper_bound(30, 1), sample.upper_bound(30, 0))
        self.assertLess(sample.upper_bound(60, 0), sample.upper_bound(30, 0))
        self.assertEqual(sample.upper_bound(4, 4), 1.0)

    def test_numbers_that_make_no_sense_are_refused(self):
        for checked, wrong in ((0, 0), (5, 6), (5, -1)):
            with self.assertRaises(ValueError):
                sample.upper_bound(checked, wrong)


class Commands(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        (self.root / "insights").mkdir()
        (self.root / "insights" / "2026-11-22-blame.md").write_text(REPORT, encoding="utf-8")
        self.log = self.root / "insights" / "human-checks.md"

    def run_sample(self, *args):
        return helpers.run("sample_check.py", *args, cwd=self.root)

    def pick(self, *args):
        return self.run_sample("pick", "insights/2026-11-22-blame.md", "--date", "2026-11-22", *args)

    def test_the_same_seed_gives_the_same_draw_and_the_seed_is_printed(self):
        first = self.pick("--n", "3", "--seed", "7")
        self.log.unlink()
        second = self.pick("--n", "3", "--seed", "7")
        self.assertEqual(first.stdout, second.stdout)
        self.assertIn("3 of the 5 lines that point to a source, drawn with seed 7:", first.stdout)
        self.log.unlink()
        self.assertNotEqual(self.pick("--n", "3", "--seed", "8").stdout, first.stdout)

    def test_without_a_seed_one_is_drawn_and_printed(self):
        self.assertRegex(self.pick("--n", "2").stdout, r"drawn with seed \d+:")

    def test_the_rows_are_added_to_the_log_with_an_empty_result(self):
        self.pick("--n", "5", "--seed", "1")
        rows = sample.read_rows(self.log)
        self.assertEqual(len(rows), 5)
        self.assertEqual({row[4] for row in rows}, {""})
        self.assertEqual({row[1] for row in rows}, {"insights/2026-11-22-blame.md"})
        self.assertTrue(any("A line with a pipe / in it" in row[3] for row in rows))
        self.assertIn("The report has only", self.pick("--n", "9", "--seed", "1").stdout)
        self.assertEqual(len(sample.read_rows(self.log)), 10)       # a second draw is added, nothing is replaced

    def test_a_report_with_no_pointer_to_a_source_is_exit_code_1(self):
        (self.root / "insights" / "2026-11-22-blame.md").write_text("# Nothing cited\n\nA thought.\n", encoding="utf-8")
        done = self.pick()
        self.assertEqual(done.returncode, 1)
        self.assertFalse(self.log.exists())

    def test_the_score_counts_what_a_person_filled_in(self):
        self.pick("--n", "5", "--seed", "1")
        text = self.log.read_text(encoding="utf-8").splitlines()
        rows = [i for i, line in enumerate(text) if line.startswith("| 2026")]
        text[rows[0]] = text[rows[0]].replace("|  |  |", "| ok | as stated, p. 7 |")
        text[rows[1]] = text[rows[1]].replace("|  |  |", "| wrong | the source says 9 of 14 |")
        text[rows[2]] = text[rows[2]].replace("|  |  |", "| OK |  |")
        self.log.write_text("\n".join(text) + "\n", encoding="utf-8")
        done = self.run_sample("score")
        self.assertEqual(done.stdout.splitlines()[0], "5 rows: 2 ok, 1 wrong, 2 not checked yet.")
        self.assertIn("3 checked, 1 wrong: up to 86.5% of claims could be wrong", done.stdout)

    def test_nothing_checked_yet_gives_no_bound(self):
        self.pick("--n", "2", "--seed", "1")
        self.assertIn("Nothing has been checked", self.run_sample("score").stdout)
        self.log.unlink()
        self.assertIn("No checks yet", self.run_sample("score").stdout)

    def test_the_bound_command_gives_the_plans_two_numbers(self):
        self.assertIn("5 checked, 0 wrong: up to 45.1%", self.run_sample("bound", "--checked", "5", "--wrong", "0").stdout)
        self.assertIn("30 checked, 0 wrong: up to 9.5%", self.run_sample("bound", "--checked", "30", "--wrong", "0").stdout)
        self.assertEqual(self.run_sample("bound", "--checked", "0", "--wrong", "0").returncode, 2)


if __name__ == "__main__":
    unittest.main()
