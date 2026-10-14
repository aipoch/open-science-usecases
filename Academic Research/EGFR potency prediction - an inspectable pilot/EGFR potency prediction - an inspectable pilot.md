# EGFR potency prediction - an inspectable pilot

## Research question

How much predictive performance survives separation by publication and by distant chemistry?

Determine whether public human EGFR activity measurements support a useful small compound-potency model. Assemble reasonably comparable biochemical IC50 observations, evaluate predictions for compounds withheld from training, challenge apparent performance with related-compound and source/assay holdouts, and retain enough evidence to inspect and rerun the calculations. This is an exploratory historical pilot, not a validated predictor for new EGFR chemistry or an assay-specific decision tool.

## Data and comparison design

An ordinary compound holdout can retain assay and publication context shared with training. The combined holdout makes that transfer harder. Compare absolute pIC50 error with within-assay rank correlation so that apparently acceptable pooled error does not obscure poor ordering within an assay.

| Input or source | Role in this case | Source context |
| --- | --- | --- |
| [ChEMBL human EGFR target CHEMBL203](https://www.ebi.ac.uk/chembl/explore/target/CHEMBL203) | Public activity measurements and source identifiers | Credit ChEMBL; this run used a frozen, ordered convenience sample, not the complete target dataset |

## Recorded findings

| Evaluation | Recorded result | Interpretation |
| --- | --- | --- |
| Curated pilot | 404 compounds | Convenience sample from the first 1,000 records. |
| Ordinary compound holdout MAE | 0.502 pIC50 | Easier retrospective partition. |
| Publication + distant-chemistry MAE | 0.788 pIC50 | Harder transfer across publication and chemistry. |
| Median within-assay rank correlation | 0.179 | Weak ordering can coexist with a usable-looking pooled error. |

The saved report describes six prespecified five-fold holdout protocols, including random compounds, scaffolds, chemical-similarity groups, assays, publications, and publications with close training analogues removed. The ridge model's mean absolute error was **0.502 pIC50 units** for ordinary compound holdouts and **0.788** for the combined publication-plus-distant-chemistry holdout. In that combined test it improved over two simple baselines, but median within-assay Spearman correlation across 14 sufficiently populated assays was only **0.179**. Thus the saved evidence is more encouraging for broad potency trends than reliable fine ranking within an unfamiliar assay or chemical series. The first-1,000-record convenience sample, missing wild-type annotation and incomplete assay protocols further limit generalization.

## What the comparison shows

The harder holdout and weak within-assay ranking expose limits of the pilot. Inspectability makes those limits easier to examine; it does not itself make the model ready for compound-selection decisions.

## Assumptions and limits

The first-1,000-record convenience sample and incomplete assay conditions limit generalization. This is an inspectable retrospective pilot, not a prospective predictor, mutant-EGFR validation or assay-specific decision tool.

## Sources and research materials

The unchanged research package comes from [upstream Case 14](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/a6034a3ce2fb272dc7d0f582b6c4c29c2d50f7ec/cases/case14). It includes the archived session, analysis materials, results and figures. The poster uses an AI-generated illustrative photograph. This introduction summarizes archived findings; the analysis was not rerun.
