# What Follows a Bitcoin Surge?

## Research question

How should a post-surge return question be defined before inspecting its outcomes?

Explores a method for studying Bitcoin returns 30 days after a large single-day price increase, using a predefined surge threshold and event-based return analysis. The session records the proposed methodology and analysis script.

## Data and comparison design

Fix the surge threshold, event date, 30-day return convention, and treatment of overlapping events. Save the event list and analysis logic so the result cannot be driven by retrospectively choosing only favorable surges.

## Recorded findings

| Analysis component | Definition or status | Interpretation |
| --- | --- | --- |
| Event rule | Identify a qualifying Bitcoin surge from price history | Must be fixed before looking at later returns. |
| Outcome window | Compare returns after each qualifying event | Overlapping windows are not independent trades. |
| Archived output | Methodology and analysis script | Provides the intended computation. |
| Verified directional result | Not established in the current introduction | No newly asserted positive-return probability is added. |

The archive contains the methodology and analysis script, but this draft does not add a verified positive-return claim that was absent from the current introduction.

A defensible event study would identify the event rule before examining forward returns, retain all qualifying events, and compare a specified forward horizon with a relevant baseline. The saved methodology and script explain that intended computation. Data-access and runtime problems in the conversation do not themselves imply anything about post-surge returns. This revision therefore adds the analysis design and dependencies but no fabricated event count, average return or positive-return probability.

## What the comparison shows

A return distribution depends on data coverage, thresholds, fees, and regime. An event study is not automatically a profitable trading strategy.

## Assumptions and limits

The archived question and analysis plan do not by themselves establish profitable post-surge returns. Data availability, event thresholds, overlapping windows, fees, and market regime must be checked before interpreting a backtest. This introduction does not present an independently validated trading result.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from Hugging Face snapshot `b0218fea4fc3fc9aa37ac616aba20e619e242c1e`. The package contains the archived conversation, session metadata, and resources listed in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this reorganization.
