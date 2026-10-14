# If a rigged coin is mixed in with twenty coins, how many tosses does it take to catch it

## Research question

How do bias strength and the number of competing coins affect identification?

Simulates finding one biased coin among twenty fair coins by comparing head counts. The archive varies bias and toss count and estimates identification probability under a fixed tie-breaking rule.

## Data and comparison design

Simulate 20 fair coins and one specified biased coin, apply the same toss count to each, select the largest head count, and resolve ties uniformly. Increase counts on a recorded grid and evaluate identification probability over repeated trials.

## Recorded findings

There is no unique answer unless the coin’s bias and required confidence are specified.

Using a constructed rigged coin with `P(heads) = 0.75`, 20 fair coins, and a 95% identification target, the simulation requires approximately:

**55 tosses per coin**, or **1,155 total tosses** across all 21 coins.

The coin with the most heads was selected; ties were resolved uniformly. Results used 50,000 Monte Carlo trials:

| Rigged `P(H)` | Tosses per coin | Total tosses | Detection probability |
|---:|---:|---:|---:|
| 0.60 | 350 | 7,350 | 95.25% |
| 0.70 | 85 | 1,785 | 95.37% |
| 0.75 | 55 | 1,155 | 96.04% |
| 0.80 | 35 | 735 | 95.62% |
| 0.90 | 17 | 357 | 95.21% |

These are approximate first crossings on the simulated toss-count grid, not universal exact minima. No included script was visible, so I supplied a reproducible replacement.

## What the comparison shows

The grid crossing is approximate and depends on the selection rule. It is not an exact universal sample-size requirement.

## Assumptions and limits

The reported counts are approximate crossings on a simulated grid, not universal exact sample-size minima. The answer depends on bias, confidence target, selection rule, and the number of coins.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
