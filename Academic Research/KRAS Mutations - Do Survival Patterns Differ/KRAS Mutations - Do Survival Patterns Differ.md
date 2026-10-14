# KRAS Mutations - Do Survival Patterns Differ

## Research question

Do KRAS mutation groups show different survival patterns after specimen collection?

Assess whether KRAS mutation groups are associated with overall survival in a suitable public pancreatic cancer cohort, with explicit cohort selection, endpoint origin, group definitions and evidence-scaled adjustment. The selected analysis uses MSK post-specimen-collection survival rather than TCGA diagnosis-origin survival.

## Data and comparison design

The comparison uses group survival curves with the saved age-, sex- and stage-adjusted Cox estimate. A median summarizes a curve at one point; a hazard ratio summarizes relative event rates under model assumptions. Check the time origin and proportional-hazards diagnostics before interpreting either.

| Input or source | Role in this case | Source context |
| --- | --- | --- |
| [cBioPortal MSK pancreatic cohort](https://www.cbioportal.org/study/summary?id=pdac_msk_2024) | Selected public cohort and endpoint metadata | Preserve upstream attribution and applicable source terms; this README grants no additional third-party rights |
| [cBioPortal DataHub source files](https://github.com/cBioPortal/datahub/tree/master/public/pdac_msk_2024) | Mutation and clinical snapshots; retrieved 2026-09-28 according to the original report | Preserve upstream attribution and applicable source terms; this README grants no additional third-party rights |
| [Original study](https://pubmed.ncbi.nlm.nih.gov/39753968/) | Study citation retained in cohort metadata | Preserve upstream attribution and applicable source terms; this README grants no additional third-party rights |

## Recorded findings

| Survival summary | Recorded result | Interpretation |
| --- | --- | --- |
| Usable outcomes | 2,270 patients | Public MSK pancreatic cohort. |
| G12D median | 15.5 months | Time begins at specimen collection. |
| G12R median | 20.4 months | Observational group summary. |
| Adjusted G12R/G12D hazard ratio | 0.769; 95% CI 0.655–0.903 | Saved age/sex/stage model; stage violates proportional hazards. |

The source contains 2,336 unique patients; 2,270 have usable survival outcomes (1,521 deaths). The five-group inferential set contains 2,249 patients and 1,505 deaths, excluding 21 multiple/ambiguous records. G12D and G12R median post-collection survival is 15.5 and 20.4 months; their 24-month estimates are 31.9% and 44.2%. The saved age/sex/stage-adjusted G12R-versus-G12D HR is 0.76885 (95% CI 0.65495–0.90255). The external review independently checked selected Kaplan–Meier/count/Holm arithmetic but did not refit Cox models.

## What the comparison shows

The recorded group difference remains an observational association. It does not show that changing a mutation would change survival, or that one group benefits more from a specific treatment.

## Assumptions and limits

These are exploratory observational associations, not causal mutation effects or treatment-benefit predictions. Stage violates proportional hazards, missing outcomes are imbalanced, and residual confounding remains. Survival begins at specimen collection; bounded checking did not refit the Cox models.

## Sources and research materials

The unchanged research package comes from the [upstream archive](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/4a22011b2b0d08492b55d75798ecb29acbeba32c/cases/case11). It retains the original conversation and included scientific artifacts, including analysis code, results and figures. The poster is an AI-generated thematic illustration, not study evidence. This introduction summarizes archived findings; the analysis was not rerun. Later bounded checks do not certify the entire study or mean the original package was corrected.
