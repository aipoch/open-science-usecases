# Can We Forecast Mauna Loa's CO2

## Research question

Does a seasonal time-series model improve on simple CO2 forecasts at each prediction horizon?

## Data and method

Compare SARIMA with the seasonal-drift baseline separately at one, six and twelve months. Assess both point errors and interval coverage: a narrow interval is only useful if its stated probability matches how often later observations fall inside it.

## Recorded findings

Analyzes Mauna Loa monthly CO2 and evaluates forecasts against simple baselines. Annual means rose from **315.98 ppm in 1959 to 427.35 ppm in 2025**. SARIMA had lower errors than seasonal drift at one- and six-month horizons, but a slightly higher error at 12 months; its nominal 80% interval covered **33 of 49** 12-month targets.

## What the findings mean

Short-horizon improvements do not imply a twelve-month advantage. The recorded interval coverage also shows why point accuracy and uncertainty calibration need separate evaluation.

## Interpretation and limits

This is historical evaluation using a later data snapshot, not a real-time data-vintage backtest. Forecast errors overlap, intervals condition on fitted parameters, and NOAA records station substitution during the Mauna Loa shutdown. A single station is not a global emissions inventory.

## Package and provenance

The unchanged research package comes from the [upstream archive](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/4a22011b2b0d08492b55d75798ecb29acbeba32c/cases/case5). It retains the original conversation and included scientific artifacts, including analysis code, results and figures. The poster is an AI-generated thematic illustration, not study evidence. This introduction summarizes archived findings; the analysis was not rerun. Later bounded checks do not certify the entire study or mean the original package was corrected.

## Import provenance

This case was added to the Academic Research category on 2026-10-13, with [the archived upstream case](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/4a22011b2b0d08492b55d75798ecb29acbeba32c/cases/case5) recorded as its source. The supplied session export and poster were uploaded without changing their contents. This introduction summarizes the archived findings and was standardized for the repository. The study, external data sources, and scientific results were not rerun or independently reverified for this import.
