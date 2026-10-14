# Open AI Models - What Can You Actually Download

## Research question

What is open in a named model release: weights, supporting files, training assets, or reproducible evaluation?

Audits what can be downloaded for eight named model releases, separating weights, supporting files, training materials, and evaluation instructions. The corrected archive records snapshot integrity checks and unresolved retrieval failures.

## Data and comparison design

The analysis uses a release-by-release availability matrix and retain retrieval failures instead of treating them as absence. Compare supplied file hashes and sizes, then separate verified snapshot integrity from licensing and training reproducibility.

## Recorded findings

| Audit outcome | Final recorded count | Interpretation |
| --- | --- | --- |
| Exact hash-and-size matches | 76 | Downloaded bytes match the retained evidence manifest. |
| Unresolved integrity mismatches | 0 | No unresolved mismatch in the corrected final audit. |
| Oversized-dataset retrieval failures | 3 | Remain failed retrievals, not absent or corrupt scientific resources. |
| Inspection scope | Files actually retrieved and checked | Downloadability is different from buildability or proof validity. |

The corrected archive records 76 exact file matches, no unresolved integrity mismatches, and three oversized-dataset retrieval failures that remain in the audit.

This case inventories accessible materials instead of judging model quality from a repository name. A file can be listed but fail retrieval, download successfully but have a wrong checksum, or pass byte integrity yet lack the dependencies needed for execution. The corrected audit separates those outcomes. The three oversized-dataset failures remain part of the record; they are not converted into successful checks by the absence of unresolved integrity mismatches.

## What the comparison shows

Downloadable weights do not imply a reproducible training pipeline. Current access and license conclusions require checking the exact release and terms.

## Assumptions and limits

This is a dated availability audit, not a current catalogue. Public files or verified snapshot hashes do not imply that all training inputs and steps needed for reproduction are available.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
