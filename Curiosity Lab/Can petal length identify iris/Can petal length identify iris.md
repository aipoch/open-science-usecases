# Can petal length identify iris

## Research question

How much species information is available from one flower measurement?

## Data and method

Compare pairwise cutoffs with a three-species rule, use millimetres consistently, and distinguish fitted cutoffs from cross-validated classification. Add petal width as a separate measurement to assess whether it improves the overlapping species pair.

## Recorded findings

Uses the local iris dataset to study classification from petal length alone and compare an additional measurement. The archived analysis includes cutoffs in millimetres, confusion counts, and uncertainty estimates.

The archive reports no pairwise errors for setosa against either other species, but seven errors in 100 versicolor/virginica observations. Ten-fold cross-validated error was 6.7% using length and 4.0% using length plus width.

## What the findings mean

The canonical balanced iris sample is not an external field survey. The reported improvement interval includes zero, so additional measurement is promising rather than conclusively better.

## Interpretation and limits

The canonical dataset is small and curated. Dataset separation and cross-validation do not directly measure field performance with volunteer measurement error or different plant populations.

## Package and provenance

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.

## Import provenance

This introduction was imported from the GitHub case description. The archived export and poster retain their original contents. This reorganization did not rerun the study or independently reverify its external sources or conclusions.
