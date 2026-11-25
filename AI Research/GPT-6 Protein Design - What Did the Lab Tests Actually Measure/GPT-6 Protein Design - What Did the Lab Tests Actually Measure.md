What does a positive protein-binding screen establish about an AI-designed molecule—and which parts of the workflow did the AI actually perform? This case examines the reported GPT-6.2 minibinder laboratory screens, tracing structures, sequences, candidate selection and physical measurements separately. It recalculates percentages from published aggregate counts; it does not generate new proteins, rerun a model or conduct a laboratory experiment.

The main distinction is between **a contribution to one design stage** and **an end-to-end result from an assisted experimental workflow**. A binding-positive result after specialist filtering supports a narrower conclusion than independent replication, therapeutic function or unassisted protein design.

## Research question and source scope

The archived investigation asks what GPT-6.2 generated, which steps relied on other models or researchers, and what denominators underlie the reported binding counts. The public case title uses GPT-6, the model-family name; the laboratory paths examined here used a pre-released GPT-6.2 model.

The sources are the [OpenAI article dated 24 November 2026](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/) and its linked [protein-biology preprint](https://cdn.openai.com/pdf/gpt-6-a-universal-foundation-model-for-protein-biology.pdf), whose title page carries the same date. The archived full PDF retrieval on 25 November contains 183 pages. The retained review covers relevant results, methods and limitations, rather than claiming an exhaustive review of every page.

The article and paper describe the same collaboration. They provide complementary detail, not two independent experimental confirmations. Antibody-redesign results and computational benchmarks elsewhere in those sources are outside this case's three-path minibinder count analysis.

## Inputs and the evidence trail

| Material | What it provides | Boundary to preserve |
|---|---|---|
| `source_brief.md` | Operator-prepared source map | A guide to sources, not raw laboratory data or a substitute for checking the paper |
| `published_aggregate_counts.csv` | Ten rows transcribed from the article | Original counts and explicit denominators; missing denominators remain missing in the upload-only calculation |
| `metric_definitions.json` | Definitions for the analysis | Keeps reported percentages separate from locally calculated values |
| `analysis_notes.md` | Scope and calculation instructions | Defines a source-based reanalysis rather than a model or wet-lab rerun |
| Saved preprint and source checks | Target-level denominators, assay descriptions and selection details | Additions are identified by source page; they are not reverse-engineered from an aggregate percentage |
| Derived CSVs and calculation audits | Exact fractions and rounded percentages | Arithmetic on author-reported observations, not newly measured outcomes |

The final source review supersedes an earlier incomplete PDF download. That matters because the article alone does not provide every target denominator. The retained final analysis supplements the original upload with directly transcribed values from the preprint's pages 16 and 22. It keeps those additions identifiable instead of silently presenting them as fields originally supplied in the CSV.

## Three workflows, three attribution questions

| Path | Starting point | GPT-6.2 contribution | Other steps before the reported screen |
|---|---|---|---|
| 1: structure generation | Researcher-supplied target structures and marked attachment sites | Code that produces 3D minibinder designs | SolubleMPNN supplies sequences; specialist models score/select candidates; constructs are made, expressed and tested |
| 2: sequence redesign on existing binders | Predicted complexes based on previously confirmed minibinders | New sequences, with parental sequences withheld | Starting binders and predicted structures come from earlier work; specialist filtering and laboratory testing remain separate contributions |
| 3: new sequences for GPT-generated structures | Three earlier GPT-generated shapes already supported by binding-positive ProteinMPNN sequences | New sequences for those shapes | Prior ProteinMPNN positives establish starting context; new candidates undergo filtering and physical screening |

Path 3 contains two PD-L1 shapes and one IL-7Rα shape. The previous ProteinMPNN-supported positives are not additional successes to add to the new 14/107 result. The final evidence review does not establish complete per-structure counts beyond the reported target-level breakdown.

The paper describes ESMFold2, Boltz-2 and OpenDDE as downstream complex evaluators. Eligibility and ranking criteria precede the selected laboratory screens. Researchers specify targets and sites, prepare inputs and organize the experiments; Onava's workflow and DNA synthesis are additional contributions. These steps should remain visible when attributing the final outcome to the model.

## Recorded binding counts and calculated percentages

Every numerator and denominator below is **author-reported**. The percentage is calculated here as `100 × positive / tested`, rounded half-up to two decimal places. It describes selected candidates with a reported screening result, not all generated, ordered or expressed designs.

| Path / target | Binding-positive | Tested | Calculated percentage |
|---|---:|---:|---:|
| 1 / five-target aggregate | 35 | 322 | 10.87% |
| 1 / PD-L1 | 5 | 92 | 5.43% |
| 1 / IL-7Rα | 3 | 93 | 3.23% |
| 1 / TrkA | 1 | 46 | 2.17% |
| 1 / VEGF-A | 8 | 46 | 17.39% |
| 1 / IL-17A | 18 | 45 | 40.00% |
| 2 / MDM2 | 75 | 88 | 85.23% |
| 2 / VEGF-A | 26 | 42 | 61.90% |
| 2 / PD-1 | 8 | 59 | 13.56% |
| 3 / three-structure aggregate | 14 | 107 | 13.08% |
| 3 / PD-L1 | 9 | 89 | 10.11% |
| 3 / IL-7Rα | 5 | 18 | 27.78% |

The aggregate rows overlap their constituent target rows. For path 1, the target counts sum to 35 positives and 322 tested; path 3 sums to 14 and 107. These reconciliation checks do not create additional observations. The analysis does not add aggregate and target rows together or pool different workflows into one headline rate.

The article prints some results at a different precision: 35/322 appears as 10.9%, while path 2's MDM2, VEGF-A and PD-1 results appear as 85%, 62% and 14%. The calculated values above are compatible with those displays. A difference caused by rounding is not a disagreement in the underlying count.

### Why the figure uses separate panels

The saved final figure presents the three paths separately and displays each numerator and denominator. It preserves workflow and target order rather than ranking the percentages as a matched performance competition. Different starting structures, target sets and selection processes make a single cross-workflow winner interpretation inappropriate.

The initial upload-only view and final supplemented view have different evidence scopes. The former retains five unavailable denominators and cannot show all target-level rates; the latter includes the verified preprint additions. Earlier figures remain historical artifacts, not contradictory measurements from another experiment.

## What did the laboratory tests measure?

The retained source review identifies biolayer interferometry (BLI), with single-dose screening and separate dose-response measurements for selected hits. Source methods describe apparent affinity fitting and controls; they do not establish that every binding-positive candidate underwent a full titration.

| Evidence or measurement | What it supports in this case | What it does not establish |
|---|---|---|
| A reported positive BLI screen | A candidate was called binding-positive under the campaign's conditions | A universally defined hit threshold or success across every assay |
| Specialist eligibility/ranking | Computational selection occurred before laboratory testing | An unfiltered generation-to-hit probability |
| Selected dose-response affinity measurements | Additional characterization of selected hits | Full affinity characterization of every screened positive |
| Binding to a target | Evidence of attachment in the reported assay | Cellular mechanism, therapeutic action, safety or clinical efficacy |
| Partner-lab involvement | Physical work within the reported collaboration | Independent replication by a separate team |

The complete operational hit-calling classifier remains unresolved in the inspected methods. A 0.4 nm exclusion described for a selected matched-affinity analysis must not be repurposed as a universal positivity threshold for all screens. Similarly, computational screening criteria and laboratory hit definitions answer different questions.

## From a headline claim to a supported conclusion

| Possible reading | Evidence-supported interpretation |
|---|---|
| “Intrinsic” means the whole pipeline was unassisted | The sources attribute generation capabilities to GPT while explicitly describing specialist sequence generation, prediction or filtering elsewhere in the workflow. |
| The largest percentage proves one design path is best | Rates come from different targets, starting points and selection conditions; this is not a matched laboratory comparison. |
| Onava testing is independent replication | Onava is a research partner in the reported work; collaboration and independent confirmation are distinct. |
| Binding-positive designs are effective medicines | Binding is one step; the case supplies no new evidence of biological activity, specificity, developability, safety or clinical benefit. |

The useful finding is that model contribution, specialist assistance and physical screening can all be true simultaneously. Describing those stages separately preserves the evidence for GPT-6.2's contributions without assigning the complete experimental outcome to it alone.

## Reproducibility and verification scope

The archive retains the four original uploads, source-cell checks, workflow maps, claim-to-evidence documents, final report, editable plotting code, result CSVs, figures and two compact reproducibility ZIPs. The complete preprint is preserved separately in the native package.

The recorded fresh-process audit ran the saved code twice in newly empty output directories: once with the final preprint-supplemented counts and once in article-only numeric mode. Numerical CSVs and build manifests matched their retained outputs. The audit reports matching PDF text and rendered pixels, while raw PDF bytes differed because of the CreationDate field; normalizing that field produced a byte match. It did not compare prior PNGs.

Editorial reports and claim-to-evidence judgments were preserved and checked, not computationally regenerated from aggregate counts. Article-only mode changes numeric inputs; its assay caption still draws on the completed source review. Neither rebuild reproduces the original model generation or laboratory experiments.

Publication preparation checked the twelve exact count fractions, rounding, aggregate reconciliation, package inventory and evidence references, and consistency of the final bundled artifacts. It did not rerun the archived analysis script or independently reanalyze sample-level assays. No confidence intervals, significance tests or cross-workflow causal estimates are supplied by this case.

## Sources and research materials

- [OpenAI article: GPT-6 models demonstrate intrinsic protein-design capabilities](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/) — laboratory experiments and the authors' qualifications on assistance and interpretation.
- [Preprint, page 16](https://cdn.openai.com/pdf/gpt-6-a-universal-foundation-model-for-protein-biology.pdf#page=16) — path 1 target denominators and reported results.
- [Preprint, page 22](https://cdn.openai.com/pdf/gpt-6-a-universal-foundation-model-for-protein-biology.pdf#page=22) — inverse-folding paths and target-specific counts.
- [Preprint, page 49](https://cdn.openai.com/pdf/gpt-6-a-universal-foundation-model-for-protein-biology.pdf#page=49) — candidate evaluation, eligibility and ranking.
- [Preprint, Appendix B beginning on page 61](https://cdn.openai.com/pdf/gpt-6-a-universal-foundation-model-for-protein-biology.pdf#page=61) — laboratory methods and measurement context.

The public introduction summarizes a source-based analysis in AIPOCH Open-Science. The native export is preserved byte-for-byte with a whitespace-free external filename. The generated poster is illustrative artwork, not a measured protein structure or laboratory photograph from the study.
