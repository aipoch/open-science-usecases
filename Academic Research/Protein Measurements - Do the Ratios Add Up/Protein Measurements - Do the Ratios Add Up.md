# Protein Measurements - Do the Ratios Add Up

## Research question

Do measured protein-channel ratios recover the intended spike-in quantities?

Assess whether deposited PRIDE PXD000001 processed TMT measurements recover the intended spike-in ratios, separating correlation from absolute agreement and evaluating conditional additional background scaling. This is a processed-data study, not raw-spectrum re-quantification.

## Data and comparison design

The comparison uses observed ratios with known intended ratios, using correlation for ordering and log2 RMSE for numerical accuracy. Evaluate additional background scaling against the same contrasts, while recognizing that channels sharing a reference are dependent.

| Input or source | Role in this case | Source context |
| --- | --- | --- |
| [PRIDE PXD000001](https://www.ebi.ac.uk/pride/archive/projects/PXD000001) | Deposited quantitative results and design records; preserve source attribution and inspect the source reuse terms. | Retain attribution and source terms; this README grants no additional reuse rights |
| [Deposited mzTab](https://ftp.pride.ebi.ac.uk/pride/data/archive/2012/03/PXD000001/F063721.dat-mztab.txt) | Six-channel peptide counts with source line traceability. | Retain attribution and source terms; this README grants no additional reuse rights |
| [Community SDRF](https://ftp.pride.ebi.ac.uk/pride/data/archive/2012/03/PXD000001/PXD000001_community_annotated.sdrf.tsv) | Intended channel ratios, cross-checked against original PRIDE XML. | Retain attribution and source terms; this README grants no additional reuse rights |

## Recorded findings

| Ratio-recovery measure | Recorded result | Interpretation |
| --- | --- | --- |
| Contrasts | 20 protein/channel comparisons | Dependent measurements with a common reference. |
| Correlation | r = 0.984 | Strong ordering, not accurate magnitudes. |
| Original log2 RMSE | 0.45354 | Ratios remain compressed. |
| After background scaling | 0.45322 | Less than 0.1% improvement; does not resolve the compression. |

The export contains 1,528 peptide rows and 9,168 positive abundance values. There are 62 spike-in rows (13/20/27/2 for enolase/BSA/PhosB/cytochrome c), 1,462 background rows and four trypsin rows excluded from scaling and spike evaluation. The primary denominator is 20 protein/channel contrasts per method. As-deposited versus additionally scaled RMSE is 0.4535444764 versus 0.4532193747 log2 units; slopes are 0.7416403057 versus 0.7391410149, and Pearson correlations 0.9843382383 versus 0.9825628452. Thus strong association coexists with compressed ratios, and scaling changes overall RMSE by less than 0.1%. The 0.8–1.25 multiplicative-tolerance counts are 12/20 and 13/20.

The original session records scientific execution and repeatability checks; this local preparation does not re-execute them. Scientific artifacts included in this selected export:

These files are within session.science and its embedded archive; they are not separate files alongside this README. No empty inputs/expected/outputs/attachments directories or duplicate extracted datasets are created.

## What the comparison shows

The high correlation and compressed ratios illustrate that tracking a pattern is easier than recovering its magnitude. The tiny RMSE change gives little support for a practical improvement from the extra scaling step.

## Assumptions and limits

High correlation does not imply accurate ratio recovery. This processed-data study uses one acquisition, with dependent peptide and common-reference contrasts; prior normalization is undocumented. It neither re-quantifies raw spectra nor identifies the cause of compression.

## Sources and research materials

The unchanged research package comes from the [upstream archive](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/4a22011b2b0d08492b55d75798ecb29acbeba32c/cases/case3). It retains the original conversation and included scientific artifacts, including analysis code, results and figures. The poster is an AI-generated thematic illustration, not study evidence. This introduction summarizes archived findings; the analysis was not rerun. Later bounded checks do not certify the entire study or mean the original package was corrected.
