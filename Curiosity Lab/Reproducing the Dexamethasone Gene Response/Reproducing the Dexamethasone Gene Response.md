# Reproducing the Dexamethasone Gene Response

**Creator:** @servasyy_ai  

## Research question

How can a paired expression analysis assess a drug-response signal while accounting for donor differences?

Reanalyzes the airway dataset associated with GSE52778 using eight untreated/dexamethasone samples and DESeq2. The paired design ~ cell + dex accounts for donor differences. The archived task includes a volcano plot, a ranked gene table, CRISPLD2 assessment, and a comparison with a reported 316-gene result in the source publication.

## Data and comparison design

The analysis uses the airway count data with untreated and dexamethasone samples and a ~ cell + dex design. Keep the gene-level effect, adjusted significance, and the total number meeting a stated threshold distinct; compare the paired design with a model omitting the donor term.

## Recorded findings

| Analysis stage | Recorded material | Why it belongs in the report |
| --- | --- | --- |
| Input and design | Public airway expression data; paired design | Donor pairing must be represented in the comparison. |
| Differential expression | Ranked genes and model-based contrasts | Direction and ranking must be read with the design and filtering. |
| Visual summary | Volcano plot | Displays effect size alongside statistical evidence. |
| Publication comparison | Documented comparison with the source report | Supports an inspectable reproduction without restoring removed numerical claims. |

The archive contains a volcano plot, ranked genes, and a documented comparison with the source publication. This draft retains those completed analysis components without reinstating previously removed numerical claims.

The central modeling decision is the paired design, written in the archived analysis as `~ cell + dex`. The cell term accounts for baseline differences between the matched cell lines, while the dex term represents the treatment contrast. Omitting the cell term changes the comparison and can change the precision or ranking of estimated effects.

1. Inspect the airway count matrix and sample metadata, including treated and untreated labels.
2. Fit the treatment contrast with the archived paired design and retain the filtering and model choices.
3. Read the volcano plot together with the ranked gene table: effect magnitude and adjusted statistical evidence answer different questions.
4. Compare the paired results with the model lacking the donor term and with the source publication.

The plot is a summary of gene-level contrasts, not an independent validation of drug mechanism. A gene can have a large estimated change with weak statistical support, or a modest change with stronger support. The reproduction materials make those judgments inspectable without restoring the numerical result claims removed in the earlier review.

## What the comparison shows

Different processing and filtering choices can change the differential-gene count. Reanalysis is not automatically exact reproduction.

## Sources and research materials

Creator attribution follows the signature on the supplied poster and matches Case Index.csv. The original session export and poster are preserved from AIPOCH-Creator-Use-Cases.zip. This introduction describes the archived research workflow.
