# How early should you leave

## Research question

How much departure buffer is needed for a weekly rather than a daily reliability target?

Models commute uncertainty and departure buffers under ordinary-day and accident-day assumptions. The final corrected run compares daily lateness with a weekly reliability requirement and saves a sensitivity table.

## Data and comparison design

The comparison uses ordinary-day and accident-day travel assumptions, then distinguish a two-state mixture from a moment-matched continuous lognormal model. Translate the daily late probability into the probability of at most one late arrival across five independent mornings.

## Recorded findings

The corrected model executed successfully, and all four artifacts were overwritten from that run.

The executed code used:

- Ordinary-day mean 30 minutes, SD 5 minutes.
- Accident-day mean 60 minutes, SD 15 minutes.
- Accident probability 10% for the defended model.
- A continuous lognormal distribution moment-matched to the resulting mixture mean and variance.
- Five independent mornings.
- A weekly requirement of at most one late morning in 95% of weeks.

The run produced:

- Moment-matched mean: 33.000 minutes.
- Moment-matched SD: 11.224972 minutes.
- Daily late probability at a 52-minute buffer: 0.061811.
- Weekly success probability at 52 minutes: 0.966302, or 96.6%.
- Weekly requirement: 95%.
- Extra buffer beyond the usual 30-minute commute: 22 minutes.

The corrected sensitivity table, using a 15-minute accident-day SD, gives these buffers for 95% of weeks with at most one late morning:

| Accident probability | Two-state mixture | Continuous lognormal |
|---:|---:|---:|
| 2% | 37.8 min | 40.9 min |
| 5% | 39.2 min | 44.9 min |
| 10% | 49.2 min | 50.1 min |
| 20% | 64.5 min | 58.1 min |

Every number in the files below came from the executed Python run `notebook-run-1790674265526-2`.

## What the comparison shows

This is a constructed reliability calculation, not a measured local commute forecast. Independence and the upper tail deserve particular scrutiny.

## Assumptions and limits

The distributions and accident probability are hypothetical, inferred from a vague commute description rather than observed trips. The independent-mornings assumption and tail model materially affect the buffer.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
