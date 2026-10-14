# Blood Metabolites - Can They Distinguish Cancer from Polyps

## Research question

Can the processed metabolite measurements distinguish cancer samples from polyp samples within this dataset?

## Data and method

Nested cross-validation separates model selection from held-out assessment. Read AUC as ranking ability across possible thresholds, and the confusion counts as performance at one fixed threshold. Repeated splits test sensitivity to partitioning but do not create new independent patients.

## Recorded findings

Tests internal discrimination between colorectal cancer and polyp samples in a public processed serum-metabolomics dataset. The primary comparison included **64 cancer and 76 polyp samples**. Three repeated nested-cross-validation AUCs were **0.856, 0.871 and 0.856**; the first-repeat fixed-threshold counts were 49 true positives, 15 false negatives, 63 true negatives and 13 false positives.

## What the findings mean

The archive suggests useful internal separation, while the false-negative and false-positive counts show the tradeoff at the chosen threshold. A clinical screening claim would require independent participants, appropriate intended-use sampling and external validation.

## Interpretation and limits

Unavailable subject identifiers prevent establishing participant independence from distinct sample IDs. Upstream processing, assay validity, batch effects and dependent validation folds limit interpretation. Internal discrimination does not establish a clinical screening test, external generalization or causal biomarkers; checking did not refit the full pipeline.

## Package and provenance

The unchanged research package comes from the [upstream archive](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/4a22011b2b0d08492b55d75798ecb29acbeba32c/cases/case13). It retains the original conversation and included scientific artifacts, including analysis code, results and figures. The poster is an AI-generated thematic illustration, not study evidence. This introduction summarizes archived findings; the analysis was not rerun. Later bounded checks do not certify the entire study or mean the original package was corrected.

## Import provenance

This case was added to the Academic Research category on 2026-10-13, with [the archived upstream case](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/4a22011b2b0d08492b55d75798ecb29acbeba32c/cases/case13) recorded as its source. The supplied session export and poster were uploaded without changing their contents. This introduction summarizes the archived findings and was standardized for the repository. The study, external data sources, and scientific results were not rerun or independently reverified for this import.
