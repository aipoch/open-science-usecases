# Florida precipitation and Niño 3.4 seasonal association

## Research question

Does the historical rainfall–Niño 3.4 association differ by season?

Assess whether a public monthly Niño 3.4 sea-surface temperature anomaly index is associated with Florida statewide monthly precipitation, and whether the apparent relationship differs by season or a short Niño-leading lag. The comparison is fixed to one state, one index and the latest 40 complete calendar years, 1986–2025. It is an observational association, not a causal effect or a validated forecast.

## Data and comparison design

The design keeps the 1986–2025 window fixed and distinguish the month-adjusted winter association from the direct winter-minus-summer contrast. A positive coefficient in one season is not by itself evidence that its coefficient differs from another season.

| Input or source | Role in this case | Source context |
| --- | --- | --- |
| [NOAA PSL monthly Niño 3.4 anomalies](https://psl.noaa.gov/data/correlation/nina34.anom.data) | Public monthly SST index snapshot | Credit NOAA PSL; preserved text and hash in the Session ZIP; not the three-month ONI |
| [NOAA NCEI Florida monthly precipitation](https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series/8/pcp/1/0/1950-2025.csv) | Public statewide precipitation snapshot | Credit NOAA NCEI; the saved source is broader than the selected 1986–2025 analysis period |

## Recorded findings

| Winter analysis | Recorded result | Interpretation |
| --- | --- | --- |
| Historical window | 1986–2025 | Supersedes retained 1950–2025 artifacts. |
| Contemporaneous slope | 20.24 mm/month per 1°C Niño 3.4 | Association with simultaneously observed climate conditions. |
| Pointwise 95% interval | 13.73–26.60 | Not the interval for the winter-minus-summer contrast. |
| Month-adjusted correlation | 0.498 | Neither a causal coefficient nor validated lead-time forecast skill. |
| Season contrast | Simultaneous interval includes zero | A positive winter association does not prove a winter/summer difference. |

The corrected analysis uses 480 contiguous outcome months (40 years), with 120 monthly observations per season. The prespecified primary DJF lag-0 slope is **20.24 mm/month per 1°C** higher Niño 3.4, with a pointwise 95% block-bootstrap interval of **13.73–26.60** and an approximate simultaneous interval of **10.35–30.13 mm/°C**. The month-adjusted winter correlation is **0.498**. The 11 direct contrasts and sensitivity results are in the corrected report and ZIP. In particular, the primary DJF-minus-JJA contrast's simultaneous interval includes zero; seasonal and lag comparisons should not be overstated. These are historical associations, not intervention effects or proof of forecast skill.

## What the comparison shows

The winter association is clearer than the evidence for a seasonal difference. A contemporaneous association also cannot establish how well an operational advance forecast would work.

## Assumptions and limits

These are historical associations, not causal effects or validated forecast skill. The simultaneous winter-minus-summer contrast interval includes zero. Climate dependence and modeling choices constrain inference; retained 1950–2025 artifacts are superseded.

## Sources and research materials

The unchanged research package comes from [upstream Case 20](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/a6034a3ce2fb272dc7d0f582b6c4c29c2d50f7ec/cases/case20). It includes the archived session, analysis materials, results and figures. The poster uses an AI-generated illustrative photograph. This introduction summarizes archived findings; the analysis was not rerun.
