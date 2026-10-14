# EGFR potency prediction - an inspectable pilot

## Research question

How much predictive performance survives separation by publication and by distant chemistry?

## Data and method

An ordinary compound holdout can retain assay and publication context shared with training. The combined holdout makes that transfer harder. Compare absolute pIC50 error with within-assay rank correlation so that apparently acceptable pooled error does not obscure poor ordering within an assay.

## Recorded findings

Tests EGFR potency prediction in a curated pilot of **404 compounds**. Mean absolute error increased from **0.502 to 0.788 pIC50 units** between ordinary compound and combined publication-plus-distant-chemistry holdouts. Median within-assay rank correlation was only 0.179.

## What the findings mean

The harder holdout and weak within-assay ranking expose limits of the pilot. Inspectability makes those limits easier to examine; it does not itself make the model ready for compound-selection decisions.

## Interpretation and limits

The first-1,000-record convenience sample and incomplete assay conditions limit generalization. This is an inspectable retrospective pilot, not a prospective predictor, mutant-EGFR validation or assay-specific decision tool.

## Package and provenance

The unchanged research package comes from [upstream Case 14](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/a6034a3ce2fb272dc7d0f582b6c4c29c2d50f7ec/cases/case14). It includes the archived session, analysis materials, results and figures. The poster uses an AI-generated illustrative photograph. This introduction summarizes archived findings; the analysis was not rerun.

## Import provenance

This case was added to the Academic Research category on 2026-10-13, with [the archived upstream case](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/a6034a3ce2fb272dc7d0f582b6c4c29c2d50f7ec/cases/case14) recorded as its source. The supplied session export and poster were uploaded without changing their contents. This introduction summarizes the archived findings and was standardized for the repository. The study, external data sources, and scientific results were not rerun or independently reverified for this import.
