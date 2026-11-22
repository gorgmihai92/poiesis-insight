# Sources behind the rules

The sources behind the rules (each rule names its source in `skills/insight/rules.md` and the playbooks). One
note per source in `notes/`; open-licence texts in `papers/` (closed ones stay local).

Every note says how much of its source was read: the notes written for 2.0.0 in a **Read** line, the earlier
ones on their **Evidence** line ("abstract only", "reference only"). A rule that rests on an abstract or on an
observation says so where it is stated. `quote_gate.py` checks each note's quotes against the source's text
where that text is on the machine: `python3 -I plugins/poiesis-insight/skills/insight/scripts/quote_gate.py
research/notes --papers research/papers`.

- **How insights happen:** [Klein & Jarosz 2011](notes/klein-2011-naturalistic-insight.md), connections,
  contradictions, impasses; [Pirolli & Card 2005](notes/pirolli-2005-sensemaking.md), foraging and sensemaking loops.
- **Testing conclusions:** [Heuer 1999](notes/heuer-1999-intelligence-analysis.md), diagnosticity and competing
  hypotheses; [Dhami et al. 2019](notes/dhami-2019-ach-evaluation.md), ACH did not improve accuracy, consistent
  weighing did; [Nickerson 1998](notes/nickerson-1998-confirmation-bias.md), confirmation bias.
- **Analysis flexibility:** [Simmons et al. 2011](notes/simmons-2011-false-positive.md), slices fixed in advance.
- **Free search with a hold-out:** [Nosek et al. 2018](notes/nosek-2018-preregistration.md), leads vs tested
  predictions; [Gelman & Loken 2014](notes/gelman-2014-forking-paths.md), forking paths;
  [Benjamini & Hochberg 1995](notes/benjamini-1995-false-discovery-rate.md), correcting for many comparisons;
  [Anscombe 1973](notes/anscombe-1973-graphs.md), plot before summarizing.
- **Rivals for correlations:** [Simpson 1951](notes/simpson-1951-interaction.md), reversal inside subgroups;
  [Barnett et al. 2005](notes/barnett-2005-regression-to-mean.md), regression to the mean.
- **Limits of intuition and patterns:** [Kahneman & Klein 2009](notes/kahneman-2009-intuitive-expertise.md);
  [Whitson & Galinsky 2008](notes/whitson-2008-illusory-patterns.md), illusory patterns (contested).
- **Research questions:** [Alvesson & Sandberg 2011](notes/alvesson-2011-problematization.md), five types of
  assumption to contest (full text); [Sandberg & Alvesson 2011](notes/sandberg-2011-gap-spotting.md), three kinds
  of gap (part of the text); [Robinson et al. 2011](notes/robinson-2011-research-gaps-framework.md), a gap
  described by where and why the evidence falls short (part of the report).
- **A person checks a sample:** [Panickssery et al. 2024](notes/panickssery-2024-self-preference.md), a model
  favours its own text (full text); [Wataoka et al. 2024](notes/wataoka-2024-self-preference-bias.md), a judge
  favours familiar text (full text).
- **Measuring the challenger and not assuming it works:** [Du et al. 2023](notes/du-2023-multiagent-debate.md),
  [Wang et al. 2024](notes/wang-2024-multi-agent-discussion.md), [Smit et al. 2024](notes/smit-2024-multi-agent-debate.md):
  mixed results on a second model pass (abstracts only);
  [Claude Code documentation 2026](notes/claude-code-2026-plugin-evals.md), the format of an eval case.
- **Ids, From and the challenge stamp:** [W3C 2013](notes/w3c-2013-prov-dm.md), entity and derivation (part of
  the text); [the lab's two recorded runs](notes/poiesis-lab-2026-recorded-runs.md), what went wrong when nothing
  recorded a verdict (observation).
- **Foresight:** [Hiltunen 2008](notes/hiltunen-2008-future-sign.md), weak signals;
  [Sharpe et al. 2016](notes/sharpe-2016-three-horizons.md), three horizons;
  [Inayatullah 1998](notes/inayatullah-1998-causal-layered-analysis.md), causal layered analysis;
  [Phadnis et al. 2015](notes/phadnis-2015-scenario-planning.md), what scenarios do;
  [Mellers et al. 2015](notes/mellers-2015-superforecasters.md), scored forecasts.
- **Trends in data:** [Benneyan et al. 2003](notes/benneyan-2003-control-charts.md), signal vs noise (control
  charts); [Kahneman & Lovallo 1993](notes/kahneman-1993-outside-view.md), base rates (the outside view).
