# Where Do AlphaFold Protein Structures Lose Confidence

## Research question

Where is local confidence low within a predicted protein rather than merely low on average?

## Data and method

Use canonical model identifiers, compute residue-level pLDDT summaries, and define a low-confidence segment as a maximal contiguous run below 70. Compare mean and median values with the longest run and the fraction below each threshold.

## Recorded findings

Examines confidence profiles in three archived AlphaFold protein models, summarizes pLDDT, and locates continuous low-confidence regions. The record includes structural visualizations and source identifiers.

The archived BRCA1 model has a long low-confidence interval from residues 101–1391; the TP53 and SNCA models have shorter localized intervals. This illustrates why one average can hide a heterogeneous profile.

## What the findings mean

pLDDT estimates local confidence, not experimentally observed accuracy or the correctness of domain arrangement in a functional state.

## Interpretation and limits

pLDDT is predicted local confidence, not experimental accuracy or proof of a biological conformation. Low-confidence regions require interpretation beyond the score alone.

## Package and provenance

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.

## Import provenance

This introduction was imported from the GitHub case description. The archived export and poster retain their original contents. This reorganization did not rerun the study or independently reverify its external sources or conclusions.
