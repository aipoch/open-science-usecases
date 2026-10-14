# 2,000 Natural Products - How Diverse Are They

## Research question

Can a small representative subset cover the structural variety of the captured natural-product pool?

Explore structural diversity in at most 2,000 sampled public COCONUT records, choose a small representative set, and explain how sampling and structural-similarity definitions affect the result. Use local computation, inspectable code, standalone tables/figures and an offline rerun bundle.

## Data and comparison design

Morgan fingerprints describe local molecular environments. Nearest-representative similarity asks how well each molecule is covered; the average and the least-covered molecule answer different questions. Compare representative-selection criteria on the same pool and fingerprint definition.

| Input or source | Role in this case | Source context |
| --- | --- | --- |
| [COCONUT download page](https://coconut.naturalproducts.net/download) | Official dataset entry point | Saved provenance records the curated release's CC0 designation; see qualification below |
| [October 2026 lite CSV ZIP](https://coconut.s3.uni-jena.de/prod/downloads/2026-10/coconut_csv_lite-10-2026.zip) | Captured source release | Archive SHA-256 `a602502a4fa0950cc2e59eed690dccd082d1a051bf9f85ccda50a82dd22ca154` |

## Recorded findings

| Selection or coverage measure | Recorded value | Meaning |
| --- | --- | --- |
| Captured modeling pool | 2,000 records | The bounded sample, not all natural products. |
| Morgan representatives | 12 | Farthest-first selection under one fingerprint definition. |
| Mean nearest similarity | 0.1916 | Average coverage of the pool. |
| Similarity ≥0.5 | 178/2,000 = 8.90% | Most sampled records do not meet this coverage threshold. |

All 2,000 sampled records parsed and were unique under isomeric canonical SMILES. All fragments and supplied charges/stereochemistry were retained; no parent stripping or post-hoc outlier removal was used. The outputs contain 1,494 nonempty scaffolds and 244 acyclic records.

The primary set contains **12 Morgan-selected representatives**; a separate 12-member MACCS set is a sensitivity comparison. The sets share two IDs. Morgan-selected/Morgan-evaluated mean nearest similarity is **0.1916368529**, worst similarity **0.0666666667**, and **178/2,000 (8.90%)** reach similarity 0.5. MACCS-selected/Morgan-evaluated mean is **0.1470678059**. Random 12-member sets have mean coverage **0.214546 ± 0.021927 sample SD**, illustrating that farthest-first improves worst coverage at a cost to average coverage.

Twenty permutations per subset size distinguish coverage SD from representative-overlap SD. Coverage SD decreases for sizes 500/1,000/1,500, while overlap SD is not consistently decreasing. Zero SD at 2,000 reflects deterministic selection from the identical captured pool, not elimination of population uncertainty. The older September wording defect is absent from this corrected final report.

## What the comparison shows

A representative set can look diverse while leaving most of the pool poorly represented. The similarity threshold makes that coverage tradeoff visible; it is not a biological activity threshold.

## Assumptions and limits

Results depend on the captured pool, fingerprint and selection criterion, rather than representing all natural products or screening suitability. Zero variability when reusing the complete pool is not zero population uncertainty. The history also records optional documentation access after denial; that response was excluded from licensing evidence, and subsequent review did not erase the operational exception.

## Sources and research materials

The unchanged research package comes from the [upstream archive](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/4a22011b2b0d08492b55d75798ecb29acbeba32c/cases/case19). It retains the original conversation and included scientific artifacts, including analysis code, results and figures. The poster is an AI-generated thematic illustration, not study evidence. This introduction summarizes archived findings; the analysis was not rerun. Later bounded checks do not certify the entire study or mean the original package was corrected.
