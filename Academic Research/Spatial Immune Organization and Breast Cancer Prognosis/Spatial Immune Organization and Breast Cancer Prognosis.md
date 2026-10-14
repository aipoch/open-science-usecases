# Spatial Immune Organization and Breast Cancer Prognosis

## Research question

Does spatial immune information improve prognosis prediction beyond clinical variables and cell composition?

Investigate whether spatial immune organization improves prognosis prediction beyond cell composition and basic clinical information in a public breast-cancer imaging cohort. The user requested processed coordinates and annotations with patient outcomes, local computation, explicit patient-level validation and uncertainty, and an inspectable, rerunnable workflow.

## Data and comparison design

The comparison uses nested feature sets using patient-level internal validation. Concordance assesses risk ordering, whereas the 60-month Brier score assesses prediction error at a stated time. Paired differences evaluate the added features against the baseline on the same validation patients.

| Input or source | Role in this case | Source context |
| --- | --- | --- |
| [Zenodo record 4607374](https://zenodo.org/records/4607374) | Jackson et al., The Single-Cell Pathology Landscape of Breast Cancer: processed coordinates, labels and metadata | The case report records a CC-BY designation; consult the source record for applicable terms. Third-party materials retain their source restrictions. |
| [Author analysis code](https://github.com/BodenmillerGroup/SCPathology_publication/tree/914cf2870e934990151c4872fff34856ff5615a5) | Source definitions and reference implementation | Retains upstream licensing and attribution requirements |

## Recorded findings

| Incremental prediction measure | Recorded change | Interpretation |
| --- | --- | --- |
| Cohort | 278 Basel breast-cancer patients | Patient-level internal validation. |
| Concordance | +0.0127 | Small favorable ordering change. |
| 60-month Brier error | −0.00163 | Small favorable prediction-error change. |
| Paired 95% intervals | Both include zero | Incremental value remains inconclusive. |

The exported research session ran on 2026-09-29. The report describes 278 patients, 284 images, 762,467 cells and 79 deaths. Regularized Cox models compare clinical information, clinical information plus composition, and those inputs plus spatial features. Validation uses three repeats of five outer patient folds with inner tuning; uncertainty uses 1,000 paired patient bootstrap draws conditional on the saved models, splits and censoring estimates.

Adding spatial features increased concordance by approximately 0.0127 and reduced Brier error by approximately 0.00163. Both paired intervals include zero. The report concludes that incremental prognostic value is inconclusive in this single cohort; it does not claim external or clinical validation.

## What the comparison shows

Small favorable point estimates with intervals spanning zero leave incremental value unresolved. Prediction improvement and clinical usefulness would still need separate evaluation even if the gain were more precise.

## Assumptions and limits

Incremental prognostic value remains inconclusive; this does not demonstrate that spatial biology has no prognostic value. The analysis uses one retrospective cohort and fixed public cell annotations. Uncertainty intervals hold fitted models and validation splits fixed, rather than capturing full retraining uncertainty. The results do not establish external validation or clinical utility.

## Sources and research materials

The unchanged research package comes from [upstream Case 28](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/dafedce528c9443a2611dc54b249f3d1e2050a73/cases/case28). It includes the conversation, source inputs, analysis code, results, and figures. The poster uses an illustrative microscope photograph, not an actual study image or experimental record. This introduction summarizes archived findings; the analysis was not rerun for this presentation.
