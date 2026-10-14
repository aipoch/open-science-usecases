# PFAS assay activity and placental cell-type expression

## Research question

Which assay-linked genes also appear in the placental expression data, and how much does mapping strictness matter?

This case examines how public in-vitro activity records for selected PFAS chemicals relate to target-gene expression in a public placental single-cell atlas. It combines processed EPA invitrodb v4.3 assay exports with the [E-MTAB-6701](https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-6701) atlas, retaining chemical–assay–gene mappings, donor variation and sensitivity analyses. It is a descriptive cross-source assessment, not a PFAS exposure experiment or a test of placental toxicity.

## Data and comparison design

The analysis treats assay-to-gene mapping and gene expression as separate evidence layers. Expanded mappings admit a broader set of links; strict human biochemical mappings require narrower target attribution. Expression indicates potential cellular context, not chemical exposure or target engagement.

## Recorded findings

| Gene-linking rule | PFOA-associated genes | PFOS-associated genes |
| --- | --- | --- |
| Expanded mapping | 45 | 142 |
| Strict human biochemical mapping | 7 | 42 |
| Expression source | Five pregnancy IDs | Cell-type expression, not a matched exposure experiment |
| Interpretation | Overlap depends on mapping rules | Counts do not establish relative toxicity |

This case examines how public in-vitro activity records for selected PFAS chemicals relate to target-gene expression in a public placental single-cell atlas. It combines processed EPA invitrodb v4.3 assay exports with the [E-MTAB-6701](https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-6701) atlas, retaining chemical–assay–gene mappings, donor variation and sensitivity analyses. It is a descriptive cross-source assessment, not a PFAS exposure experiment or a test of placental toxicity.

The saved analysis selects PFOS and PFOA by assay coverage, freezes a 200-gene panel before inspecting expression, and uniquely matches 197 genes. It retains 18,547 placenta-origin cells from five pregnancy IDs; the primary minimum-cell rule yields 41 donor–cell-type groups, 18,400 cells and 12 cell types. Expanded active-assay mappings implicate 45 expression-matched genes for PFOA and 142 for PFOS; stricter human biochemical mappings reduce these to seven and 42. These are assay-linked transcript contexts, not confirmed placental targets or a relative toxicity ranking.

Important limits include five early-gestation donors, three unresolved gene symbols, incomplete assay-quality information and no matched PFAS exposure or placental outcome measurements. Neither chemical has explicit sample-QC-pass records in the selected assay data. The sources cannot establish placental exposure, target engagement, causality, a safe dose or adverse fetal effects. Detailed methods, donor intervals and sensitivity results remain in the retained report.

## What the comparison shows

The large change in linked-gene counts shows that mapping rules shape the overlap. More mapped genes do not mean greater toxicity, and expressed targets do not establish an in-vivo PFAS effect.

## Assumptions and limits

This is not an exposure experiment or placental toxicity test. Small donor numbers, incomplete assay QC and absent matched exposure/outcome data prevent claims about target engagement, safe doses, fetal harm or relative toxicity.

## Sources and research materials

The unchanged research package comes from [upstream Case 30](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/a6034a3ce2fb272dc7d0f582b6c4c29c2d50f7ec/cases/case30). It includes the archived session, analysis materials, results and figures. The poster uses an AI-generated illustrative photograph. This introduction summarizes archived findings; the analysis was not rerun.
