# Diet Diversity - Does the Gut Microbiome Differ

## Research question

Is reported plant diversity associated with microbial composition after country adjustment?

Assess reported plant-type categories and gut microbial community composition in historical American Gut data, with geography and questionnaire-missingness sensitivity.

## Data and comparison design

The analysis compares samples through Bray–Curtis dissimilarity and its corrected geometry, rather than testing one organism in isolation. Read incremental R² with the permutation test and dispersion checks: a detectable association may still explain very little of the variation.

## Recorded findings

| Analysis element | Recorded result | Meaning |
| --- | --- | --- |
| Fixed-seed sample | 600 participants | Captured historical American Gut sample. |
| Main analysis | 564 participants | After the archived eligibility and missingness rules. |
| Incremental R² | 0.804% | Country-adjusted corrected Bray–Curtis geometry. |
| Permutation p-value | .004 | A detectable, small association; sensitivities are less conclusive. |

The source contains 4,827 matching samples and 22,742 features. Eligibility and participant deduplication leave 2,719 participants, from whom a fixed-seed country-proportional sample of 600 was selected. Main analysis includes 564 respondents with known country; 479 complete cases, 540 US respondents and a 300-person eight-state subset support sensitivity analyses.

All 9,089 nonzero cohort features were retained. Bray–Curtis geometry had 259 materially negative eigenvalues; Lingoes correction yielded 598 retained coordinate dimensions. All dimensions were used for inference; display axes explain 4.40% and 2.47% of corrected inertia.

The primary country-adjusted association has incremental R² **0.0080399356 (0.804%)**, partial R² **0.0081978586 (0.820%)**, pseudo-F **1.1344562**, and permutation **p=.004** using 999 permutations. This is a small association in corrected geometry, not the fraction of raw-count biological variance explained or a causal benefit. Multiplicity-adjusted complete-case and regional sensitivity tests are less conclusive.

The new mean centroid distances decrease from **0.840916** to **0.808207** across increasing plant categories; “More than 30” is correctly identified as the minimum. The previous attempt's range defect is absent. Dispersion F is **2.3986004**, with saved permutation p=.046; unequal dispersion limits a pure centroid interpretation.

Artifacts inside the package: `analysis_rules.md`, `analysis.py`, `study_report.md`, `plant_diversity_reproducible.zip`, `ordination.png`, and `sensitivity_missingness.png`. The bundle additionally includes captured inputs, model/cohort/missingness/geometry tables, PDF figures and replay records.

## What the comparison shows

The recorded association is small and sensitive to analysis choices. It describes community-composition differences in this cohort, without establishing that dietary diversity caused a healthier microbiome.

## Assumptions and limits

The small association is not a causal dietary benefit or a fraction of raw-count biological variance explained. Self-report, missingness, confounding and a heavily US-dominated cohort limit generalization. Unequal dispersion and substantial geometry correction complicate interpretation; original geometry and permutation generation were not independently rerun.

## Sources and research materials

The unchanged research package comes from the [upstream archive](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/4a22011b2b0d08492b55d75798ecb29acbeba32c/cases/case21). It retains the original conversation and included scientific artifacts, including analysis code, results and figures. The poster is an AI-generated thematic illustration, not study evidence. This introduction summarizes archived findings; the analysis was not rerun. Later bounded checks do not certify the entire study or mean the original package was corrected.
