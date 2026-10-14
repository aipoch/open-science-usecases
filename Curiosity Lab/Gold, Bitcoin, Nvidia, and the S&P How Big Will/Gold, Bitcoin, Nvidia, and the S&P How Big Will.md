# Gold, Bitcoin, Nvidia, and the S&P How Big Will

## Research question

How do return rankings change when risk is displayed beside terminal growth?

Aligns gold, Bitcoin, NVIDIA, and an S&P proxy over a common historical window and compares returns, volatility, and drawdowns. The archive retains calculation files, curves, and data-alignment assumptions.

## Data and comparison design

Align all four series over January 6, 2023–January 6, 2026, distinguish adjusted equities from spot prices, and rebase to a common index. Report total and annualized returns, volatility, and peak-to-trough drawdown on the same window.

## Recorded findings

### Main findings

For the common three-year window, January 6, 2023–January 6, 2026:

| Asset | Total return | Annualized return | Volatility | Max drawdown |
|---|---:|---:|---:|---:|
| NVIDIA | 1,160.03% | 132.65% | 50.02% | −36.89% |
| Bitcoin | 452.22% | 76.73% | 46.40% | −31.94% |
| Gold | 140.44% | 33.96% | 16.56% | −11.30% |
| S&P 500 proxy | 85.45% | 22.85% | 15.30% | −18.76% |

NVIDIA’s lead over the S&P 500 proxy reached 1,074.58 percentage points. It led Bitcoin by 707.81 points and gold by 1,019.59 points. Bitcoin beat the S&P proxy by 366.77 points, while gold beat it by 54.99 points.

The outsized NVIDIA and Bitcoin returns came with roughly three times the volatility of gold or the S&P proxy. Gold delivered the smallest drawdown and lowest volatility.

Prices were placed on a calendar-daily index, forward-filled only from prior observations, and rebased to 100. NVIDIA and SPY use split- and dividend-adjusted prices; spot gold and Bitcoin require no corporate-action adjustment. SPY represents the S&P 500, while gold is spot XAU/USD. Source methodology and adjustment documentation are available from the [TradeSmart dataset](https://github.com/revred/TradeSmart.Tracker) and [NVIDIA dataset](https://github.com/yennanliu/finance_data/blob/main/data/prices/nvda.csv).

This measures a historical gap—it does not predict how large the next three-year gap will be.

## What the comparison shows

A common calendar is essential, but forward-filled nontrading days still affect the interpretation of daily volatility. This is a historical risk-return comparison.

## Assumptions and limits

Calendar alignment and forward filling affect the comparison. Despite the forward-looking title, this is a historical backtest, not an estimate of the next three years.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
