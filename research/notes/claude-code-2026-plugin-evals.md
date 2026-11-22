# Test plugins with evals (Claude Code documentation, 2026)

- **Source:** Claude Code documentation · https://code.claude.com/docs/en/plugin-evals
- **File:** `../papers/claude-code-2026-plugin-evals.txt` (the page's Markdown as served on 2026-11-22; no page numbers, so sections are cited)
- **Licence:** documentation of Anthropic. The text is kept on the machine that read it.
- **Evidence:** documentation: what the tool is said to do. With it: the help of `claude plugin eval` and of `claude plugin eval init` in Claude Code 2.1.311, and the blank case `claude plugin eval init --bare` wrote on 2026-11-22.
- **Read:** part of the page: "How an eval run works", "Write a case manually", "Set run limits and tools in prompt.md", "Choose and weight graders", "Score against the no-plugin baseline", "Seed the workspace or conversation", "Grant tools", "How runs are isolated", "Eval suite reference" (the `prompt.md` fields, the `case.yaml` fields, grader frontmatter and grader types), and the troubleshooting entry on a plugin's agents. Not read: the quickstart, mocks, CI, reading the results, the other troubleshooting entries · 2026-11-22

## What it says
- A case is a folder with `prompt.md` (frontmatter and the prompt) and `graders/<name>.md`, one check each. The blank case holds `max_turns`, `allowed_tools` and one `llm` grader ("Write a case manually"; the blank case).
- Each run starts in an empty folder with only the plugin loaded: no user settings, no `CLAUDE.md`, no other plugin ("How runs are isolated").
- A run's score is the share of its graders that passed; a case runs three times unless `runs` says otherwise, and again without the plugin for a baseline ("How a case is scored").
- Only read-only tools a case lists are granted, `Agent` among them. `Bash`, `Write`, `Edit`, `WebFetch` and `WebSearch` need a grant on the command line ("Grant tools").
- A case that lists `Agent` can dispatch a plugin's agent by its namespaced name. In the baseline runs that agent does not exist, and the call fails as expected (troubleshooting).
- Grader types: `regex`, `tool_used`, `tool_order`, `file_exists` cost nothing; `llm` and `baseline` call a judge model. A `regex` grader looks at the last message unless `target` says otherwise. `arm: with-only` keeps a grader out of the two-arm score ("Grader types", "Score against the no-plugin baseline").
- Each run with the plugin, each baseline run and each judge call is a model call ("How a case is scored").

## What it means for the plugin
- The eval cases in `plugins/poiesis-insight/evals/` use this layout and only fields and grader types named in the reference.
- The cases that measure the `challenger` list `Agent` and grade the structured verdict with `regex` graders, which cost nothing.
- Nothing here was observed in a run: the cases were written and not run.

## Quotes
- "Each run starts in an empty working directory"
- "A run's score is the fraction of its graders that passed"
- "There are no custom-code graders."
- "can dispatch one of your plugin's agents by its namespaced name"
