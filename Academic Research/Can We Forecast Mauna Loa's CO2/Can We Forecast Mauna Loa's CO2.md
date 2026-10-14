# Can We Forecast Mauna Loa's CO2

## Research question

Does a seasonal time-series model improve on simple CO2 forecasts at each prediction horizon?

Describe long-term rise and seasonality in public Mauna Loa monthly CO2, and evaluate a compact forecasting model against simple baselines using chronological held-out targets. Distinguish current-vintage historical evaluation from real-time forecasting.

## Data and comparison design

The comparison uses SARIMA with the seasonal-drift baseline separately at one, six and twelve months. Assess both point errors and interval coverage: a narrow interval is only useful if its stated probability matches how often later observations fall inside it.

| Input or source | Role in this case | Source context |
| --- | --- | --- |
| [NOAA monthly Mauna Loa CO2](https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt) | Frozen public monthly series; retain NOAA attribution and historical Scripps credit. | Retain attribution and source terms; this README grants no additional reuse rights |
| [NOAA trends documentation](https://gml.noaa.gov/ccgg/trends/) | Definitions, preliminary-data caveats and measurement context. | Retain attribution and source terms; this README grants no additional reuse rights |

## Recorded findings

| Forecast component | Recorded result | Interpretation |
| --- | --- | --- |
| Annual mean change | 315.98 ppm (1959) → 427.35 ppm (2025) | The station series, not a global emissions total. |
| One- and six-month error | SARIMA lower than seasonal drift | Advantage depends on horizon. |
| Twelve-month error | SARIMA slightly higher | Short-horizon improvement does not extend uniformly. |
| Nominal 80% twelve-month interval | 33/49 targets covered | Coverage must be assessed separately from point error. |

The selected analysis uses 814 monthly values from March 1958 through December 2025. Annual means rise from 315.9816667 ppm in 1959 to 427.3491667 ppm in 2025: +111.3675 ppm, or 35.2449245%. At 1/6/12-month horizons, common eligible targets are 60/55/49. SARIMA MAEs are 0.298604/0.445793/0.669625 ppm; seasonal-drift MAEs are 0.552486/0.600024/0.640619 ppm. The small 12-month drift advantage is descriptive, not a demonstrated general superiority. The 12-month 80% interval covers 33/49 targets (67.3%).

The original session records scientific execution and repeatability checks; this local preparation does not re-execute them. Scientific artifacts included in this selected export:

- `analysis.R`

These files are within session.science and its embedded archive; they are not separate files alongside this README. No empty inputs/expected/outputs/attachments directories or duplicate extracted datasets are created.

## What the comparison shows

Short-horizon improvements do not imply a twelve-month advantage. The recorded interval coverage also shows why point accuracy and uncertainty calibration need separate evaluation.

## Assumptions and limits

This is historical evaluation using a later data snapshot, not a real-time data-vintage backtest. Forecast errors overlap, intervals condition on fitted parameters, and NOAA records station substitution during the Mauna Loa shutdown. A single station is not a global emissions inventory.

## Sources and research materials

The unchanged research package comes from the [upstream archive](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/4a22011b2b0d08492b55d75798ecb29acbeba32c/cases/case5). It retains the original conversation and included scientific artifacts, including analysis code, results and figures. The poster is an AI-generated thematic illustration, not study evidence. This introduction summarizes archived findings; the analysis was not rerun. Later bounded checks do not certify the entire study or mean the original package was corrected.
