# Eval cases

Six cases for `claude plugin eval`. Two put 15 first-pass conclusions to the `challenger` agent: the six of the
lab's recorded trend scan (2026-11-17), with the run's own numbers, and nine in a synthetic case on a neutral
subject (coastal flood defence), with studies and counts made up for the test. Four are rules of this plugin,
three of them drawn from what went wrong in the recorded runs.

| Case | Passes when |
|---|---|
| `challenger-trend-scan` | the agent answers with one block per conclusion, and none of C1 to C6 is kept: all six were weakened in the recorded run |
| `challenger-synthetic-map` | synthetic, for the test: none of I1 to I4 and T2 to T5 is kept, I4 and T4 are dropped, T1 is not dropped, T2 is weakened with its two parts told apart, and I3 becomes "none found" |
| `verdict-copied-not-retyped` | a weakened verdict stays weakened when the user asks for a cleaner label |
| `new-challenge-after-method-change` | a changed base and a changed sentence call for a new challenge, not for the old label |
| `gap-before-question` | a gap is described by where and why the evidence falls short, and "nobody has studied it" becomes "none found" |
| `method-pattern-is-counted` | a finding that rests on one method is written with the method in it, and the method is counted |

**No case has been run.** They were written on 2026-11-22 in the layout `claude plugin eval init --bare` gives
(`prompt.md` and `graders/*.md`), with fields and grader types from the documentation's reference as read that
day (`research/notes/claude-code-2026-plugin-evals.md` in the repository).

## What the two challenger cases measure, and what they do not
- Each of the 15 conclusions has its own `regex` grader on the `**Verdict:**` line of its block, so a case's score
  is the share of conclusions on which the agent agrees with the expected verdicts. `regex` graders cost nothing.
- The trend-scan verdicts are one recorded run of the same agent on a Sonnet model. They are not ground truth.
  The graders are set where the data in the prompt decide the matter: a conclusion the numbers contradict must not
  be kept, the one that held must not be dropped.
- The synthetic case's studies and counts were made up for the test on 2026-11-26 (synthetic, for the test): they
  stand for no real study, database or run, and its prompt says so. Its expected verdicts follow from those data,
  and `tests/test_evals.py` checks the facts that decide each one (one marsh study of six found no change; the two
  studies that compare dunes and seawalls disagree; no study reports maintenance costs; one unread preprint is the
  only item for I4; T2's forecasting part rises in 2025 alone; T4 meets its rule on about two works expected, and
  one fewer fails it). No run has checked that the agent reaches them.
- Across the two cases, a challenger that keeps everything fails 14 of 15; one that drops everything fails 2 (T1,
  and T2, which has a part that holds).
- T2 joins two claims, one that holds and one that does not. It is graded as weakened, with a judge checking that
  its two parts are told apart: a stamp has three verdicts.
- The trend-scan prompt is written by `tests/eval_data.py` from the notebook's `fixtures/`, and a test checks it
  against them, so no number in it was retyped. The synthetic prompt is written by `tests/synthetic_map.py`, which
  computes every share, growth rate, impact and median from the made-up raw counts; a test checks the prompt
  against it.
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
