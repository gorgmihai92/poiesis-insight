"""The eval cases: written in the documented layout, built from the recorded runs, and never run here."""
from __future__ import annotations

import re
import unittest

import eval_data
import helpers

EVALS = helpers.PLUGIN / "evals"
CASES = sorted(path.parent for path in EVALS.glob("*/prompt.md"))
PROMPT_KEYS = {"schema_version", "name", "description", "tags", "plugins", "runs", "expected_outcome", "model",
               "max_turns", "timeout_seconds", "allowed_tools", "append_system_prompt", "env"}
GRADER_KEYS = {"regex": {"pattern", "flags", "match", "target"}, "tool_used": {"tool", "input_match", "min", "max"},
               "llm": {"criteria", "focus"}}
READ_ONLY_TOOLS = {"Read", "Glob", "Grep", "NotebookRead", "Skill", "AskUserQuestion", "Agent", "TodoWrite"}
RECORDED = {"C1": "weakened", "C2": "weakened", "C3": "weakened", "C4": "weakened", "C5": "weakened",
            "C6": "weakened", "I1": "weakened", "I2": "weakened", "I3": "weakened", "I4": "weakened",
            "I5": "dropped", "T1": "kept", "T2": "weakened", "T3": "weakened", "T4": "weakened", "T5": "dropped"}


def parts(path):
    """The frontmatter of a case file as a dict of raw strings, and its body."""
    text = path.read_text(encoding="utf-8")
    _, front, body = text.split("---\n", 2)
    fields = {}
    for line in front.splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields, body


def unquote(value: str) -> str:
    return value[1:-1] if len(value) > 1 and value[0] == value[-1] and value[0] in "'\"" else value


def graders(case):
    return {path.stem: parts(path) for path in sorted((case / "graders").glob("*.md"))}


def answer(verdicts: dict[str, str]) -> str:
    """An answer in the form `agents/challenger.md` asks for."""
    blocks = [f"### {id_}\n- **Claim:** the sentence\n- **Verdict:** {verdict}\n- **Narrower:** none\n"
              f"- **Reason:** none found among the 15 studies.\n" for id_, verdict in verdicts.items()]
    return "\n".join(blocks) + "\n**Tally:** done.\n"


def passes(grader, text: str) -> bool:
    fields, _ = grader
    flags = re.I if "i" in fields.get("flags", "") else 0
    found = re.findall(unquote(fields["pattern"]), text, flags)
    match = unquote(fields.get("match", "contains"))
    if match == "not_contains":
        return not found
    if match.startswith("count:"):
        return len(found) == int(match.split(":")[1])
    return bool(found)


class Layout(unittest.TestCase):
    def test_there_are_six_cases_and_none_has_results(self):
        self.assertEqual([case.name for case in CASES],
                         ["challenger-responsibility-map", "challenger-trend-scan", "gap-before-question",
                          "method-pattern-is-counted", "new-challenge-after-method-change",
                          "verdict-copied-not-retyped"])
        self.assertFalse((EVALS / "results").exists(), "the cases are written, not run")

    def test_prompts_use_only_documented_fields_and_read_only_tools(self):
        for case in CASES:
            fields, body = parts(case / "prompt.md")
            self.assertLessEqual(set(fields), PROMPT_KEYS, case.name)
            self.assertEqual(fields["runs"], "1", case.name)
            tools = {tool.strip() for tool in fields["allowed_tools"].strip("[]").split(",")}
            self.assertLessEqual(tools, READ_ONLY_TOOLS, case.name)
            self.assertTrue(body.strip(), case.name)

    def test_graders_use_only_documented_types_and_fields(self):
        for case in CASES:
            found = graders(case)
            self.assertTrue(found, case.name)
            for name, (fields, body) in found.items():
                kind = fields["type"]
                self.assertIn(kind, GRADER_KEYS, f"{case.name}/{name}")
                self.assertLessEqual(set(fields) - {"type", "weight", "arm"}, GRADER_KEYS[kind], f"{case.name}/{name}")
                if kind == "llm":
                    self.assertIn("PASS if", body)
                    self.assertIn("FAIL if", body)
                if kind == "regex":
                    re.compile(unquote(fields["pattern"]))

    def test_each_case_has_a_check_that_the_plugin_was_used(self):
        for case in CASES:
            tools = {fields.get("tool") for fields, _ in graders(case).values() if fields["type"] == "tool_used"}
            self.assertTrue(tools & {"Skill", "Agent"}, case.name)

    def test_the_two_challenger_cases_may_dispatch_the_agent(self):
        for name in ("challenger-trend-scan", "challenger-responsibility-map"):
            fields, body = parts(EVALS / name / "prompt.md")
            self.assertIn("Agent", fields["allowed_tools"])
            self.assertIn("`challenger` agent", body)


class SixteenConclusions(unittest.TestCase):
    """One grader per recorded conclusion, on the verdict line of its block."""

    def verdict_graders(self):
        found = {}
        for name in ("challenger-trend-scan", "challenger-responsibility-map"):
            for stem, grader in graders(EVALS / name).items():
                hit = re.fullmatch(r"([cit]\d)-(?:kept|weakened|dropped)(?:-or-(?:kept|weakened|dropped))*", stem)
                if hit:
                    found[hit.group(1).upper()] = grader
        return found

    def test_every_conclusion_has_its_grader(self):
        self.assertEqual(sorted(self.verdict_graders()), sorted(RECORDED))

    def test_the_recorded_verdicts_pass_all_sixteen(self):
        text = answer(RECORDED)
        for id_, grader in self.verdict_graders().items():
            self.assertTrue(passes(grader, text), id_)

    def test_a_challenger_that_keeps_everything_fails_fifteen(self):
        text = answer({id_: "kept" for id_ in RECORDED})
        failed = [id_ for id_, grader in self.verdict_graders().items() if not passes(grader, text)]
        self.assertEqual(sorted(failed), sorted(set(RECORDED) - {"T1"}))

    def test_a_challenger_that_drops_everything_fails_on_the_one_that_held(self):
        text = answer({id_: "dropped" for id_ in RECORDED})
        failed = [id_ for id_, grader in self.verdict_graders().items() if not passes(grader, text)]
        self.assertEqual(failed, ["T1"])

    def test_a_verdict_is_read_from_its_own_block_only(self):
        text = answer({"C1": "kept", "C2": "weakened"})
        found = self.verdict_graders()
        self.assertFalse(passes(found["C1"], text))
        self.assertTrue(passes(found["C2"], text))

    def test_a_word_that_is_not_a_verdict_does_not_pass(self):
        found = self.verdict_graders()
        for word in ("split", "partly kept", "kept with caveats"):
            self.assertFalse(passes(found["T2"], answer({"T2": word})), word)

    def test_the_count_graders_want_one_verdict_line_per_conclusion(self):
        for name, ids in (("challenger-trend-scan", [i for i in RECORDED if i.startswith("C")]),
                          ("challenger-responsibility-map", [i for i in RECORDED if not i.startswith("C")])):
            count = next(g for stem, g in graders(EVALS / name).items() if stem.endswith("verdict-lines"))
            self.assertTrue(passes(count, answer({i: RECORDED[i] for i in ids})), name)
            self.assertFalse(passes(count, answer({i: RECORDED[i] for i in ids[:-1]})), name)

    def test_none_found_is_looked_for_in_the_block_of_i4(self):
        grader = graders(EVALS / "challenger-responsibility-map")["i4-none-found"]
        self.assertTrue(passes(grader, answer({"I3": "weakened", "I4": "weakened"})))
        other = "### I3\n- **Verdict:** weakened\n- **Reason:** none found.\n\n### I4\n- **Verdict:** kept\n- **Reason:** no such experiment exists.\n"
        self.assertFalse(passes(grader, other))


class BuiltFromTheNotebook(unittest.TestCase):
    def test_the_two_prompts_are_what_the_script_writes_from_the_fixtures(self):
        lab = helpers.lab()
        if lab is None:
            self.skipTest("the Poiesis Lab notebook is not on this machine (POIESIS_LAB, or ~/Poiesis Lab)")
        for name, build in (("challenger-trend-scan", eval_data.trend_scan),
                            ("challenger-responsibility-map", eval_data.responsibility_map)):
            self.assertEqual((EVALS / name / "prompt.md").read_text(encoding="utf-8"), build(lab), name)

    def test_each_prompt_holds_its_conclusions_and_no_verdict(self):
        for name, ids in (("challenger-trend-scan", "C"), ("challenger-responsibility-map", "IT")):
            _, body = parts(EVALS / name / "prompt.md")
            listed = re.findall(r"^- \*\*([CIT]\d):\*\*", body, re.M)
            self.assertEqual(listed, [id_ for id_ in RECORDED if id_[0] in ids])
            for word in ("weakened", "narrower", "verdict"):       # the prompt must not tell the agent the verdicts
                self.assertFalse(word in body.lower(), f"{name}: the prompt says \"{word}\"")


if __name__ == "__main__":
    unittest.main()
