# Light-Activated Neurons - Does the Cutoff Matter

## Research question

Which response classifications survive changes in window, effect threshold, and multiplicity correction?

## Data and method

Vary the specified analysis settings while tracking neuron identity. Replace a finite Monte Carlo p-value floor with exact probabilities where available, and compare per-window corrections with corrections spanning all windows.

## Recorded findings

Revisits the optotagging data across response windows, effect thresholds, and multiple-testing corrections. The final analysis replaces a limiting Monte Carlo probability floor with exact probabilities while retaining the original reference.

The reference count remains 31, but the exact-probability analysis identifies 11 units stable across window-wide corrections where the original floor yielded none. The 13-unit per-window stable core keeps its identities.

## What the findings mean

Sensitivity to a numerical probability floor is a computational issue. Stability across settings is not proof of direct optical activation.

## Interpretation and limits

Selection stability is a statistical property under specified choices, not proof of direct activation. The original and corrected calculations should not be conflated.

## Package and provenance

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.

## Import provenance

This introduction was imported from the GitHub case description. The archived export and poster retain their original contents. This reorganization did not rerun the study or independently reverify its external sources or conclusions.
