# AqSolDB scaffold novelty and aqueous solubility prediction

## Research question

Does a solubility model retain its accuracy when test molecules come from held-out scaffolds?

Test whether a compact CPU-scale solubility model looks less accurate on unfamiliar molecular scaffolds than on an ordinary random split, and inspect what its largest errors and chemical-similarity patterns reveal. This is a bounded evaluation of model generalization and of Open-Science's inspectable research workflow, not a claim of universal performance on novel chemistry.

## Data and comparison design

A random split can distribute related molecular structures across training and test sets. A scaffold split groups molecules by a shared core before separation. Compare logS prediction error under both designs while checking which compounds, especially acyclic ones, remain eligible for each partition.

| Input or source | Role in this case | Source context |
| --- | --- | --- |
| [AqSolDB publication](https://doi.org/10.1038/s41597-019-0151-1) | Dataset description and curation context | Cite the publication; original measurements came from multiple prior sources |
| [Harvard Dataverse deposit](https://doi.org/10.7910/DVN/OVHAW8) | Original dataset deposit | Its API returned HTTP 403 in the saved run, so the deposited bytes could not be cross-checked |
| [Author's AqSolDB repository](https://github.com/mcsorkun/AqSolDB) | Public fallback snapshot at commit `8e02b548fd9a78778ff89a5aa9a460d1a289cc3a` | The repository states MIT and its notice is included in the embedded ZIP; preserve attribution and review underlying measurement-source terms before further reuse |

## Recorded findings

| Random-forest metric | Random split | Scaffold split |
| --- | --- | --- |
| Mean MAE | 0.700 logS | 0.812 logS |
| Mean RMSE | 0.987 logS | 1.109 logS |
| Curated modeling identities | 8,479 total | Five splits per protocol |
| Acyclic compounds | Not a separate novelty holdout | Remain in training in all scaffold splits |

After curation, 8,479 modeling identities remained. Across five splits, the fixed random forest's mean MAE rose from **0.700** on random splits to **0.812 logS** on scaffold splits (about 16%); RMSE rose from **0.987** to **1.109 logS**. One scaffold split was easier, and test compositions differed, so the difference is not a paired compound-level treatment effect. The report also documents larger errors at solubility extremes, imperfect protection from structural similarity, and missing experimental conditions. The acyclic group stayed in training in all five scaffold splits, limiting the novelty claim.

## What the comparison shows

The harder structural holdout reveals an accuracy loss hidden by ordinary random splitting. Because the test populations differ, the gap describes this evaluation design rather than a fixed cost of molecular novelty.

## Assumptions and limits

Test compositions differed, and acyclic compounds remained in training in every scaffold split. The difference is not a universal penalty for novel chemistry; incomplete experimental conditions also limit interpretation.

## Sources and research materials

The unchanged research package comes from [upstream Case 4](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/a6034a3ce2fb272dc7d0f582b6c4c29c2d50f7ec/cases/case4). It includes the archived session, analysis materials, results and figures. The poster uses an AI-generated illustrative photograph. This introduction summarizes archived findings; the analysis was not rerun.
