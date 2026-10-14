# Genomic context of the Horvath epigenetic clock

## Research question

Do apparent clock-CpG enrichments persist when the comparison background better reflects platform availability?

Assess whether the 353 CpGs in the publicly documented Horvath 2013 clock have a distinctive genomic annotation profile compared with sites that could have been measured by the assay. In particular, compare the full Illumina 450K CpG background with a 27K-shared proxy closer to the clock's cross-platform selection opportunity. This is a compact annotation-based evaluation of Open-Science's research and reproducibility workflow, not a drug-discovery study or a validation of biological aging mechanisms.

## Data and comparison design

The comparison uses the same clock sites against the full 450K set and the 27K-shared proxy. An enrichment odds ratio depends on how common an annotation is in the chosen background; platform selection can therefore mimic a biological preference.

| Input or source | Role in this case | Source context |
| --- | --- | --- |
| [Horvath 2013 article](https://doi.org/10.1186/gb-2013-14-10-r115) | Clock definition and original candidate-universe context | Cite the article; the publisher's supplementary site list was not directly cross-checked in this run |

## Recorded findings

| Annotation comparison | Recorded result | Why the background matters |
| --- | --- | --- |
| Clock sites | 353 CpGs | The fixed selected set. |
| Backgrounds | Full 450K and 27K-shared proxy | Platform availability changes the eligible comparison pool. |
| CpG-shore enrichment | Odds ratio 1.54 under shared proxy | Persists under that narrower comparison. |
| Island / promoter enrichment | Island no longer clear; promoter much smaller | Some apparent enrichment is background-sensitive. |

Original analysis date: 2026-09-24; figure addition and new export: 2026-10-12. The original report compares 353 clock CpGs with 482,068 non-clock controls in the full 450K CpG assay and 25,625 non-clock controls in the 27K-shared proxy. It reports 72 feature/background comparisons, including chemistry-specific sensitivity analyses. The exact original 21,369-probe training-eligible universe was **not** recovered.

Against the full assay, CpG-island, shore and promoter odds ratios are 1.37, 2.36 and 3.77. Against the shared-platform proxy, they are 0.83 (no clear island association), 1.54 and 1.33. The report identifies shore enrichment as the most consistent residual feature: 147/353 clock sites (41.6%) versus 31.7% of shared-platform non-clock controls, OR 1.54 (95% CI 1.23–1.91). It explicitly limits these results to annotation/selection contrasts, not causal aging mechanisms.

## What the comparison shows

Some annotation contrasts persist while others weaken with the background change. This makes the choice of eligible comparison sites central to the interpretation.

## Assumptions and limits

The shared-platform set is a proxy, not the original training-eligible universe. Older annotations, correlated CpGs and unadjusted figure intervals limit interpretation. These annotation contrasts neither establish an aging mechanism nor clinically validate the clock.

## Sources and research materials

The unchanged research package comes from [upstream Case 2](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/a6034a3ce2fb272dc7d0f582b6c4c29c2d50f7ec/cases/case2). It includes the archived session, analysis materials, results and figures. The poster uses an AI-generated illustrative photograph. This introduction summarizes archived findings; the analysis was not rerun.
