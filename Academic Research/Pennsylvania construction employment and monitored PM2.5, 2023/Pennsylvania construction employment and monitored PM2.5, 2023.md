# Pennsylvania construction employment and monitored PM2.5, 2023

## Research question

How much construction employment falls in counties with an eligible annual monitoring summary?

Describe how 2023 private construction payroll jobs are distributed across Pennsylvania counties with different eligible outdoor PM2.5 monitor summaries. Separate absent and insufficient monitoring from measured concentration bands. This is a county-level descriptive comparison, **not** a measure of individual workers' exposure or a causal health analysis.

## Data and comparison design

Join county payroll totals with eligible county PM2.5 summaries and retain an explicit missing-monitoring category. Employment-weighted coverage describes where recorded jobs are located; it does not measure each worker’s dose or the duration spent at a job site.

| Input or source | Role in this case | Source context |
| --- | --- | --- |
| [BLS QCEW 2023 annual NAICS 23 CSV](https://data.bls.gov/cew/data/api/2023/a/industry/23.csv) | Official construction-employment source | Cite BLS; the archived rows and acquisition ledger define this run |
| [BLS area titles](https://data.bls.gov/cew/doc/titles/area/area_titles.csv) | County names and area identifiers | Cite BLS; duplicated title rows are retained and explicitly deduplicated |
| [EPA 2023 annual monitor file](https://aqs.epa.gov/aqsweb/airdata/annual_conc_by_monitor_2023.zip) | Official PM2.5 annual monitor summaries | Cite EPA; this case retains the Pennsylvania parameter-88101 rows and selection flags |
| [EPA file definitions](https://aqs.epa.gov/aqsweb/airdata/FileFormats.html) and [PM2.5 correction advisory](https://aqs.epa.gov/aqsweb/airdata/Data_Advisory_PM25_88101_Pregen_Files.pdf) | Interpret completeness, metrics and affected instrument methods | Official documentation retained in the input ZIP |

## Recorded findings

| Coverage quantity | Recorded value | Interpretation |
| --- | --- | --- |
| Total payroll jobs | 247,962 | 2023 county employment totals. |
| Jobs without eligible county PM2.5 | 65,246; 26.3% | Missing monitoring is retained rather than treated as zero pollution. |
| Counties with eligible monitoring | 23 of 67 | Coverage is incomplete. |
| Exposure scale | County ambient summary | Not a measurement of individual construction-worker dose. |

The report includes all 67 Pennsylvania counties and **247,962** published annual-average private construction payroll jobs. **65,246 jobs (26.3%)** were in counties without an eligible PM2.5 value: 35 counties had no reported parameter-88101 monitor row, and nine had monitor rows but no eligible complete annual summary. These jobs were not placed in a measured low-PM2.5 band. The 2023 state total and 12,686 unknown-location jobs are reported separately, including the two-job rounding discrepancy.

The selected EPA rows yielded 38 sites in 23 counties. The report explains the annual-summary basis, one-row-per-site selection, two accepted daily durations, event treatment, completeness, and the official instrument correction advisory. Its highest-site sensitivity changes the measured band for three counties representing 39,641 jobs; monitoring-gap counts remain unchanged. The county averages are descriptive, not personal exposure or regulatory attainment estimates.

## What the comparison shows

The missing category is a substantive part of the result. Dropping those counties would hide coverage gaps and change the denominator of any employment summary.

## Assumptions and limits

County ambient summaries are not workers’ individual exposures or regulatory attainment estimates. Missing monitoring is not zero pollution. Coverage rules and site aggregation affect categories; a later, narrower-basis rerun is not merged into this version.

## Sources and research materials

The unchanged research package comes from [upstream Case 24](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/a6034a3ce2fb272dc7d0f582b6c4c29c2d50f7ec/cases/case24). It includes the archived session, analysis materials, results and figures. The poster uses an AI-generated illustrative photograph. This introduction summarizes archived findings; the analysis was not rerun.
