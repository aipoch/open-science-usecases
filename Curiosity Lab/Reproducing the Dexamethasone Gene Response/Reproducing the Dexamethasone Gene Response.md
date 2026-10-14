# Reproducing the Dexamethasone Gene Response

**Creator:** @servasyy_ai

## Research question

How can a paired expression analysis assess a drug-response signal while accounting for donor differences?

## Data and method

Use the airway count data with untreated and dexamethasone samples and a ~ cell + dex design. Keep the gene-level effect, adjusted significance, and the total number meeting a stated threshold distinct; compare the paired design with a model omitting the donor term.

## Recorded findings

Reanalyzes the airway dataset associated with GSE52778 using eight untreated/dexamethasone samples and DESeq2. The paired design ~ cell + dex accounts for donor differences. The archived task includes a volcano plot, a ranked gene table, CRISPLD2 assessment, and a comparison with a reported 316-gene result in the source publication.

The archive contains a volcano plot, ranked genes, and a documented comparison with the source publication. This draft retains those completed analysis components without reinstating previously removed numerical claims.

## What the findings mean

Different processing and filtering choices can change the differential-gene count. Reanalysis is not automatically exact reproduction.

## Scope

This case is a reanalysis using a paired DESeq2 design. Its differential-gene totals differ from the source publication, so it should not be described as an exact reproduction.

## Package and provenance

Creator attribution follows the signature on the supplied poster and matches Case Index.csv. The original session export and poster are preserved from AIPOCH-Creator-Use-Cases.zip. This introduction describes the archived research workflow.
