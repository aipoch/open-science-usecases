# In a Year's Worth of Weather Forecasts, Are Predictions of ‘Sunny’ Weather More Accurate, or Are Predictions of ‘Rain’ More Accurate?

## Research question

How can unequal rain and sunshine base rates distort an apparent accuracy comparison?

Examines the sunny and rainy base rates in Kunming during 2024 using Open-Meteo weather data. The archived output includes annual and monthly condition tables and a climatology report.

## Data and comparison design

First count the observed conditions in the same city and year, then establish whether an independently issued forecast archive exists. True verification requires forecast–observation pairs made before the weather occurred; reanalysis cannot replace the forecast.

## Recorded findings

### Kunming 2024 — Climatology analysis (base rates)

I pulled a full year (366 days, 2024) of observed weather for Kunming from Open-Meteo and produced the base-rate analysis that underlies the stated question.

### Key numbers

| Condition | Days | Share of year |
|---|---|---|
| **Rain** | 258 | **70.5%** |
| Cloudy | 79 | 21.6% |
| **Sunny** | 28 | **7.7%** |
| Snow | 1 | 0.3% |

Mean daily precipitation **3.74 mm**; wet days (≥0.1 mm) **259 (70.8%)**.

### Why this matters for "sunny vs. rain accuracy"

In Kunming, **rain outnumbers sunny ~9:1**. So a naive "always predict rain" forecaster would be ~70% correct with **zero skill**, while "sunny" is a rare event that a forecast must actively discriminate. This base-rate asymmetry is exactly why raw hit rate can't answer the stated question — it needs a **skill score** against genuine advance forecasts.

### Why the archive does not provide actual hit/false-alarm rates (honest limitation)


## What the comparison shows

An always-rain rule can look accurate in a rain-dominated dataset while having no discrimination skill.

## Assumptions and limits

The available endpoints did not provide an independent operational forecast archive. This case describes weather-condition base rates, not a completed comparison of forecast accuracy; hit and false-alarm rates require genuine advance forecasts paired with observations.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from Hugging Face snapshot `b0218fea4fc3fc9aa37ac616aba20e619e242c1e`. The package contains the archived conversation, session metadata, and resources listed in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this reorganization.
