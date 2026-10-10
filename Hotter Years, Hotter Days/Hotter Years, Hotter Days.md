# Hotter Years, Hotter Days?

## Research topic and question

- Can the Hottest Ten Days Reveal What Averages Hide?

Do a year’s ten hottest days reveal warming more clearly than its average temperature? Investigate New York’s Central Park using the latest available NOAA GHCN-Daily data (station USW00094728), starting in 1991. Download the data from https://www.ncei.noaa.gov/pub/data/ghcn/daily/ and use its documentation. Compare complete years and explain the evidence and limitations in English.

## Research findings

The conclusion holds for Central Park during 1991–2025 after accounting for correlation between years and using a robust trend estimator.

| Metric | Newey–West OLS slope | 95% HAC CI | Theil–Sen slope | 95% CI |
|---|---:|---:|---:|---:|
| Annual mean temperature | **+0.305 °C/decade** | +0.159 to +0.452 | **+0.323 °C/decade** | +0.059 to +0.550 |
| Mean of ten hottest maxima | −0.164 °C/decade | −0.451 to +0.123 | −0.241 °C/decade | −0.736 to +0.400 |

Newey–West inference used three annual lags. The annual-mean trend remains clearly positive (`p = 0.00005`), whereas the hot-ten trend remains statistically indistinguishable from zero (`p = 0.264`). Theil–Sen estimates give the same interpretation. The negative hot-ten estimates are not persuasive evidence of cooling because their intervals are wide and cross zero.

All 35 years from 1991 through 2025 passed the completeness and quality-flag checks.
