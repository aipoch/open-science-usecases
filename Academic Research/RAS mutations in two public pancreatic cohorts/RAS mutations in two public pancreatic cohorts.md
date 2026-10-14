# RAS mutations in two public pancreatic cohorts

## Research question

How different are reported RAS mutation frequencies under a common ductal-histology eligibility rule?

Compare reported RAS mutation frequencies in two public pancreatic ductal adenocarcinoma (PDAC) cohorts while making the eligible and actually mutation-profiled denominators explicit. Check whether clinical and assay differences permit a fair interpretation, and preserve the data choices and calculations for local inspection and rerun. This case is a descriptive comparison of processed public releases, not an estimate of population prevalence or a causal explanation of the between-cohort difference.

## Data and comparison design

The analysis applies the same histology rule to both cohorts, count eligible profiled patients and retain unknown profiling status. A common inclusion rule makes the tabulation clearer but does not harmonize sequencing sensitivity, tumor cellularity or stage distributions.

| Input or source | Role in this case | Source context |
| --- | --- | --- |
| [TCGA PanCancer Atlas PAAD study](https://www.cbioportal.org/study/summary?id=paad_tcga_pan_can_atlas_2018) | Public processed clinical and mutation records | Credit the source study and cBioPortal; frozen extracts define this run |
| [CPTAC Cell 2021 PAAD study](https://www.cbioportal.org/study/summary?id=paad_cptac_2021) | Second public processed cohort | Credit the source study and cBioPortal; frozen extracts define this run |
| [cBioPortal DataHub](https://github.com/cBioPortal/datahub) | Public sequenced case lists, study metadata and a TCGA gene-panel matrix | Source URLs are mutable; the archive preserves retrieved copies and SHA-256 values |

## Recorded findings

| Eligible ductal cohort | KRAS mutation-positive | Interpretation |
| --- | --- | --- |
| TCGA | 104/150 = 69.3% | Cohort-specific profiled denominator. |
| CPTAC | 130/135 = 96.3% | Different stage, assay and cellularity mix. |
| Difference | 27.0 percentage points | Descriptive, not a causal effect or population prevalence contrast. |
| Unprofiled patients | Unknown | Never counted as mutation-negative. |

Under the rerun's explicit ductal-histology definition, **104/150 (69.3%)** profiled TCGA patients and **130/135 (96.3%)** profiled CPTAC patients had a reported KRAS mutation. The descriptive difference is **27.0 percentage points**. The report provides a conditional 95% difference interval of **18.7–35.0 percentage points**; it assumes independent cohorts, while distinct identifier namespaces do not prove the absence of shared biological donors. The difference should not be interpreted as a causal or population-prevalence contrast.

The source audit distinguishes 184 TCGA and 140 CPTAC listed patients, 179 and 140 mutation-profile members, 153 and 135 explicitly ductal patients, and 150 and 135 patients satisfying both criteria. It preserves the three TCGA explicitly ductal patients outside the selected mutation profile as unknown for this analysis, not mutation-negative. The TCGA gene-panel matrix and connector gene-coverage audit support the selected testing denominator; CPTAC's panel-matrix URL was unavailable, so its testing evidence relies on the complete case list plus the documented universal gene-coverage audit. The study cohorts differ in recorded stage distributions and lack matched assay sensitivity, cellularity and treatment metadata.

## What the comparison shows

The recorded contrast is large, but its source is unresolved. Cohort and measurement differences remain plausible explanations and must accompany the percentages.

## Assumptions and limits

Cohorts differ in stage, assays, cellularity and metadata; donor independence is not established. Unprofiled patients remain unknown, not mutation-negative. These results are neither population prevalence estimates nor a causal explanation of the difference.

## Sources and research materials

The unchanged research package comes from [upstream Case 18](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/a6034a3ce2fb272dc7d0f582b6c4c29c2d50f7ec/cases/case18). It includes the archived session, analysis materials, results and figures. The poster uses an AI-generated illustrative photograph. This introduction summarizes archived findings; the analysis was not rerun.
