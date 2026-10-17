# Foresight

What is emerging and what may come: signals, horizons, scenarios and dated forecasts. It opens possibilities and
makes them testable; it does not predict one future.

## Signals
Collect signals from the input (and, if the user asks, from new research via the research plugin). Log each one with
`templates/signal.md`, keeping three things apart (Hiltunen 2008): the **signal** (what was observed, how visible),
the **issue** (how widespread), the **interpretation** (what it might mean to us). A weak signal is low on
visibility and spread; it is not yet a trend.

## Trends in data
When the data have a time order (survey waves, usage logs, metrics), a trend is reported only after three checks:
- **Signal or noise:** is the change larger than the series' usual variation? Draw the series with its mean and
  limits at about three standard deviations, and look for points outside them or a long run on one side
  (control charts; Benneyan et al. 2003). Say how many points the series has; a few points give a lead, not a trend.
- **Base rate:** how often do similar changes, in similar series or past periods, continue? Start the forecast from
  that outside view and adjust it, not from the story of this case (Kahneman & Lovallo 1993).
- **Shape:** steady, speeding up, slowing down or leveling off; seasonal; a sudden break. Extrapolate only as a
  dated forecast in the log, never as a statement.

## Horizons (Sharpe et al. 2016)
Place each pattern: **H1** the current way, losing its fit; **H3** an emerging pattern on the fringes; **H2** the
transitional innovations, either feeding H3 (H2+) or being absorbed back into H1 (H2−). All three exist at once.

## Uncommon conclusions: read the layers (Inayatullah 1998)
For the main issue, write four readings: the **litany** (the headline trend), the **social causes**, the
**worldview** behind them, the **myth or metaphor**. Conclusions that only appear at the deeper layers are the
uncommon ones; they still go through `playbooks/challenge.md`.

## Scenarios (Phadnis et al. 2015)
Two to four scenarios built on the most uncertain, most important drivers. Report what holds across all scenarios
(robust) and what depends on one (contingent); scenarios guide flexible choices, they are not forecasts.

## Forecasts (Mellers et al. 2015)
Where a claim can be checked later, write it as a forecast: a precise question, a probability, a date to resolve
it. Add it to `foresight/forecasts.md` (`templates/forecasts.md`). When dates pass, score them:
`python3 -I $S/forecasts.py foresight/forecasts.md`. Scores show which reasoning to trust next time.

## Save (see SKILL.md, "Saving")
`foresight/<YYYY-MM-DD>-<topic>.md`: signals, horizons, layers, scenarios, what survived the challenge, and the
forecasts added to the log.
