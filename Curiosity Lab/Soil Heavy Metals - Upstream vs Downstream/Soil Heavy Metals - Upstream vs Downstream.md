# Soil Heavy Metals - Upstream vs Downstream

**Creator:** @RealYDT  

## Research question

Which measured characteristics differ between the two supplied site groups?

Analyzes the supplied soil_survey_2026.csv, using site_group 0 for upstream and 1 for downstream. The archived workflow summarizes 12 variables by group, plots lead concentrations, and retains a reusable analysis script. It also compares standardized effect sizes and Mann–Whitney U tests with Bonferroni adjustment.

## Data and comparison design

Retain the declared 0/1 grouping, tabulate count, mean, median, and spread for all variables, and show the lead distribution. Standardized effect sizes and adjusted rank-test results supplement rather than replace the original units and sample distributions.

## Recorded findings

| Evidence component | What is compared | Interpretation |
| --- | --- | --- |
| Group description | Upstream and downstream soil samples | Descriptive grouping does not by itself establish a source of pollution. |
| Multi-indicator tables | The supplied heavy-metal measurements by group | Units and denominators need to accompany each comparison. |
| Lead boxplot | Distribution and spread rather than just a group mean | Shows heterogeneity and possible influential observations. |
| Reusable script | Repeat the same summaries from the supplied table | Preserves the comparison workflow without reinstating removed numerical conclusions. |

The archived output contains descriptive tables, the lead boxplot, and a reusable script. This draft emphasizes the comparison workflow rather than reinstating previously removed numerical conclusions.

The first task is to retain the supplied meaning of the group code, rather than infer geography from an arbitrary zero or one. Descriptive statistics are calculated in the original measurement units. Means emphasize the total scale of the values; medians and the lead boxplot help reveal skew, spread and potentially influential observations.

1. Check variable types, missing values, duplicate sample identifiers and the declared upstream/downstream encoding.
2. Produce comparable group summaries for each measured indicator, keeping the unit and denominator with the result.
3. Examine the lead distribution visually instead of relying on a single average.
4. Read standardized effect sizes and adjusted rank tests alongside the descriptive values, not as replacements for them.

A group contrast can reflect different sampling locations, background geology or other unmeasured context. The comparison therefore describes the supplied soil samples; it does not establish a particular contamination source or a downstream causal effect. The reusable script and tables preserve the workflow while the previously removed numerical conclusions remain omitted.

## What the comparison shows

The upstream/downstream coding needs confirmation. Correlated metals should not be counted as independent causal evidence.

## Sources and research materials

Creator attribution follows the signature on the supplied poster and matches Case Index.csv. The original session export and poster are preserved from AIPOCH-Creator-Use-Cases.zip. This introduction describes the archived research workflow.
