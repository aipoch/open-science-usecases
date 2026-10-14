# Blood Metabolites - Can They Distinguish Cancer from Polyps

## Research question

Can the processed metabolite measurements distinguish cancer samples from polyp samples within this dataset?

Evaluate how well a small public processed serum metabolomics dataset distinguishes colorectal cancer from a defensible non-cancer comparison, and how trustworthy internal held-out performance is. The primary task uses CRC versus polyp samples and explicitly examines data quality and limits to generalization.

## Data and comparison design

Nested cross-validation separates model selection from held-out assessment. Read AUC as ranking ability across possible thresholds, and the confusion counts as performance at one fixed threshold. Repeated splits test sensitivity to partitioning but do not create new independent patients.

| Input or source | Role in this case | Source context |
| --- | --- | --- |
| [Dataset DOI](https://doi.org/10.21228/M8FG61) | Deposited processed serum data and metadata | Preserve upstream attribution and applicable source terms; this README grants no additional third-party rights |
| [Original study](https://doi.org/10.1021/pr500494u) | Targeted serum metabolic profiling publication; deposit/publication sample and feature counts differ | Preserve upstream attribution and applicable source terms; this README grants no additional third-party rights |

## Recorded findings

| Validation component | Recorded result | Interpretation |
| --- | --- | --- |
| Primary sample groups | 64 cancer; 76 polyp | Samples, not independently established unique participants. |
| Nested-CV AUCs | 0.856 / 0.871 / 0.856 | Three repeated internal evaluations. |
| First-repeat cancer decisions | 49 true positive; 15 false negative | One fixed decision threshold. |
| First-repeat polyp decisions | 63 true negative; 13 false positive | Threshold tradeoff, not a clinical screening estimate. |

The deposit contains 224 samples and 113 metabolites; the primary comparison is 64 CRC versus 76 polyp samples. Three repeated nested-CV AUCs are 0.856291118, 0.871299342 and 0.855674342. The prespecified first-repeat AUC has a conditional saved-prediction bootstrap interval of 0.786950–0.916149. At the fixed 0.5 threshold, TP/FN/TN/FP are 49/15/63/13. None of 99 saved permutation AUCs exceeds the observed value, giving corrected p=0.01. The external review checked ranking/count/percentile arithmetic, not a complete pipeline refit.

## What the comparison shows

The archive suggests useful internal separation, while the false-negative and false-positive counts show the tradeoff at the chosen threshold. A clinical screening claim would require independent participants, appropriate intended-use sampling and external validation.

## Assumptions and limits

Unavailable subject identifiers prevent establishing participant independence from distinct sample IDs. Upstream processing, assay validity, batch effects and dependent validation folds limit interpretation. Internal discrimination does not establish a clinical screening test, external generalization or causal biomarkers; checking did not refit the full pipeline.

## Sources and research materials

The unchanged research package comes from the [upstream archive](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/4a22011b2b0d08492b55d75798ecb29acbeba32c/cases/case13). It retains the original conversation and included scientific artifacts, including analysis code, results and figures. The poster is an AI-generated thematic illustration, not study evidence. This introduction summarizes archived findings; the analysis was not rerun. Later bounded checks do not certify the entire study or mean the original package was corrected.
