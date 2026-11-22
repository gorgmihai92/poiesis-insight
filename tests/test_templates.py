"""The properties block at the top of an insight report (2.1.0, templates/report.md): what it holds, the rules it
keeps, and that the scripts read a report with it as they read one without it."""
from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

import helpers

sample = helpers.load("sample_check")
TEMPLATES = helpers.SKILL / "templates"
GATE = helpers.TESTS / "fixtures" / "gate"


def block_of(text: str) -> list[str]:
    lines = text.split("\n")
    if lines[0] != "---" or "---" not in lines[1:]:
        return []
    return lines[1: lines.index("---", 1)]


class TheBlock(unittest.TestCase):
    def test_the_report_template_starts_with_the_common_fields(self):
        block = block_of((TEMPLATES / "report.md").read_text(encoding="utf-8"))
        self.assertEqual([line.split(":", 1)[0] for line in block], ["type", "plugin", "date", "topic"])
        self.assertIn("plugin: poiesis-insight", block)

    def test_it_keeps_the_rules_the_other_plugins_need(self):
        for line in block_of((TEMPLATES / "report.md").read_text(encoding="utf-8")):
            self.assertFalse(line.lstrip().startswith("#"), line)
            self.assertNotIn("[[", line)
            self.assertRegex(line, r'^[a-z]+:(?: (?:"[^"]*"|\[\]|<[^:"]*>|[a-z-]+))?$', line)

    def test_the_fragments_have_no_block(self):
        """An insight, a question and a method table go inside a report, so a block there would sit mid-file."""
        for name in ("insight.md", "question.md", "methods.md"):
            self.assertFalse((TEMPLATES / name).read_text(encoding="utf-8").startswith("---"), name)


PROPERTIES = ('---\n'
              'type: insight-report\n'
              'plugin: poiesis-insight\n'
              'date: 2026-11-17\n'
              'topic: "gate example: three conclusions"\n'
              '---\n')


class ReadTheSame(unittest.TestCase):
    def folder(self, prefix: str) -> Path:
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        shutil.copytree(GATE / "insights", root / "insights")
        note = root / "insights" / "2026-11-17-gate-example.md"
        note.write_text(prefix + note.read_text(encoding="utf-8"), encoding="utf-8")
        return root

    def test_ids_lists_and_finds_stale_objects_the_same(self):
        for command in (["list"], ["stale"], ["next", "IN"]):
            without = helpers.run("ids.py", *command, cwd=self.folder(""))
            with_ = helpers.run("ids.py", *command, cwd=self.folder(PROPERTIES))
            self.assertEqual((with_.returncode, with_.stdout), (without.returncode, without.stdout), command)

    def test_the_stamps_verify_the_same(self):
        results = []
        for prefix in ("", PROPERTIES):
            root = self.folder(prefix)
            done = helpers.run("challenge_stamp.py", "verify", "--note", "insights/2026-11-17-gate-example.md", cwd=root)
            results.append((done.returncode, done.stdout))
        self.assertEqual(results[1], results[0])
        self.assertIn("OK IN-001 kept 2026-11-17", results[0][1])

    def test_the_same_claims_are_drawn(self):
        text = (GATE / "insights" / "2026-11-17-gate-example.md").read_text(encoding="utf-8")
        shift = PROPERTIES.count("\n")
        self.assertEqual(sample.claims_of(PROPERTIES + text),
                         [(n + shift, line) for n, line in sample.claims_of(text)])


if __name__ == "__main__":
    unittest.main()
