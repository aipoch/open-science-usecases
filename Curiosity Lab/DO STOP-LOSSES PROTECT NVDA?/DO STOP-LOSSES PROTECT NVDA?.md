# DO STOP-LOSSES PROTECT NVDA?

## Research question

How do tighter stop rules change both downside exposure and time invested?

Backtests several trailing-stop thresholds against holding NVIDIA using supplied adjusted prices. The final record includes next-open exits, moving-average re-entry, fees, and a trade log.

## Data and comparison design

The analysis uses adjusted OHLC data and a high-water mark known before the current day. Execute stop signals and moving-average re-entry at the next open, record turnover fees, and compare multiple trailing thresholds with buy-and-hold.

## Recorded findings

Completed using the supplied 1,508 trading sessions. Stops use each day’s low versus the prior day’s adjusted high-water mark; exits and SMA-crossover re-entries execute next open.

| Strategy | Ending value | Max drawdown | Exits | Re-entries | Fees |
|---|---:|---:|---:|---:|---:|
| Buy and hold | $313,542.64 | -66.34% | 0 | 0 | $10.00 |
| 5% trailing stop | $12,186.79 | -51.97% | 74 | 74 | $2,202.10 |
| 10% trailing stop | $40,719.66 | -52.81% | 47 | 47 | $2,291.41 |
| 15% trailing stop | $122,471.40 | -56.61% | 29 | 29 | $3,541.42 |
| 20% trailing stop | $111,317.32 | -58.75% | 20 | 20 | $1,980.23 |

The 5% strategy’s first stop was signaled from the prior peak and sold on 2020-01-28; its first re-entry was 2020-01-29. The full 345-row trade log is included below. The notebook now has executable Python cells.

## What the comparison shows

Lower drawdown and higher terminal return are different objectives. Results depend on gaps, next-open execution, re-entry rules, costs, and the particular trending market.

## Assumptions and limits

The final implementation uses daily lows against the prior adjusted high-water mark. Historical performance is conditional on that timing rule, price adjustments, and costs; it does not guarantee protection against future losses.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
