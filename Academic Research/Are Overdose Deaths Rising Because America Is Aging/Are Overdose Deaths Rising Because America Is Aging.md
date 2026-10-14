# Are Overdose Deaths Rising Because America Is Aging

## Research question

Could changing population age composition explain the historical rise in overdose mortality?

Investigate how population age structure changes the interpretation of US national drug-overdose mortality trends. Compare crude and officially age-adjusted rates, then use the available broad age groups to assess demographic composition separately. The target audience is a reviewer of the research answer and Open-Science workflow. The initial request leaves the manageable period and defensible methods to the native Plan; the selected analysis uses 1999–2016.

## Data and comparison design

The analysis separates death counts, crude rates and age-adjusted rates before decomposing change into age composition and age-specific mortality. Counts also reflect population size; standardized rates ask what change remains when age weights are held comparable.

| Input or source | Role in this case | Source context |
| --- | --- | --- |
| [CDC dataset metadata](https://data.cdc.gov/api/views/xbxb-epbu.json) | Definitions, standardization and denominator history | Exact retrieved metadata snapshot is preserved in the bundled analysis; consult source terms for reuse |

## Recorded findings

| National summary | 1999 | 2016 or recorded change |
| --- | --- | --- |
| Overdose deaths | 16,849 | 63,632 |
| Crude and official age-adjusted rates | Historical baseline | Both rise by about 226% |
| Broad-age composition term | Age-group decomposition | Slightly offsets rather than explains the increase |

The chosen source provides 162 national year/age rows over 18 years: one all-age and eight broad-age rows per year. Endpoint deaths increase from 16,849 to 63,632. Crude rates increase from 6.0382 to 19.6925 per 100,000, and official adjusted rates from 6.0570 to 19.7851. Published-rate increases are 226.13% and 226.65%, respectively.

The symmetric broad-age decomposition gives within-age change +13.895354, composition change -0.238376 and residual change -0.002639 per 100,000, reconciling to +13.654338. The composition term offsets about 1.75% of the net increase. This is descriptive accounting, not a causal attributable fraction. The result applies to 1999–2016, not current overdose trends.

## What the comparison shows

The composition component offsets rather than explains the recorded increase. That accounting result directs attention to changing within-age mortality without identifying its causes.

## Assumptions and limits

The decomposition is descriptive accounting, not causal attribution. Broad age bands retain within-band aging, and official fine-age adjustment and its confidence intervals were not independently reconstructed. The findings concern the historical period, not current overdose trends.

## Sources and research materials

The unchanged research package comes from the [upstream archive](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/4a22011b2b0d08492b55d75798ecb29acbeba32c/cases/case1). It retains the original conversation and included scientific artifacts, including analysis code, results and figures. The poster is an AI-generated thematic illustration, not study evidence. This introduction summarizes archived findings; the analysis was not rerun. Later bounded checks do not certify the entire study or mean the original package was corrected.
