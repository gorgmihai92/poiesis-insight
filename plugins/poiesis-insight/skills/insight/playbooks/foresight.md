# Foresight

What is emerging and what may come: signals, horizons, scenarios and dated forecasts. It opens possibilities and
makes them testable; it does not predict one future.

## Signals
Collect signals from the input (and, if the user asks, from new research via the research plugin). Log each one with
`templates/signal.md`, keeping three things apart (Hiltunen 2008): the **signal** (what was observed, how visible),
the **issue** (how widespread), the **interpretation** (what it might mean to us). A weak signal is low on
visibility and spread; it is not yet a trend.

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

## Save
`foresight/<YYYY-MM-DD>-<topic>.md`: signals, horizons, layers, scenarios, what survived the challenge, and the
forecasts added to the log.
