# Monthly rotation of best-performing assets vs. buy-and-hold

## Research question

What does a trailing-return rotation rule do when it cannot see future prices?

Constructs a monthly asset-rotation example using trailing information and compares it with equal-weight buy-and-hold. The archive records selected assets, data cutoffs, and strategy calculations.

## Data and comparison design

The analysis uses the recorded fictional eight-asset, 240-month history; choose the top two using only the preceding 12 months, retain the warm-up period, and apply returns after the decision. Compare with an equal-weight holding rule on the same simulated paths.

## Recorded findings

### Does rotating "best-performing" assets each month mean buying at market peaks?

**Short answer: only in the naive (flawed) version of the idea. A correctly implemented monthly rotation uses *trailing* (point-in-time) returns, so it tends to buy assets that are still rising — it is *not* systematically buying tops.** The "buying at peaks" worry usually comes from a look-ahead/survivorship error, not from the strategy itself.

### What I built
Since there was no market data in the workspace, I generated a realistic simulated history of **8 assets over 240 months (2005–2024)** with distinct drift/volatility and slowly rotating leadership, then backtested two strategies using only data known at each decision date:

- **Buy & Hold** — equal-weight across all assets.
- **Monthly Rotation** — each month hold the top-2 assets by trailing 12-month return (known at that date); first 12 months are a warm-up period where the strategy holds cash because it lacks history.

Both strategies earn the return realized *after* the rebalance decision — **no look-ahead bias**.

### Results (synthetic data)

| Strategy | Total return | CAGR | Ann. vol | Sharpe | Max DD |
|---|---|---|---|---|---|
| Buy & Hold (equal-weight) | 193% | 5.6% | 6.8% | 0.83 | −14.8% |
| Monthly Rotation (top-2 of 12mo) | 242% | 6.4% | 12.5% | 0.56 | −24.5% |

### The "buying at peak" evidence
Across all genuine rotation decisions (excluding warm-up), the diagnostic measured each purchase price against the asset's trailing high:

- **36%** of selections bought at ≥98% of their trailing high (i.e. near a local top).
- **Mean buy price = 90.6%** of the trailing high — the median purchase is *not* at the peak.

So the strategy does occasionally buy near highs, but that is the expected price of *momentum*: it holds winners while they continue to win. On average it buys below the trailing peak, not at it.

### Caveats (important)
1. **Synthetic data.** These numbers illustrate the *methodology*; they are not real market returns. The correct way to answer the stated question for real assets is to run this exact point-in-time framework on real price history.
2. **No costs.** Rotation trades monthly; transaction costs, taxes, and slippage are not modeled and would reduce the rotation edge.
3. **Higher risk.** Rotation had higher volatility and a deeper drawdown than buy-and-hold — the higher return is partly risk compensation.
4. **Momentum ≠ peaks, but it can chase reversals.** If markets mean-revert sharply, a trailing-return rule can buy just before a top. That is the genuine, irreducible risk in this strategy — and it's exactly what the stated question is probing.


## What the comparison shows

No-look-ahead accounting is necessary but not sufficient for realistic investing. Asset selection, market construction, costs, and turnover still determine the result.

## Assumptions and limits

The market history is simulated, not downloaded historical prices. This illustrates point-in-time decision rules and look-ahead concerns, not evidence that rotation reliably outperforms in real markets.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
