# Eval cases

Six cases for `claude plugin eval`. Two put the 16 first-pass conclusions of the lab's two recorded runs
(2026-11-17) to the `challenger` agent, with the runs' own numbers. Four are rules of this plugin, three of them
drawn from what went wrong in those runs.

| Case | Passes when |
|---|---|
| `challenger-trend-scan` | the agent answers with one block per conclusion, and none of C1 to C6 is kept: all six were weakened in the recorded run |
| `challenger-responsibility-map` | none of I1 to I5, T2, T3 and T4 is kept, T1 is not dropped, T5 is dropped, and I4 becomes "none found" |
| `verdict-copied-not-retyped` | a weakened verdict stays weakened when the user asks for a cleaner label |
| `new-challenge-after-method-change` | a changed base and a changed sentence call for a new challenge, not for the old label |
| `gap-before-question` | a gap is described by where and why the evidence falls short, and "nobody has studied it" becomes "none found" |
| `method-pattern-is-counted` | a finding that rests on one method is written with the method in it, and the method is counted |

**No case has been run.** They were written on 2026-11-22 in the layout `claude plugin eval init --bare` gives
(`prompt.md` and `graders/*.md`), with fields and grader types from the documentation's reference as read that
day (`research/notes/claude-code-2026-plugin-evals.md` in the repository).

## What the two challenger cases measure, and what they do not
- Each of the 16 conclusions has its own `regex` grader on the `**Verdict:**` line of its block, so a case's score
  is the share of conclusions on which the agent agrees with the recorded run. `regex` graders cost nothing.
- The recorded verdicts are one run of the same agent on a Sonnet model. They are not ground truth. The graders
  are set where the data in the prompt decide the matter: a conclusion the numbers contradict must not be kept,
  the one that held must not be dropped. A challenger that keeps everything fails 15 of 16; one that drops
  everything fails 1.
- The recorded run's one "split" verdict (T2) is graded as weakened or dropped, with a judge checking that its two
  parts are told apart: a stamp has three verdicts.
- The prompts are written by `tests/eval_data.py` from the notebook's `fixtures/`, and a test checks them
  against it, so no number in them was retyped.
- In the runs without the plugin the agent does not exist, and its call fails. That is expected: these two cases
  say how the agent does, not how much the plugin adds.

## Running them
Each run is a real model call, and each `llm` grader calls a judge model three times. From the plugin's folder:

```
claude plugin eval . --no-publish --max-cost-usd 5
claude plugin eval . --case verdict-copied-not-retyped --no-publish
claude plugin eval . --tag challenger --ablation none --no-publish
```

- Without `--no-publish` the command publishes its report to claude.ai when the account allows it.
- `--max-cost-usd` stops the run at a ceiling. `--ablation none` skips the runs without the plugin.
- Every case asks for one run (`runs: 1`): a first pass is six runs with the plugin, six without, and the judges
  of six `llm` graders. `--runs 3` gives a steadier score.
- The two challenger cases start a subagent, so they take longer: `timeout_seconds` is 1500.
- Sign the Claude command line in first with `claude auth login`. A sign-in in the desktop app does not reach it.
