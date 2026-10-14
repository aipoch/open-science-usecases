# Mirror-Image Molecules - Can Algorithms Tell Them Apart

## Research question

Which molecular representation makes enantiomers distinguishable to a fingerprint?

## Data and method

Compare chirality-enabled and disabled fingerprints on the same pair, then check whether SMILES parsing, Standard InChI reconstruction, and tautomer handling preserve the same structure and stereocenters.

## Recorded findings

Compares molecular fingerprints for enantiomer pairs with chirality enabled and disabled. Follow-up checks examine how SMILES, InChI reconstruction, tautomer choice, and stereochemistry handling affect similarity.

For the archived asparagine pair, chirality-disabled similarities are 1.0 while chirality-enabled values are lower. Changing the input route changes those values without reversing the verified S/R assignments.

## What the findings mean

A fingerprint similarity is representation-dependent, not a direct measure of molecular interchangeability or biological effect.

## Interpretation and limits

Representation choices change fingerprints without necessarily changing the handedness assignment. A similarity score does not establish equal biological effects or replace experimental evidence.

## Package and provenance

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.

## Import provenance

This introduction was imported from the GitHub case description. The archived export and poster retain their original contents. This reorganization did not rerun the study or independently reverify its external sources or conclusions.
