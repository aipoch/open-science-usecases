# Light-Activated Neurons - Does the Cutoff Matter

## Research question

Which response classifications survive changes in window, effect threshold, and multiplicity correction?

Revisits the optotagging data across response windows, effect thresholds, and multiple-testing corrections. The final analysis replaces a limiting Monte Carlo probability floor with exact probabilities while retaining the original reference.

## Data and comparison design

Vary the specified analysis settings while tracking neuron identity. Replace a finite Monte Carlo p-value floor with exact probabilities where available, and compare per-window corrections with corrections spanning all windows.

## Recorded findings

**Yes—the Monte Carlo floor limited the strictest corrections.** Exact probabilities now drive all sensitivity comparisons; the original calculation is preserved separately.

At the highest light level:

| Result | Original | Exact |
|---|---:|---:|
| Reference selection | 31 | 31 |
| Always selected across per-window settings | 13 | 13 |
| Always selected across window-wide corrections | 0 | **11** |

For the reference window, across-window Holm correction at 0.01 changes from **3 to 22 neurons**. The 13-neuron stable core retains exactly the same identities.

The saved script regenerated all final figures and tables successfully. Statistical stability still does not establish direct activation.

## What the comparison shows

Sensitivity to a numerical probability floor is a computational issue. Stability across settings is not proof of direct optical activation.

## Assumptions and limits

Selection stability is a statistical property under specified choices, not proof of direct activation. The original and corrected calculations should not be conflated.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
