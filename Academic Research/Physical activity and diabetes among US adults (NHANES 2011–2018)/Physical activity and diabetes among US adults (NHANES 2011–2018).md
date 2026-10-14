# Physical activity and diabetes among US adults (NHANES 2011–2018)

## Research question

How does the activity–diabetes prevalence contrast change after demographic and BMI adjustment?

Investigate the association between self-reported physical activity and prevalent diabetes among US adults in historical public NHANES data. Compare unweighted, survey-weighted and progressively adjusted analyses, while explaining why cross-sectional associations cannot establish a preventive effect. This case evaluates Open-Science's ability to execute and document a compact, inspectable survey analysis in R.

## Data and comparison design

Survey weighting and covariate adjustment serve different purposes: weighting accounts for the sampling design, while adjustment makes the comparison conditional on measured characteristics. Read the prevalence difference in percentage points and examine how it changes when BMI enters the model.

| Input or source | Role in this case | Source context |
| --- | --- | --- |
| [CDC NHANES 2011–2012](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?BeginYear=2011), [2013–2014](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?BeginYear=2013), [2015–2016](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?BeginYear=2015), [2017–2018](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?BeginYear=2017) | Official public DEMO, PAQ, DIQ, GHB, BMX and SMQ components | Use for statistical reporting and analysis only; do not attempt identification or linkage to individually identifiable data. See the [NCHS Data User Agreement](https://www.cdc.gov/nchs/policy/data-user-agreement.html). |
| [CDC NHANES weighting tutorial](https://wwwn.cdc.gov/nchs/nhanes/tutorials/weighting.aspx) | Survey-weighting and design guidance | Cite CDC methodology; the saved analysis records its own design choices and limitations |

## Recorded findings

| High-activity versus no-activity contrast | Recorded prevalence difference | Interpretation |
| --- | --- | --- |
| Survey-weighted | −10.38 percentage points | Accounts for sampling design. |
| Adjusted including BMI | −2.73 percentage points | Conditional on included measured characteristics. |
| Adjusted 95% CI | −4.04 to −1.41 points | Uncertainty for this historical association. |
| Analysis population | 18,241 adults, 2011–2018 | Cross-sectional complete-case comparison. |

In 18,241 complete-case adults, reporting at least 150 moderate-equivalent minutes of recreational activity per week versus none was associated with lower diabetes prevalence. The estimated high-versus-none gap was **−11.03 percentage points** unweighted, **−10.38 points** survey-weighted, **−5.33 points** after demographics, education, income and smoking, and **−2.73 points** after also adding BMI (95% CI −4.04 to −1.41). These are cross-sectional, model-dependent associations, not an intervention effect; complete-case selection, reverse causation and measurement error remain important limits.

## What the comparison shows

The narrower adjusted gap shows that crude group differences include other measured characteristics. Cross-sectional measurement cannot establish whether activity preceded diabetes or whether illness changed activity.

## Assumptions and limits

These historical cross-sectional associations are not preventive treatment effects or current US prevalence estimates. Complete-case selection, reverse causation and self-reported activity limit interpretation.

## Sources and research materials

The unchanged research package comes from [upstream Case 6](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/a6034a3ce2fb272dc7d0f582b6c4c29c2d50f7ec/cases/case6). It includes the archived session, analysis materials, results and figures. The poster uses an AI-generated illustrative photograph. This introduction summarizes archived findings; the analysis was not rerun.
