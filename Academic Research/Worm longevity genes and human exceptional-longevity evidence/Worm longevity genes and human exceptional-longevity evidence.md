# Worm longevity genes and human exceptional-longevity evidence

## Research question

Do human candidates mapped from worm longevity genes overlap eligible exceptional-longevity catalog evidence?

Examine a small, prespecified set of model-organism longevity genes, map them to candidate human genes without concealing orthology ambiguity, and audit public human longevity association records. The question is what the selected public tables support, not whether a missing catalog record disproves a biological role in ageing.

## Data and comparison design

The analysis separates orthology mapping from phenotype and gene matching in the catalog. Keep eligible matches, excluded records and unresolved rows in distinct groups. A broad biological notion of longevity may not match the exact human phenotype definitions used by the screen.

| Input or source | Role in this case | Source context |
| --- | --- | --- |
| [GenAge model-organism gene download](https://genomics.senescence.info/genes/models_genes.zip) | Worm longevity-gene shortlist and source annotations | GenAge build 21; cite the source; reuse terms for redistribution have not been independently established here |
| [GWAS Catalog public releases](https://ftp.ebi.ac.uk/pub/databases/gwas/releases/latest/) | Association, study and ancestry exports | Snapshot from the directory dated 2026-10-05; cite the Catalog; `latest` is mutable |

## Recorded findings

| Screening step | Recorded quantity | Interpretation |
| --- | --- | --- |
| Eligible worm genes | 9 | Starting biological evidence set. |
| Human candidates | 21 | Orthology mapping can be one-to-many. |
| Eligible exceptional-longevity rows | 75; no matching candidates | A result under the frozen matching rules. |
| Unresolved rows | 159 | Unknown evidence, not negative findings. |

Nine of ten preselected worm genes were present in GenAge build 21; `akt-2` was excluded without replacement. Alliance's stringent graph produced 21 distinct human candidates, with three one-to-one, 13 one-to-many and five many-to-many edges. The saved GWAS Catalog screening examined 1,198,394 association rows and retained 75 eligible exceptional-longevity rows from 15 study accessions. None matched the 21 candidates under the stated reported-gene or catalog-mapped-gene rules. Another 159 rows remained unresolved rather than being called negative findings.

The broader screen did contain a FOXO3 catalog-mapped row with an unresolved longevity definition, plus two candidate-gene rows excluded for mixed or proxy outcomes. These qualifications matter: neither the zero eligible matches nor the source table's omissions establish a gene-level null or lack of biological relevance.

## What the comparison shows

The zero eligible overlap applies to the stated mapping and catalog rules. Unresolved evidence remains unknown, so the screen cannot be read as a biological rejection of the candidate genes.

## Assumptions and limits

Zero eligible matches is not a biological null. Orthology ambiguity, phenotype definitions and catalog coverage constrain conclusions. Unresolved and excluded evidence must not be treated as negative findings; independent scientific rerun remains unverified.

## Sources and research materials

The unchanged research package comes from [upstream Case 22](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/a6034a3ce2fb272dc7d0f582b6c4c29c2d50f7ec/cases/case22). It includes the archived session, analysis materials, results and figures. The poster uses an AI-generated illustrative photograph. This introduction summarizes archived findings; the analysis was not rerun.
