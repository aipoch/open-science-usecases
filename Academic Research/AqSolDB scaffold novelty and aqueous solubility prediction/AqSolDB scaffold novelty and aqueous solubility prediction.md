# AqSolDB scaffold novelty and aqueous solubility prediction

## Research question

Does a solubility model retain its accuracy when test molecules come from held-out scaffolds?

## Data and method

A random split can distribute related molecular structures across training and test sets. A scaffold split groups molecules by a shared core before separation. Compare logS prediction error under both designs while checking which compounds, especially acyclic ones, remain eligible for each partition.

## Recorded findings

Tests aqueous-solubility prediction on 8,479 curated AqSolDB molecular identities using random and scaffold splits. Random-forest mean absolute error increased from **0.700 to 0.812 logS** on scaffold splits, indicating weaker performance under this structural holdout design.

## What the findings mean

The harder structural holdout reveals an accuracy loss hidden by ordinary random splitting. Because the test populations differ, the gap describes this evaluation design rather than a fixed cost of molecular novelty.

## Interpretation and limits

Test compositions differed, and acyclic compounds remained in training in every scaffold split. The difference is not a universal penalty for novel chemistry; incomplete experimental conditions also limit interpretation.

## Package and provenance

The unchanged research package comes from [upstream Case 4](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/a6034a3ce2fb272dc7d0f582b6c4c29c2d50f7ec/cases/case4). It includes the archived session, analysis materials, results and figures. The poster uses an AI-generated illustrative photograph. This introduction summarizes archived findings; the analysis was not rerun.

## Import provenance

This case was added to the Academic Research category on 2026-10-13, with [the archived upstream case](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/a6034a3ce2fb272dc7d0f582b6c4c29c2d50f7ec/cases/case4) recorded as its source. The supplied session export and poster were uploaded without changing their contents. This introduction summarizes the archived findings and was standardized for the repository. The study, external data sources, and scientific results were not rerun or independently reverified for this import.
