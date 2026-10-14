# Mass Spectra - Can They Reveal a Chemical Family

## Research question

Can processed tandem mass spectra predict chemical family for held-out compound identities?

Build a bounded local chemical-class prediction benchmark from public tandem mass spectra and existing annotations, using identity-separated splits, simple controls, inspectable predictions and qualified generalization claims.

## Data and comparison design

The analysis separates compound groups across training, validation and test sets so repeat spectra of one compound do not bridge partitions. Compare family predictions with the precursor-only control, and read macro-F1 alongside accuracy to give minority classes a visible role.

## Recorded findings

| Compound-holdout evaluation | Recorded result | Interpretation |
| --- | --- | --- |
| Selected population | 2,000 compound groups; 3,849 spectra | Positive-ion GNPS tandem spectra; nine classes. |
| Accuracy | 51.0% | Compound identity separated across partitions. |
| Macro-F1 | 0.477 | Gives each chemical-family class a visible contribution. |
| Precursor-only macro-F1 | 0.107 | Control for information available without the full spectral pattern. |

The selected population contains 2,000 normalized groups and 3,849 spectra across nine classes. Training/validation/test contain 1,200/400/400 groups and 2,264/817/768 spectra. Primary compound holdout accuracy is 204/400 = 0.510 and macro-F1 is 0.476944; the saved 500-replicate percentile interval is 0.425356–0.527839. Precursor-only macro-F1 is 0.107186 and majority macro-F1 is 0.040445. The random-spectrum diagnostic gives macro-F1 0.615343 but contains substantial identity overlap; different populations prevent treating that difference as a causal leakage estimate.

No substantive defect requiring scientific correction was identified within the bounded checking scope. The review is not whole-study certification.

Latest scientific artifacts inside the session:

- `spectral_class_audit.tar.gz`

## What the comparison shows

The spectra contain predictive information beyond the precursor-only control in this selected population. Identity holdout still leaves broader chemistry and instrument transfer untested.

## Assumptions and limits

Identity separation does not establish scaffold, instrument or external-library generalization. The random-spectrum diagnostic uses a different population with identity overlap, so its higher score is not a causal estimate of leakage. Fitting-set ambiguities remain disclosed; source labels, fitting and bootstrap generation were not independently recreated.

## Sources and research materials

The unchanged research package comes from the [upstream archive](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/4a22011b2b0d08492b55d75798ecb29acbeba32c/cases/case27). It retains the original conversation and included scientific artifacts, including analysis code, results and figures. The poster is an AI-generated thematic illustration, not study evidence. This introduction summarizes archived findings; the analysis was not rerun. Later bounded checks do not certify the entire study or mean the original package was corrected.
