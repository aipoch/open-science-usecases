# Involved versus uninvolved Crohn ileum - donor-aware expression assessment

## Research question

Which expression contrasts remain credible when paired donors, rather than individual cells, define replication?

Use public GSE134809 single-cell data to compare involved and uninvolved Crohn ileal tissue across 11 paired donors. The task asks for donor-supported inflammatory expression differences, a clean computation from frozen inputs, inspectable analysis artifacts, and careful treatment of tissue definitions, donor replication, chemistry, annotations and statistical limitations. A within-cohort expression contrast is not independent biological validation, a healthy-control comparison, causal evidence or a treatment-response prediction.

## Data and comparison design

Cells from the same donor share biological and technical context. Read the paired-donor contrast separately from the number of cells, and distinguish the composite association rule from independently corrected panel-gene and program tests. The V2-only sensitivity changes the chemistry subset.

| Input or source | Role in this case | Source context |
| --- | --- | --- |
| [GSE134809](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE134809) | Public Crohn ileal single-cell source data | Credit GEO and the original study; use the frozen input hashes for exact reconstruction |
| [Martin et al., Cell 2019](https://doi.org/10.1016/j.cell.2019.08.008) | Study design and biological context | The publication's cohort and annotations are not interchangeable with this reanalysis |

## Recorded findings

| Testing layer | Recorded result | Replication unit or scope |
| --- | --- | --- |
| Input | 69,762 cells from 11 paired donors | Donors, not cells, define independent biological replication. |
| Composite association rule | 15 inflammatory gene–lineage associations | Separate from the individual-gene testing family. |
| Individual panel genes | None pass separately corrected exact-test FDR | A stricter, separately corrected evidence layer. |
| Program tests | 6/18 pass primary FDR; none in V2-only sensitivity | Chemistry restriction changes the support. |

The selected Session was exported on 2026-09-29 from a new clean project. It records a `gpt-6-astra` run with 36 Notebook executions, including two failed executions retained in the history, and **seven Artifact lineages / eight Artifact versions**. The saved report describes 69,762 assigned immune/stromal cells from 22 ileal libraries and 11 paired donors. Six lineages have 8–11 eligible donor pairs. It reports 15 inflammatory gene–lineage associations meeting its composite negative-binomial/donor-consistency rule, strongest in myeloid cells; **none** of the individual inflammatory-panel genes crosses the separately corrected exact-test FDR threshold. Six of 18 primary program tests narrowly cross FDR <0.05, while none does in the V2-only sensitivity. These are the producing Session's reported results, not calculations independently recomputed for this repository submission.

## What the comparison shows

Many cells do not replace independent donors. Different testing families and chemistry restrictions can produce different discovery counts without being contradictory.

## Assumptions and limits

Small donor counts, chemistry and annotation choices constrain this within-cohort contrast. Historical review issues were addressed in review_dispositions.json; textual review does not establish a full computational audit or fresh-environment Notebook rerun.

## Sources and research materials

The unchanged research package comes from [upstream Case 12](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/a6034a3ce2fb272dc7d0f582b6c4c29c2d50f7ec/cases/case12). It includes the archived session, analysis materials, results and figures. The poster uses an AI-generated illustrative photograph. This introduction summarizes archived findings; the analysis was not rerun.
