# Registry-results availability in completed glioblastoma trials

## Research question

How often do the eligible completed trials show registry results in the captured snapshot?

Assess how often a bounded set of completed interventional glioblastoma trials have results indicated in their public ClinicalTrials.gov registry records, and describe how that availability varies with time since primary completion. Preserve the source snapshot, trial-level decisions and calculations so that the analysis can be inspected and rerun. This case evaluates a descriptive registry workflow, not publication status, legal compliance, treatment efficacy or a time-to-posting model.

## Data and comparison design

The analysis uses the fixed eligible cohort and snapshot date, then group trials by elapsed time since completion. Registry availability is a status at observation; without posting histories it does not identify when results first appeared or whether a deadline was met.

| Input or source | Role in this case | Source context |
| --- | --- | --- |
| [ClinicalTrials.gov](https://clinicaltrials.gov/) | Public trial registry represented by the connector's normalized responses | Credit the registry; this archive is a dated extract, not complete raw API records or historical versions |

## Recorded findings

| Elapsed-time summary | Trials with registry results | Interpretation |
| --- | --- | --- |
| All eligible trials | 33/80 = 41.25% | September 2026 bounded snapshot. |
| Increasing elapsed-time groups | 0/1; 11/33; 10/24; 12/22 | Youngest group contains only one trial. |
| Posting-history availability | Incomplete | No legal-deadline or time-to-first-posting conclusion. |
| Missing registry results | Not a publication-status finding | Results may be reported outside the registry. |

In the saved cohort, 33 of 80 included trials (41.25%) had registry results indicated. The four elapsed-time groups were: less than one year, 0/1; one to less than three years, 11/33; three to less than five years, 10/24; and at least five years, 12/22. Seven included primary-completion dates specified only a month; earliest, midpoint and latest date interpretations changed no timing group. The Session records a second offline execution that reproduced both calculation CSVs byte for byte.

## What the comparison shows

The older groups have more visible registry results in this snapshot. The pattern cannot distinguish delayed posting, publication elsewhere or differences in trial eligibility.

## Assumptions and limits

This bounded cross-sectional cohort does not represent every glioblastoma trial. Missing registry results do not prove nonpublication or legal violations. Incomplete posting histories prevent deadline analysis, and the youngest group contains only one trial.

## Sources and research materials

The unchanged research package comes from [upstream Case 16](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/a6034a3ce2fb272dc7d0f582b6c4c29c2d50f7ec/cases/case16). It includes the archived session, analysis materials, results and figures. The poster uses an AI-generated illustrative photograph. This introduction summarizes archived findings; the analysis was not rerun.
