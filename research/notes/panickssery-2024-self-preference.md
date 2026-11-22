# LLM Evaluators Recognize and Favor Their Own Generations (Panickssery, Bowman & Feng, 2024)

- **Source:** arXiv:2404.13076v1, 15 April 2024 · https://arxiv.org/abs/2404.13076 (a preprint; pages = PDF pages)
- **File:** `../papers/panickssery-2024-self-preference.pdf`
- **Licence:** on arXiv; its licence was not checked: local only.
- **Evidence:** empirical · three models (Llama-2-7b-chat, GPT-3.5, GPT-4) judging summaries of 1,000 news articles from each of two datasets, as written by themselves, by the other models and by people; fine-tuning to raise or lower self-recognition (p. 2, 5).
- **Read:** full text of the paper, p. 1–8. Not read: the appendixes, p. 11–21 · 2026-11-22

## What it says
- Self-preference: a model scores its own outputs higher than others' while human annotators judge them equal in quality (p. 1).
- On two summarization tasks the three models favoured summaries they had written over those of other models and of people (p. 2).
- Without fine-tuning the models told their own text from others' above chance; GPT-4 was right 73.5% of the time (p. 2).
- After fine-tuning, the strength of self-preference rose in a straight line with the ability to recognize one's own text (p. 1, 5).
- A consequence the authors draw: a model's rating can be inflated because it is most similar to the model that evaluates it, which weakens oversight (p. 7).
- Limits the authors state: the evidence supports the causal reading without fully validating it; the true quality of the summaries was not controlled, and a preference for one's own text can be justified when it is better; one task; another study found the opposite order between GPT-4 and GPT-3.5 (p. 6, 7).

## What it means for the plugin
- The `challenger` agent runs on a model of the same family as the session that wrote the conclusions. A judge from the same family may favour what a session like itself wrote: that is the reason a person checks a sample of claims against their sources.
- This is an inference, not a finding of the paper: it studied quality ratings of summaries by three models of 2023. It did not study checking a claim against its source, and it did not study Claude models.

## Quotes
- "an LLM evaluator scores its own outputs higher than others’ while human annotators consider them of equal quality" (p. 1)
- "GPT-4 is 73.5% accurate distinguishing itself from two other LLMs and humans" (p. 2)
- "contrary to our findings" (p. 6)
- "a model’s rating can be inflated simply because it’s most similar to the model used for evaluation" (p. 7)
- "our experiments can only provide evidence towards the causal hypothesis without fully validating it" (p. 7)
- "Self-preference can be justifiable if the LLM’s generation is indeed higher quality than the alternative" (p. 7)
