"""The eval cases: written in the documented layout, built from a recorded run or from made-up data that decide
their verdicts, and never run here."""
from __future__ import annotations

import re
import unittest

import eval_data
import helpers
import synthetic_map

EVALS = helpers.PLUGIN / "evals"
CASES = sorted(path.parent for path in EVALS.glob("*/prompt.md"))
PROMPT_KEYS = {"schema_version", "name", "description", "tags", "plugins", "runs", "expected_outcome", "model",
               "max_turns", "timeout_seconds", "allowed_tools", "append_system_prompt", "env"}
GRADER_KEYS = {"regex": {"pattern", "flags", "match", "target"}, "tool_used": {"tool", "input_match", "min", "max"},
               "llm": {"criteria", "focus"}}
READ_ONLY_TOOLS = {"Read", "Glob", "Grep", "NotebookRead", "Skill", "AskUserQuestion", "Agent", "TodoWrite"}
# C1 to C6: the verdicts of the recorded trend scan. I1 to T5: the synthetic case, whose made-up data are built to
# give these verdicts (`synthetic_map.EXPECTED`; `SyntheticData` checks that the data decide them).
EXPECTED = {"C1": "weakened", "C2": "weakened", "C3": "weakened", "C4": "weakened", "C5": "weakened",
            "C6": "weakened", **synthetic_map.EXPECTED}


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
              f"- **Reason:** none found among the nine studies.\n" for id_, verdict in verdicts.items()]
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
                         ["challenger-synthetic-map", "challenger-trend-scan", "gap-before-question",
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
        for name in ("challenger-trend-scan", "challenger-synthetic-map"):
            fields, body = parts(EVALS / name / "prompt.md")
            self.assertIn("Agent", fields["allowed_tools"])
            self.assertIn("`challenger` agent", body)


class FifteenConclusions(unittest.TestCase):
    """One grader per conclusion of the two cases, on the verdict line of its block."""

    def verdict_graders(self):
        found = {}
        for name in ("challenger-trend-scan", "challenger-synthetic-map"):
            for stem, grader in graders(EVALS / name).items():
                hit = re.fullmatch(r"([cit]\d)-(?:kept|weakened|dropped)(?:-or-(?:kept|weakened|dropped))*", stem)
                if hit:
                    found[hit.group(1).upper()] = grader
        return found

    def test_every_conclusion_has_its_grader(self):
        self.assertEqual(sorted(self.verdict_graders()), sorted(EXPECTED))

    def test_the_expected_verdicts_pass_all_fifteen(self):
        text = answer(EXPECTED)
        for id_, grader in self.verdict_graders().items():
            self.assertTrue(passes(grader, text), id_)

    def test_a_challenger_that_keeps_everything_fails_fourteen(self):
        text = answer({id_: "kept" for id_ in EXPECTED})
        failed = [id_ for id_, grader in self.verdict_graders().items() if not passes(grader, text)]
        self.assertEqual(sorted(failed), sorted(set(EXPECTED) - {"T1"}))

    def test_a_challenger_that_drops_everything_fails_on_the_one_that_held_and_the_one_with_a_part_that_held(self):
        text = answer({id_: "dropped" for id_ in EXPECTED})
        failed = [id_ for id_, grader in self.verdict_graders().items() if not passes(grader, text)]
        self.assertEqual(sorted(failed), ["T1", "T2"])

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
        for name, ids in (("challenger-trend-scan", [i for i in EXPECTED if i.startswith("C")]),
                          ("challenger-synthetic-map", [i for i in EXPECTED if not i.startswith("C")])):
            count = next(g for stem, g in graders(EVALS / name).items() if stem.endswith("verdict-lines"))
            self.assertTrue(passes(count, answer({i: EXPECTED[i] for i in ids})), name)
            self.assertFalse(passes(count, answer({i: EXPECTED[i] for i in ids[:-1]})), name)

    def test_none_found_is_looked_for_in_the_block_of_i3(self):
        grader = graders(EVALS / "challenger-synthetic-map")["i3-none-found"]
        self.assertTrue(passes(grader, answer({"I2": "dropped", "I3": "weakened"})))
        other = ("### I2\n- **Verdict:** dropped\n- **Reason:** none found.\n\n### I3\n- **Verdict:** kept\n"
                 "- **Reason:** no such study exists.\n")
        self.assertFalse(passes(grader, other))


class BuiltFromTheNotebook(unittest.TestCase):
    def test_the_trend_scan_prompt_is_what_the_script_writes_from_the_fixtures(self):
        lab = helpers.lab()
        if lab is None:
            self.skipTest("the Poiesis Lab notebook is not on this machine (POIESIS_LAB, or ~/Poiesis Lab)")
        self.assertEqual((EVALS / "challenger-trend-scan" / "prompt.md").read_text(encoding="utf-8"),
                         eval_data.trend_scan(lab))

    def test_each_prompt_holds_its_conclusions_and_no_verdict(self):
        for name, ids in (("challenger-trend-scan", "C"), ("challenger-synthetic-map", "IT")):
            _, body = parts(EVALS / name / "prompt.md")
            listed = re.findall(r"^- \*\*([CIT]\d):\*\*", body, re.M)
            self.assertEqual(listed, [id_ for id_ in EXPECTED if id_[0] in ids])
            for word in ("weakened", "narrower", "verdict"):       # the prompt must not tell the agent the verdicts
                self.assertFalse(word in body.lower(), f"{name}: the prompt says \"{word}\"")


class SyntheticData(unittest.TestCase):
    """`challenger-synthetic-map`: its prompt is what `synthetic_map.py` writes from made-up data, it says it is
    synthetic, and the data decide the verdicts its graders expect."""

    CASE = EVALS / "challenger-synthetic-map"

    def test_the_prompt_is_what_the_script_writes(self):
        self.assertEqual((self.CASE / "prompt.md").read_text(encoding="utf-8"), synthetic_map.prompt())

    def test_the_case_says_it_is_synthetic_where_it_is_described_and_above_its_data(self):
        fields, body = parts(self.CASE / "prompt.md")
        self.assertTrue(unquote(fields["description"]).startswith("Synthetic, for the test:"))
        self.assertIn("synthetic", fields["tags"])
        self.assertIn("The studies and the counts below are synthetic, made for this test", body)

    def test_the_data_decide_the_expected_verdicts(self):
        failed = [name for name, holds in synthetic_map.facts().items() if not holds]
        self.assertEqual(failed, [])

    def test_every_verdict_grader_accepts_its_expected_verdict_and_refuses_kept_where_the_data_say_no(self):
        found = graders(self.CASE)
        for id_, verdict in synthetic_map.EXPECTED.items():
            grader = next(g for stem, g in found.items() if re.match(rf"{id_.lower()}-(?:kept|weakened|dropped)", stem))
            self.assertTrue(passes(grader, answer({id_: verdict})), id_)
            if verdict != "kept":
                self.assertFalse(passes(grader, answer({id_: "kept"})), id_)

    def test_the_checks_bite_when_the_data_change(self):
        topic = "Groundwater salinisation"
        works, cited = synthetic_map.TOPICS[topic]
        changes = {
            "T4 meets the rule": (topic, (works, cited - 1)),
            "T2 forecasting accelerates only with 2025": ("Storm-surge forecasting",
                                                          (synthetic_map.TOPICS["Storm-surge forecasting"][0][:-1]
                                                           + [125], 13)),
            "T3 share falls, count rises": ("Seawalls", (synthetic_map.TOPICS["Seawalls"][0][:-1] + [160], 21)),
        }
        for fact, (name, value) in changes.items():
            saved = synthetic_map.TOPICS[name]
            synthetic_map.TOPICS[name] = value
            try:
                self.assertFalse(synthetic_map.facts()[fact], fact)
            finally:
                synthetic_map.TOPICS[name] = saved
        self.assertEqual([name for name, holds in synthetic_map.facts().items() if not holds], [])


if __name__ == "__main__":
    unittest.main()
