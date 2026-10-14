# Where Do AlphaFold Protein Structures Lose Confidence

## Research question

Where is local confidence low within a predicted protein rather than merely low on average?

Examines confidence profiles in three archived AlphaFold protein models, summarizes pLDDT, and locates continuous low-confidence regions. The record includes structural visualizations and source identifiers.

## Data and comparison design

The analysis uses canonical model identifiers, compute residue-level pLDDT summaries, and define a low-confidence segment as a maximal contiguous run below 70. Compare mean and median values with the longest run and the fraction below each threshold.

## Recorded findings

Analyzed canonical AlphaFold DB v6 models for three human proteins. A low-confidence region was defined as a maximal continuous run with pLDDT <70.

| Protein | Length | Mean pLDDT | Median | pLDDT <50 | pLDDT <70 | Longest low-confidence run |
|---|---:|---:|---:|---:|---:|---|
| TP53 / P04637 | 393 | 75.1 | 91.6 | 29.8% | 40.2% | 26–93 (68 aa) |
| BRCA1 / P38398 | 1,863 | 41.6 | 31.2 | 80.4% | 82.6% | 101–1391 (1,291 aa) |
| SNCA / P37840 | 140 | 75.2 | 85.2 | 12.9% | 37.1% | 89–140 (52 aa) |

Principal low-confidence regions:

- TP53: 1–19, 26–93, 293–323, and 356–393. Two isolated residues at 183 and 185 also fall below 70.
- BRCA1: 101–1391 and 1420–1648 dominate the model; several short terminal runs are also present.
- α-synuclein: one continuous run, 89–140.

These patterns are consistent with confident compact domains separated by flexible or disordered regions—especially in BRCA1. However, that interpretation is biological context, not proof from pLDDT alone.

Crucially, pLDDT is the model’s local confidence estimate, not experimental accuracy. High pLDDT does not demonstrate that a conformation exists in vivo, has the correct domain arrangement, or matches a particular functional state. Conversely, low pLDDT often reflects intrinsic disorder, flexibility, alternative conformations, or insufficient evolutionary information—not necessarily a modeling “error.” Experimental structures and biochemical evidence remain necessary for validation.

## What the comparison shows

pLDDT estimates local confidence, not experimentally observed accuracy or the correctness of domain arrangement in a functional state.

## Assumptions and limits

pLDDT is predicted local confidence, not experimental accuracy or proof of a biological conformation. Low-confidence regions require interpretation beyond the score alone.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
