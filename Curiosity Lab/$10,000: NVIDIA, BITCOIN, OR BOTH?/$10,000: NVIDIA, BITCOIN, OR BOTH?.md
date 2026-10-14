# $10,000: NVIDIA, BITCOIN, OR BOTH?

## Research question

Would diversification improve the outcome of the same initial investment over the same historical dates?

Compares a $10,000 investment in NVIDIA, Bitcoin, and a 50/50 portfolio using supplied adjusted-price CSVs. The archived backtest includes monthly rebalancing, trading costs, drawdowns, a trade ledger, and rerun files.

## Data and comparison design

The analysis uses the intersection of available NVIDIA trading dates and Bitcoin observations, so all portfolios share the same start and end. Compare two single-asset portfolios with a 50/50 portfolio whose weights are restored monthly. Record each rebalance and its turnover fee instead of deducting an unexplained annual cost.

## Recorded findings

NVIDIA won over the period.

| Portfolio | Ending value | Total return | Maximum drawdown |
|---|---:|---:|---:|
| All NVDA | $312,338.99 | 3,023.39% | -66.34% |
| All Bitcoin | $125,272.64 | 1,152.73% | -76.63% |
| 50/50, monthly rebalance | $272,379.33 | 2,623.79% | -66.50% |

The split made 72 monthly rebalancing trades and paid $455.12 in modeled 0.1% turnover costs. It reduced the ending value versus all-NVDA, but substantially exceeded all-Bitcoin.

Assumptions: common NVDA trading dates (2020-01-02 to 2025-12-31); the initial 50/50 allocation has no fee; fees apply to monthly rebalancing, including the final period-end rebalance.

## What the comparison shows

The historical return winner also experienced a large interim loss. Diversification, transaction costs, and start-date choice answer different questions; one backtest does not establish a preferred future allocation.

## Assumptions and limits

The original market-data download was blocked, so the completed calculation uses user-supplied prices. Results depend on the historical window, shared trading dates, and fee assumptions; they are not a forecast.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
