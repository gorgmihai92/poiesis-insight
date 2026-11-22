"""The entry gate: a claim's quote is found in the source's text."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import helpers

gate = helpers.load("quote_gate")
NOTES = helpers.TESTS / "texts" / "notes"
PAPERS = helpers.TESTS / "texts" / "papers"
TEXT = (PAPERS / "example-2020-counting-works.txt").read_text(encoding="utf-8")


class Finding(unittest.TestCase):
    def setUp(self):
        self.pages = gate.pages_of(TEXT)

    def test_true_words_on_the_cited_page_are_found(self):
        self.assertEqual(gate.find("the database itself takes in new kinds of record", self.pages, (1, 1))[0], "FOUND")

    def test_a_hyphen_at_a_line_end_and_curly_marks_do_not_matter(self):
        self.assertEqual(gate.find("the data-base itself takes in", self.pages, (1, 1))[0], "FOUND")
        self.assertEqual(gate.find('We call this the "base effect".', self.pages, (2, 2))[0], "FOUND")

    def test_a_changed_digit_is_not_found(self):
        self.assertEqual(gate.find("In our sample of 412 topics, 73 showed a fall", self.pages, (2, 2))[0], "NOT FOUND")

    def test_true_words_on_another_page_are_the_wrong_page(self):
        status, where = gate.find("A count describes the database as much as the field.", self.pages, (2, 2))
        self.assertEqual(status, "WRONG PAGE")
        self.assertIn("start on p. 3", where)

    def test_a_quote_with_an_ellipsis_needs_every_part_in_order(self):
        self.assertEqual(gate.find("A share computed over all works then falls ... We call this", self.pages, (2, 2))[0], "FOUND")
        self.assertEqual(gate.find("We call this ... A share computed over all works", self.pages, (2, 2))[0], "NOT FOUND")

    def test_a_quote_may_run_onto_the_next_page_but_starts_on_the_one_given(self):
        across = "disappeared when the base was limited to articles. A count describes the database"
        self.assertEqual(gate.find(across, self.pages, (2, 2))[0], "FOUND")
        self.assertEqual(gate.find(across, self.pages, (3, 3))[0], "WRONG PAGE")

    def test_a_very_short_quote_is_marked_as_a_weak_check(self):
        self.assertIn("weak check", gate.find("base effect", self.pages, (2, 2))[1])

    def test_a_text_without_page_marks_is_searched_whole(self):
        pages = gate.pages_of("no marks here, only the words to find")
        self.assertEqual(gate.find("only the words to find", pages, (4, 4))[0], "FOUND")


class TheReviewsCases(unittest.TestCase):
    PAGES = {1: "Growth of 40% was observed (p < 0.5). The effect did not change behaviour in the lab.",
             2: "Scores rose by 1,000 points, and the change was -3.2 on average."}

    def setUp(self):
        self.pages = {n: gate.fold(text) for n, text in self.PAGES.items()}

    def test_a_moved_decimal_point_or_a_changed_sign_is_not_found(self):
        for quote, page in (("Growth of 4.0% was observed", 1), ("(p < .05)", 1), ("rose by 1.000 points", 2),
                            ("the change was 3.2 on average", 2), ("Growth of 40 was observed", 1)):
            self.assertEqual(gate.find(quote, self.pages, (page, page))[0], "NOT FOUND", quote)
        for quote, page in (("Growth of 40% was observed (p < 0.5)", 1), ("rose by 1,000 points", 2),
                            ("the change was −3.2 on average", 2)):
            self.assertEqual(gate.find(quote, self.pages, (page, page))[0], "FOUND", quote)

    def test_an_ellipsis_does_not_bridge_a_long_gap(self):
        long_text = {1: "The effect " + "filler words here " * 30 + "changed behaviour."}
        pages = {n: gate.fold(text) for n, text in long_text.items()}
        self.assertEqual(gate.find("The effect ... changed behaviour", pages, (1, 1))[0], "NOT FOUND")
        status, where = gate.find("The effect ... did not change behaviour", self.pages, (1, 1))
        self.assertEqual(status, "FOUND")
        self.assertIn("has an ellipsis", where)

    def test_a_line_under_quotes_that_is_not_a_quote_is_reported(self):
        note = "# A\n\n## Quotes\n- \"the database itself takes in new kinds of record\" (p. 1)\n- the effect was large (p. 2)\n> a blockquote (p. 2)\n"
        read = {number for number, _, _ in gate.quotes_of(note)}
        self.assertEqual([n for n, _ in gate.unread_quote_lines(note, read)], [5, 6])


class TheRecheckCases(unittest.TestCase):
    def test_an_apostrophe_after_the_quote_does_not_end_it(self):
        note = '- "the database itself takes in new kinds of record" (p. 1), the authors\' words\n'
        ((_, quote, span),) = gate.quotes_of(note)
        self.assertEqual((quote, span), ("the database itself takes in new kinds of record", (1, 1)))


class Reading(unittest.TestCase):
    def test_quote_lines_give_their_words_and_pages(self):
        note = '- "one" (p. 4)\n- “two” (pp. 4–5)\n- not a quote (p. 2)\n* "three"\n'
        self.assertEqual(gate.quotes_of(note), [(1, "one", (4, 4)), (2, "two", (4, 5)), (4, "three", None)])

    def test_the_read_level_is_taken_from_the_note(self):
        self.assertEqual(gate.read_level("- **Read:** abstract only · 2026-11-22\n"), "abstract only · 2026-11-22")
        self.assertEqual(gate.read_level("- **Evidence:** analytical · **abstract only**.\n"), "abstract only")
        self.assertEqual(gate.read_level("# A note\n"), "not stated")


class Gate(unittest.TestCase):
    def run_gate(self, *args):
        return helpers.run("quote_gate.py", *args)

    def test_one_note_two_true_quotes_one_changed_one_on_the_wrong_page(self):
        done = self.run_gate(NOTES / "example-2020-counting-works.md")
        self.assertEqual(done.returncode, 1)
        statuses = [line.split()[0] + (" PAGE" if line.startswith("WRONG") else "")
                    for line in done.stdout.splitlines() if "example-2020" in line]
        self.assertEqual([status.replace("NOT", "NOT FOUND") for status in statuses],
                         ["FOUND", "FOUND", "NOT FOUND", "WRONG PAGE", "FOUND"])
        self.assertIn("2 quotes failed", done.stdout)

    def test_a_note_with_no_quote_and_one_with_no_text_are_said_not_passed_silently(self):
        done = self.run_gate(NOTES / "example-2021-abstract-only.md", NOTES / "example-2022-no-text-here.md")
        self.assertEqual(done.returncode, 0)
        self.assertIn("NO QUOTES  example-2021-abstract-only.md · read: abstract only", done.stdout)
        self.assertIn("NO TEXT    example-2022-no-text-here.md · read: full text", done.stdout)
        self.assertIn("2 notes not checked against the source", done.stdout)

    def test_strict_fails_when_a_note_could_not_be_checked(self):
        self.assertEqual(self.run_gate(NOTES / "example-2021-abstract-only.md", "--strict").returncode, 1)
        self.assertEqual(self.run_gate(NOTES / "example-2022-no-text-here.md", "--strict").returncode, 1)

    def test_the_text_is_also_looked_for_in_a_papers_folder(self):
        done = self.run_gate(NOTES / "example-2022-no-text-here.md", "--papers", PAPERS)
        self.assertIn("NO TEXT", done.stdout)       # no file of that name there either
        done = self.run_gate(NOTES, "--papers", PAPERS)
        self.assertEqual(done.returncode, 1)

    def test_a_path_that_does_not_exist_is_exit_code_2(self):
        self.assertEqual(self.run_gate("no/such/folder").returncode, 2)


class ThisRepositorysNotes(unittest.TestCase):
    """The notes behind the plugin's own rules, checked where their texts are on the machine."""

    def test_no_quote_in_the_notes_fails(self):
        notes = helpers.ROOT / "research" / "notes"
        papers = helpers.ROOT / "research" / "papers"
        done = helpers.run("quote_gate.py", notes, "--papers", papers)
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertNotIn("NOT FOUND", done.stdout)
        self.assertNotIn("WRONG PAGE", done.stdout)


if __name__ == "__main__":
    unittest.main()


PROPERTIES = ('---\n'
              'type: source-note\n'
              'plugin: poiesis-research\n'
              'from:\n'
              '  - "[[IN-001]]"\n'
              '  - "words that are in no source"\n'
              '---\n')


class PropertiesAtTheTop(unittest.TestCase):
    """Obsidian's properties block, YAML between two `---` lines at the very top, is not part of the note's text:
    a list item in it that starts with a quotation mark is not a quote."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self._tmp.name)
        self.original = (NOTES / "example-2020-counting-works.md").read_text(encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def gate_on(self, text: str):
        note = self.folder / "example-2020-counting-works.md"
        note.write_text(text, encoding="utf-8")
        return helpers.run("quote_gate.py", note, "--papers", PAPERS)

    def test_the_gate_gives_the_same_result_with_and_without_properties(self):
        without = self.gate_on(self.original)
        with_ = self.gate_on(PROPERTIES + self.original)
        self.assertEqual(with_.returncode, without.returncode)
        self.assertEqual(with_.stdout.splitlines()[-2:], without.stdout.splitlines()[-2:])
        statuses = lambda done: [line.split(" · ")[0].split()[0] for line in done.stdout.splitlines() if " · line " in line]
        self.assertEqual(statuses(with_), statuses(without))
        self.assertNotIn("IN-001", with_.stdout)

    def test_line_numbers_still_count_the_properties_lines(self):
        first = lambda done: next(line for line in done.stdout.splitlines() if " · line " in line)
        number = lambda line: int(line.split(" · line ")[1].split(" · ")[0])
        self.assertEqual(number(first(self.gate_on(PROPERTIES + self.original))),
                         number(first(self.gate_on(self.original))) + PROPERTIES.count("\n"))
