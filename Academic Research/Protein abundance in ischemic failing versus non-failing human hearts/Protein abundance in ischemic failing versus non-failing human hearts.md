# Protein abundance in ischemic failing versus non-failing human hearts

## Research question

Which apparent protein differences survive a change in normalization?

Use an existing public processed LFQ matrix to compare a clearly labeled ischemic heart-failure group with non-failing donor hearts. Evaluate which abundance differences survive multiple-testing correction and how the interpretation changes under missing-value and normalization sensitivities. This is an exploratory analysis, not a diagnostic or causal study.

## Data and comparison design

The comparison uses the archived MaxLFQ-scale analysis with sample-median centering on the same groups. Apply multiple-testing correction within each analysis and keep protein-group identity separate from a confident single-gene assignment.

| Input or source | Role in this case | Source context |
| --- | --- | --- |
| [Tomin et al. (2021)](https://doi.org/10.3390/ijms22041787) and [supplementary materials](https://www.mdpi.com/1422-0067/22/4/1787/s1) | Published cohort description and Table S5 diagnosis-to-experiment labels | Open-access article under CC BY 4.0; credit the original authors and source |
| [PRIDE PXD021261](https://www.ebi.ac.uk/pride/archive/projects/PXD021261) | Public processed `proteinGroupss_LFQ.txt` and related metadata | Credit the original data creators; do not use historical reviewer-account credentials |

## Recorded findings

| Comparison element | Archived MaxLFQ scale | After sample-median centering |
| --- | --- | --- |
| Sample groups | 12 ischemic failing; 10 non-failing male hearts | Same samples |
| Tested protein groups | 1,327 | Same comparison population |
| 5% FDR discoveries | TF and a CP-associated group | Neither remains significant |
| Identity and context | CP protein-group assignment unresolved | Batch mapping unavailable; not a stable diagnostic signature |

Scientific run date: 2026-09-28; current export and redacted-package update: 2026-10-10. The report tested 1,327 protein groups after filtering, finding TF/serotransferrin and a CP/ceruloplasmin-associated group at BH q < 0.05 on the archived MaxLFQ scale. Both were fully observed and remained on the shortlist across 100 low-intensity imputation stress tests. Neither remained below 5% FDR after sample-median centering; CP also has unresolved group identity owing to a contaminant-database accession. This is a small, normalization-sensitive exploratory association, not a general heart-failure signature.

## What the comparison shows

The loss of the two discoveries after centering makes normalization central to the finding. It supports a sensitivity discussion, rather than a stable heart-failure biomarker claim.

## Assumptions and limits

The small-sample findings are normalization-sensitive, not a general heart-failure signature. CP protein-group identity remains unresolved, and verified batch mapping was unavailable. The study does not establish diagnostic or causal effects.

## Sources and research materials

The unchanged research package comes from [upstream Case 8](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/a6034a3ce2fb272dc7d0f582b6c4c29c2d50f7ec/cases/case8). It includes the archived session, analysis materials, results and figures. The poster uses an AI-generated illustrative photograph. This introduction summarizes archived findings; the analysis was not rerun.
