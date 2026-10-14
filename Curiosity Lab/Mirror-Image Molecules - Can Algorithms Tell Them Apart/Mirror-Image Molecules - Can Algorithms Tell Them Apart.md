# Mirror-Image Molecules - Can Algorithms Tell Them Apart

## Research question

Which molecular representation makes enantiomers distinguishable to a fingerprint?

Compares molecular fingerprints for enantiomer pairs with chirality enabled and disabled. Follow-up checks examine how SMILES, InChI reconstruction, tautomer choice, and stereochemistry handling affect similarity.

## Data and comparison design

The same enantiomer pair is fingerprinted with chirality disabled and enabled. A second comparison changes the input route from isomeric SMILES to Standard InChI reconstruction. Stereocenter assignments and mirror-inversion checks are retained so a similarity change can be attributed to representation or tautomer handling rather than an unnoticed swap of enantiomer labels.

## Recorded findings

**Confirmed. The original comparison uses PubChem’s isomeric SMILES**, parsed with `Chem.MolFromSmiles`, without tautomer standardization.

For asparagine, SMILES produces the **amide** form, whereas parsing its Standard InChI produces an **imidic-acid tautomer**. Standard InChI normalizes certain mobile-hydrogen arrangements, so reconstructing it need not recover the original tautomer.

| L/D pair similarity | SMILES input | InChI input |
|---|---:|---:|
| Morgan, chirality off | 1.000000 | 1.000000 |
| Morgan, chirality on | 0.619048 | 0.636364 |
| Atom-pair, chirality off | 1.000000 | 1.000000 |
| Atom-pair, chirality on | 0.657895 | 0.650000 |

Both routes preserve **L = S and D = R** and pass mirror-inversion checks. The scores change because hydrogen placement and bond orders affect fingerprint features—not because the enantiomer assignments changed.

The archived checks also found that default RDKit tautomer canonicalization removed the stereocenter annotation here. Preserving tetrahedral stereochemistry explicitly made both input routes converge to the amide while retaining S/R.

## What the comparison shows

A fingerprint similarity is representation-dependent, not a direct measure of molecular interchangeability or biological effect.

## Assumptions and limits

Representation choices change fingerprints without necessarily changing the handedness assignment. A similarity score does not establish equal biological effects or replace experimental evidence.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
