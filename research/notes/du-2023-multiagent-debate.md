# Improving Factuality and Reasoning in Language Models through Multiagent Debate (Du, Li, Torralba, Tenenbaum & Mordatch, 2023)

- **Source:** arXiv:2305.14325v1, 23 May 2023 · https://arxiv.org/abs/2305.14325 (a preprint)
- **File:** none (reference only)
- **Licence:** on arXiv; not checked.
- **Evidence:** empirical, as the abstract describes it.
- **Read:** abstract only, from the arXiv record · 2026-11-22

## What it says (from the abstract)
- Several instances of a language model propose answers and debate them over rounds to reach a common answer.
- The authors report that this improves mathematical and strategic reasoning across a number of tasks, and the factual validity of what is generated.

## What it means for the plugin
- One of three sources read only as abstracts on whether a second model pass improves answers. This one reports that it does; [Wang et al. 2024](wang-2024-multi-agent-discussion.md) and [Smit et al. 2024](smit-2024-multi-agent-debate.md) report that it often does not.
- The three study several model instances debating answers to benchmark questions. None studies an agent that tests conclusions against a project's data. So no rule rests on them: they are the reason the `challenger` is measured on recorded conclusions (the eval cases) and not assumed to work.
