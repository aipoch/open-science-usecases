# Air Pollution - Is the Turning Point Real

## Research question

Does the annual exposure series require a change in slope, or can a simpler trend explain it?

Assess whether an apparent change point in a short annual national PM2.5 exposure series is stable under alternative error assumptions, time windows and model choices. Compare a searched continuous hinge with a no-break linear trend and a smooth quadratic; distinguish break-year uncertainty conditional on a break from evidence that a break exists.

## Data and comparison design

A hinge model joins two slopes at a candidate year. Searching many years makes the best-looking break easier to find by chance, so read search-adjusted tests alongside AICc and BIC, which penalize added complexity. A knot at the earliest eligible year deserves particular scrutiny.

| Input or source | Role in this case | Source context |
| --- | --- | --- |
| [World Bank India PM2.5 API](https://api.worldbank.org/v2/country/IND/indicator/EN.ATM.PM25.MC.M3?format=json&per_page=1000) | Original national annual exposure response |  |
| [World Bank indicator metadata](https://api.worldbank.org/v2/indicator/EN.ATM.PM25.MC.M3?format=json) | Units, source and indicator definition |  |
| [IHME GBD 2023 source attribution](https://ghdx.healthdata.org/record/ihme-data/gbd-2023-air-pollution-exposure-estimates-1990-2023) | Upstream attribution from captured World Bank metadata; not downloaded by the study |  |

## Recorded findings

| Model check | Independent errors | AR(1) errors |
| --- | --- | --- |
| Selected hinge knot | 1995 | 1995 |
| Search-adjusted p-value | 0.2060 | 0.3365 |
| Sensitivity support | No AICc or BIC hinge wins in 48 settings | The settings are correlated, not 48 independent replications. |

The 34 observations have mean **51.649594** and sample SD **2.032641 µg/m³**. Requiring five observations strictly on each side gives 24 eligible knots, **1995–2018**. Both searched hinges select 1995, an eligibility boundary.

Hinge-minus-line AICc/BIC differences are **+1.438992/+3.148856** for independent errors and **+2.310964/+3.631885** for AR(1), favoring the line. The no-break slopes remain positive, approximately **+0.144895/+0.142971 µg/m³/year**; no break does not mean no trend.

Among 1,999 null replicates per error model, 411 and 672 exceedances give add-one search-adjusted p-values **0.2060** and **0.3365**. The hinge wins neither AICc nor BIC in any of 48 sensitivity settings. AICc line/quadratic counts are 42/6; BIC counts are 45/3. Half select boundary knots. Conditional knot intervals span **1995–2018**, the full eligible range; these intervals assume a fitted hinge and do not establish break existence.

The selected series does **not convincingly support a stable abrupt trend break** under these comparisons. This is not proof that no real change occurred.

## What the comparison shows

The apparent turning point loses support when search and model complexity are accounted for. A visually appealing bend therefore should not be presented as a demonstrated policy effect.

## Assumptions and limits

No supported break does not mean no trend or prove that no real change occurred. National aggregation, short windows, exposure-model uncertainty and error assumptions constrain the finding. Conditional break-year intervals assume a break exists; correlated sensitivity settings are not independent votes.

## Sources and research materials

The unchanged research package comes from the [upstream archive](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/4a22011b2b0d08492b55d75798ecb29acbeba32c/cases/case25). It retains the original conversation and included scientific artifacts, including analysis code, results and figures. The poster is an AI-generated thematic illustration, not study evidence. This introduction summarizes archived findings; the analysis was not rerun. Later bounded checks do not certify the entire study or mean the original package was corrected.
