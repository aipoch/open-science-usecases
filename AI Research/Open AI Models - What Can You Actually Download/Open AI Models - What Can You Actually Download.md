# Open AI Models - What Can You Actually Download

## Research question

What is open in a named model release: weights, supporting files, training assets, or reproducible evaluation?

## Data and method

Use a release-by-release availability matrix and retain retrieval failures instead of treating them as absence. Compare supplied file hashes and sizes, then separate verified snapshot integrity from licensing and training reproducibility.

## Recorded findings

Audits what can be downloaded for eight named model releases, separating weights, supporting files, training materials, and evaluation instructions. The corrected archive records snapshot integrity checks and unresolved retrieval failures.

The corrected archive records 76 exact file matches, no unresolved integrity mismatches, and three oversized-dataset retrieval failures that remain in the audit.

## What the findings mean

Downloadable weights do not imply a reproducible training pipeline. Current access and license conclusions require checking the exact release and terms.

## Interpretation and limits

This is a dated availability audit, not a current catalogue. Public files or verified snapshot hashes do not imply that all training inputs and steps needed for reproduction are available.

## Package and provenance

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.

## Import provenance

This introduction was imported from the GitHub case description. The archived export and poster retain their original contents. This reorganization did not rerun the study or independently reverify its external sources or conclusions.
