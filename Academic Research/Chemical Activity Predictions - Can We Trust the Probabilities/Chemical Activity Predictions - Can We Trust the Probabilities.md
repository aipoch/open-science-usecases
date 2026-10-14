# Chemical Activity Predictions - Can We Trust the Probabilities

## Research question

Can a model rank assay-active compounds and also assign reliable activity probabilities?

Use public Tox21 structures to assess manageable SR-MMP classification, probability calibration and chemical coverage. The endpoint is in-vitro mitochondrial membrane potential activity, not human liver toxicity. The selected deliverable is the second reviewed attempt (9-2).

## Data and comparison design

Scaffold separation tests compounds outside the training cores. AUC measures ranking, whereas Brier score measures squared probability error. Calibration adjusts the probability scale; coverage heuristics ask a separate question about resemblance to known chemistry.

| Input or source | Role in this case | Source context |
| --- | --- | --- |
| [DeepChem/MoleculeNet Tox21 CSV](https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/tox21.csv.gz) | Benchmark structures and binary endpoint labels; preserve source provenance and inspect upstream usage terms. | Retain attribution and source terms; this README grants no additional reuse rights |
| [NIH Tox21 challenge data](https://tripod.nih.gov/tox21/challenge/data.jsp) | Label definitions and link to assay AID 720637. | Retain attribution and source terms; this README grants no additional reuse rights |
| [NIH endpoint definitions](https://tripod.nih.gov/tox21/challenge/about.jsp) | MMP endpoint context. | Retain attribution and source terms; this README grants no additional reuse rights |
| [PubChem AID 720637](https://pubchem.ncbi.nlm.nih.gov/bioassay/720637) | Linked reference; the assay record itself was not downloaded by the original connector. | Retain attribution and source terms; this README grants no additional reuse rights |

## Recorded findings

| Test measure | Before calibration | After calibration or scope |
| --- | --- | --- |
| Brier score | 0.12964 | 0.11528 |
| Ranking AUC | 0.797 | Calibration and ranking are distinct evaluations. |
| Holdout | 945 structures | Scaffold-separated chemical population. |
| Coverage heuristic | Chemical resemblance screening | Not shown to remove high-error predictions. |

Of 7,831 source rows, 5,395 unique labeled structures remain. Training/calibration/test sizes are 3,508/942/945, with 518/168/168 actives. The scaffold-held-out test gives AUC 0.797186 and AP 0.515864 versus prevalence 0.177778. Calibration changes Brier from 0.129641 to 0.115279 and log loss from 0.444370 to 0.375025. At the calibration-F1-selected threshold, TP/FP/FN/TN are 125/219/43/558. A heuristic screen marks 773 supported and 172 flagged, without establishing that it removes high-error predictions.

The original session records scientific execution and repeatability checks; this local preparation does not re-execute them. Scientific artifacts included in this selected export:

These files are within session.science and its embedded archive; they are not separate files alongside this README. No empty inputs/expected/outputs/attachments directories or duplicate extracted datasets are created.

## What the comparison shows

Improved probability calibration can coexist with unchanged ranking. Neither metric converts an in-vitro assay endpoint into a clinical toxicity probability.

## Assumptions and limits

The endpoint is in-vitro mitochondrial membrane potential activity, not human toxicity. Sparse chemical strata, fingerprint collisions and single-split uncertainty limit generalization. A later check identified a displayed interval endpoint that should read **−0.00413 rather than −0.00414**; the original package remains unchanged, and the calibration conclusion is unaffected.

## Sources and research materials

The unchanged research package comes from the [upstream archive](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/4a22011b2b0d08492b55d75798ecb29acbeba32c/cases/case9). It retains the original conversation and included scientific artifacts, including analysis code, results and figures. The poster is an AI-generated thematic illustration, not study evidence. This introduction summarizes archived findings; the analysis was not rerun. Later bounded checks do not certify the entire study or mean the original package was corrected.
