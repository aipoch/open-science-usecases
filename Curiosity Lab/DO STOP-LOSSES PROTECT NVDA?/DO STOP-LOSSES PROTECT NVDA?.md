# DO STOP-LOSSES PROTECT NVDA?

## Research question

How do tighter stop rules change both downside exposure and time invested?

## Data and method

Use adjusted OHLC data and a high-water mark known before the current day. Execute stop signals and moving-average re-entry at the next open, record turnover fees, and compare multiple trailing thresholds with buy-and-hold.

## Recorded findings

Backtests several trailing-stop thresholds against holding NVIDIA using supplied adjusted prices. The final record includes next-open exits, moving-average re-entry, fees, and a trade log.

In the archived window, tighter stops reduce reported drawdown but also create many exits and lower ending wealth. The 5% rule has 74 exits and finishes near $12,187 versus roughly $313,543 for buy-and-hold.

## What the findings mean

Lower drawdown and higher terminal return are different objectives. Results depend on gaps, next-open execution, re-entry rules, costs, and the particular trending market.

## Interpretation and limits

The final implementation uses daily lows against the prior adjusted high-water mark. Historical performance is conditional on that timing rule, price adjustments, and costs; it does not guarantee protection against future losses.

## Package and provenance

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.

## Import provenance

This introduction was imported from the GitHub case description. The archived export and poster retain their original contents. This reorganization did not rerun the study or independently reverify its external sources or conclusions.
