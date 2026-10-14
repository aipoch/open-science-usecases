# Can petal length identify iris

## Research question

How much species information is available from one flower measurement?

Uses the local iris dataset to study classification from petal length alone and compare an additional measurement. The archived analysis includes cutoffs in millimetres, confusion counts, and uncertainty estimates.

## Data and comparison design

The comparison uses pairwise cutoffs with a three-species rule, use millimetres consistently, and distinguish fitted cutoffs from cross-validated classification. Add petal width as a separate measurement to assess whether it improves the overlapping species pair.

## Recorded findings

| Classification comparison | Recorded errors or rate | What changes |
| --- | --- | --- |
| Setosa versus either other species | No pairwise errors in the captured sample | The species is well separated in these measurements. |
| Versicolor versus virginica | 7 errors among 100 observations | These two species overlap in petal length. |
| Petal length, 10-fold CV | 6.7% error | A held-out estimate for the length-only rule. |
| Petal length + width, 10-fold CV | 4.0% error | The second measurement reduces error in this evaluation. |

Using the local, canonical R `iris` dataset (150 plants; 50 each of setosa, versicolor, virginica), petal length alone is useful but not uniformly reliable.

Key field cutoffs, in millimetres:

- **Setosa vs. versicolor:** cutoff at **24.5 mm**; **0/100 errors** in the pair.
- **Setosa vs. virginica:** cutoff at **32.0 mm**; **0/100 errors** in the pair.
- **Versicolor vs. virginica:** cutoff at **47.5 mm**; **7/100 errors** (**7%**). This is the overlapping pair.

A practical three-species rule is:

- `< 24.5 mm` → setosa
- `24.5–47.5 mm` → versicolor
- `> 47.5 mm` → virginica

With shuffled, stratified 10-fold cross-validation, petal length alone gave:

- **Accuracy:** 93.3%
- **Error rate:** **6.7%**
- Bootstrap 95% CI for error: **2.7%–10.7%**
- Confusion counts:

  - setosa: 50/50 correct
  - versicolor: 44/50 correct; **6/50 misclassified (12%)**
  - virginica: 46/50 correct; **4/50 misclassified (8%)**

So the bad case is versicolor: about **12% error** in this dataset. A simple Wilson 95% interval for that observed class error is approximately **5.6%–23.8%**. The interval is wide because there are only 50 plants per species, and this is not an external field-validation sample.

Adding petal width materially helps. A nearest-centroid classifier using petal length plus petal width reduced cross-validated error from **6.7% to 4.0%**, an absolute reduction of **2.7 percentage points**. The paired bootstrap 95% interval for the reduction was approximately **−0.7 to 6.7 percentage points**, so the improvement is plausible but not decisively established by this small benchmark.

Important limitation: these cutoffs are optimized on the standard iris dataset. Real populations, measurement error, cultivar variation, and observer disagreement may worsen performance. Treat the thresholds as a field-guide starting point, not a validated diagnostic standard.

Saved artifacts:

- iris_petal_field_guide_analysis.R — reproducible R analysis code

## What the comparison shows

The canonical balanced iris sample is not an external field survey. The reported improvement interval includes zero, so additional measurement is promising rather than conclusively better.

## Assumptions and limits

The canonical dataset is small and curated. Dataset separation and cross-validation do not directly measure field performance with volunteer measurement error or different plant populations.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
