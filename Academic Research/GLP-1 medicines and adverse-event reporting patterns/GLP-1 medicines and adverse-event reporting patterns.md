# GLP-1 medicines and adverse-event reporting patterns

## Research question

Are particular events disproportionately reported with the selected medicines in the frozen FAERS snapshot?

Examine disproportionate reporting for two selected GLP-1 medicines and two exact adverse-event terms in one complete public FDA quarterly release. This is a reporting-pattern analysis, **not** an estimate of clinical incidence, causality, or comparative drug safety.

## Data and comparison design

A reporting odds ratio compares the balance of event and other-event reports for a medicine with the corresponding comparator reports. Case eligibility and matching rules define that comparison. FAERS provides reports, rather than the total number of treated or untreated people.

| Input or source | Role in this case | Source context |
| --- | --- | --- |
| [FDA quarterly extract listing](https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html) | Identifies the 2026 Q2 ASCII release | Public FDA source, inspected 2026-10-08 |
| [FDA 2026 Q2 ASCII ZIP](https://fis.fda.gov/content/Exports/faers_ascii_2026q2.zip) | Original quarterly reporting tables and documentation | Retained in the Session; cite FDA and respect source-specific reuse terms |
| [FDA AEMS limitations](https://www.fda.gov/drugs/fda-adverse-event-monitoring-system-aems/fda-adverse-event-monitoring-system-aems-public-dashboard) | Interpretation of spontaneous-reporting data | Reports do not establish incidence or causation |

## Recorded findings

| Drug | Pancreatitis reporting odds ratio | Cholelithiasis reporting odds ratio |
| --- | --- | --- |
| Semaglutide | 4.20 | 4.60 |
| Liraglutide | 3.58 | 6.71 |
| Eligible FAERS cases | 422,458 in 2026 Q2 | Frozen primary matching rules |
| Measure boundary | Reporting disproportionality | Not incidence or a head-to-head clinical safety ranking |

The analysis retained **422,458 eligible unique cases** from FDA FAERS 2026 Q2. All four planned exact-term comparisons were estimable. Primary reporting odds ratios were 4.20 for semaglutide–Pancreatitis, 4.60 for semaglutide–Cholelithiasis, 3.58 for liraglutide–Pancreatitis, and 6.71 for liraglutide–Cholelithiasis. The report supplies raw cell counts, intervals, Holm-adjusted tests, suspect-role sensitivity estimates, and limitations. Liraglutide co-reporting counts are sparse; combination products and an ambiguous brand-containing name remain under the frozen matching rule and are disclosed.

## What the comparison shows

The ratios flag reporting patterns for investigation. Differences between medicines can reflect reporting and use patterns, so these values cannot rank their absolute clinical risks.

## Assumptions and limits

Reporting odds ratios are not incidence, causality or head-to-head safety rankings. Reporting bias, absent exposure denominators and sparse co-reports limit interpretation. The corrected reproduction bundle fixes metadata without changing scientific results.

## Sources and research materials

The unchanged research package comes from [upstream Case 26](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/a6034a3ce2fb272dc7d0f582b6c4c29c2d50f7ec/cases/case26). It includes the archived session, analysis materials, results and figures. The poster uses an AI-generated illustrative photograph. This introduction summarizes archived findings; the analysis was not rerun.
