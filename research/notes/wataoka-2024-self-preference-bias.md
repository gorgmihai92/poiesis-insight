# Self-Preference Bias in LLM-as-a-Judge (Wataoka, Takahashi & Ri, 2024)

- **Source:** arXiv:2410.21819v2, 21 June 2025 (first version 29 October 2024) · https://arxiv.org/abs/2410.21819 (a preprint; pages = PDF pages)
- **File:** `../papers/wataoka-2024-self-preference-bias.pdf`
- **Licence:** on arXiv; its licence was not checked: local only.
- **Evidence:** empirical · eight models judging pairs of answers from the Chatbot Arena dataset (33,000 dialogues, each pair with a human preference) (p. 4).
- **Read:** full text of the paper, p. 1–9. Not read: the reference list, p. 9–11 · 2026-11-22

## What it says
- A measure of self-preference: how much more often a judge agrees with people when people prefer the judge's own answer than when they prefer the other one (p. 3).
- GPT-4 had the largest value: it agreed with people 94.5% of the time when they preferred its answer and 42.5% when they did not, a difference of 0.520 (p. 4).
- The bias is not the same everywhere: three of the eight models had negative values, undervaluing their own answers (p. 4).
- Judges rated answers with lower perplexity (text more familiar to the judge) higher than people did, whether or not the judge had written them (p. 1, 6, 7). GPT-4 and GPT-3.5 were left out of this analysis because their perplexities could not be obtained (p. 5).
- In the cases the authors looked at, the bias was about styles of answering, not clear factual errors (p. 7).
- One mitigation they suggest: several models as judges (p. 6).

## What it means for the plugin
- A judge prefers text that is familiar to it. A challenger reading conclusions written by a model of its own family reads familiar text.
- Limit that matters here: the bias they found was about style, not factual errors, and the task was rating chat answers. That a same-family checker misses the same factual errors is not shown. The human check on a sample is a precaution and a product decision.

## Quotes
- "LLMs assign significantly higher evaluations to outputs with lower perplexity than human evaluators, regardless of whether the outputs were self-generated" (p. 1)
- "The difference between these values is 0.520" (p. 4)
- "showed negative values, indicating a reverse bias" (p. 4)
- "we excluded GPT-4 and GPT-3.5-Turbo, as perplexity values could not be obtained for these models" (p. 5)
- "one possible approach is ensemble evaluation using multiple models" (p. 6)
- "the bias was often not related to clear factual errors but rather to differences in response styles" (p. 7)
