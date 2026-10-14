# Amazon Tree-Cover Loss - Does the Definition Change the Picture

## Research question

How much does the canopy definition change measured tree-cover loss in the same geographic window?

Describe annual mapped tree-cover loss and canopy-threshold sensitivity in a small fixed western Amazon study area. The selected analysis uses a WGS84 box near Iberia, Peru (longitude −69.60 to −69.40; latitude −11.50 to −11.30), Hansen GFC-2024-v1.12 and complete years 2001–2024.

## Data and comparison design

The design keeps the raster extent and loss-year layer fixed while changing the year-2000 canopy threshold. Report lost area in hectares separately from the fraction of eligible baseline canopy: changing that baseline can change the percentage without changing the timing of the largest annual event.

| Input or source | Role in this case | Source context |
| --- | --- | --- |
| [Hansen GFC-2024-v1.12](https://storage.googleapis.com/earthenginepartners-hansen/GFC-2024-v1.12/download.html) | Fixed release; treecover2000, lossyear and datamask from tile 10S_070W; original report records CC BY 4.0 and Hansen/UMD/Google/USGS/NASA attribution | Preserve upstream attribution and applicable source terms; this README grants no additional third-party rights |
| [Global Forest Change](https://glad.earthengine.app/view/global-forest-change) | Dataset landing page and interpretation context | Preserve upstream attribution and applicable source terms; this README grants no additional third-party rights |
| [Hansen et al. 2013](https://doi.org/10.1126/science.1244693) | Original methodology, not independent validation of the local 2024 result | Preserve upstream attribution and applicable source terms; this README grants no additional third-party rights |

## Recorded findings

| Mapped-loss summary | Recorded value | Definition |
| --- | --- | --- |
| Canopy baseline | Year 2000, ≥30% threshold | Defines eligible baseline area. |
| Cumulative 2001–2024 loss | 25,133 ha | Loss inside the fixed western Amazon window. |
| Fraction of baseline | 55.54% | A threshold-dependent denominator. |
| Peak year | 2024: 6,732 ha | Peak persists across all three tested canopy thresholds. |

The 800 × 800 window contains 599,739 qualifying ≥30% canopy land pixels, giving a year-2000 baseline of 45,252.1643 ha. Cumulative mapped loss in 2001–2024 is 25,133.0619 ha, or 55.5400% of that fixed baseline. The 2024 peak is 6,731.5776 ha, 6.4325 times the 2023 total, and remains the peak at all three thresholds (≥30%, ≥50%, ≥75%). Raising the threshold from 30% to 75% reduces cumulative mapped loss by 1.082945%; the affected fraction increases because its baseline denominator also shrinks. The external review checked saved-table arithmetic and additionally recalculated the baseline from preserved input arrays.

## What the comparison shows

The peak year is more stable across these definitions than the cumulative percentage. This distinguishes a robust temporal feature from a denominator-sensitive estimate.

## Assumptions and limits

Mapped pixel loss is not independently validated deforestation, permanence, cause, carbon emissions or current forest area. The local rectangle is not representative of the entire Amazon. Release and processing differences affect temporal comparisons; threshold sensitivity is not a confidence interval.

## Sources and research materials

The unchanged research package comes from the [upstream archive](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/4a22011b2b0d08492b55d75798ecb29acbeba32c/cases/case15). It retains the original conversation and included scientific artifacts, including analysis code, results and figures. The poster is an AI-generated thematic illustration, not study evidence. This introduction summarizes archived findings; the analysis was not rerun. Later bounded checks do not certify the entire study or mean the original package was corrected.
