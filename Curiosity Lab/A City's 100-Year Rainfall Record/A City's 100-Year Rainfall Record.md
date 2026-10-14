# A City's 100-Year Rainfall Record

## Research question

Are heavy-rain events becoming more frequent, or is a larger fraction of annual rain falling in the very largest storms?

Examines heavy-rain frequency and the share of annual precipitation concentrated in heavy events using the Central Park rainfall series. The archive records coverage checks, alternative thresholds, trend calculations, and exported tables.

## Data and comparison design

Aggregate the Central Park daily series only after checking annual coverage. Compare a baseline 95th-percentile heavy-day definition with a fixed 25 mm threshold. Separately calculate heavy-day frequency, the heavy-day share of annual rain, wettest-day and wettest-five-day shares, and monthly concentration.

## Recorded findings

| Rainfall measure | Archived trend per decade | Interpretation |
| --- | --- | --- |
| Heavy-day frequency | +0.32 percentage points | Heavy days become a larger fraction of observed days. |
| Heavy-rainfall share | +1.05 percentage points | More annual rain falls on broadly defined heavy days. |
| Wettest one-day / five-day share | No clear trend | The result is not concentration into only a few exceptional storms. |
| Monthly concentration | No clear trend | Seasonal concentration is a separate question. |
| Analyzed coverage | 96 complete years, 1925–2020 | Annual completeness is checked before trend fitting. |

The 96 complete years from 1925–2020 indicate that heavy rainfall became more prominent:

- Baseline-95th-percentile heavy-day frequency increased by **0.32 percentage points per decade** (95% bootstrap CI: 0.14–0.52; Mann–Kendall p=0.0098).
- Heavy days’ share of annual precipitation increased by **1.05 percentage points per decade** (CI: 0.36–1.77; p=0.021).
- The ≥25 mm definition produced similar increases.
- No clear trend appeared in the wettest-one-day share, wettest-five-day share, or monthly precipitation concentration index.

Thus, rainfall became more concentrated in broadly defined heavy events, but not demonstrably concentrated into only the year’s few largest storms.

The analysis uses Central Park station `USW00094728`, independently identified in [NOAA’s station catalogue](https://www.ncdc.noaa.gov/cdo-web/datasets/GHCND/stations/GHCND%3AUSW00094728/detail). Because notebook networking failed, daily values came from a [public GitHub copy of the NOAA series](https://github.com/saidakhamidova/NYC-Precipitation-and-Global-Temperature-Correlation-A-Climate-Change-Indicator/blob/main/NOAA-NYC-PRCP.csv). I reversed that copy’s erroneous Fahrenheit-style transformation before analysis. The incomplete 2021 record was exported but excluded from trends.

## What the comparison shows

More rain on broadly defined heavy days is not the same as concentration into only a handful of exceptional storms. The supplied mirror required a documented reversal of an erroneous unit transformation.

## Assumptions and limits

The daily series came from a public copy after direct access failed, with a documented transformation reversed before analysis. Different concentration metrics gave different conclusions; this is one station, not a global attribution study.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
