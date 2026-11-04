# Weight-Space Programming: Did Every Math Problem Improve?

## The question

A model's average math score can rise sharply while some problems remain unsolved. This case asks whether an apparent gain from weight-space programming extends to every shared problem, and what the saved records can actually tell us about the change.

The session reanalyzes supplied public score records for a baseline and a weight-edited model. It performs no new model inference or local regrading. On the **25 problems with records in both versions, 18 improve and seven tie at zero correct recorded samples; none decline**. Mean recorded correctness rises from 5% to 47%, but that does not mean every problem improves or that the same gain holds across the full benchmark.

## First make the populations comparable

The baseline file contains 25 problems with four recorded correctness flags each. The edited file contains 500 problems with four flags each. Comparing the baseline's small subset directly with the edited full-file average would mix populations. The workflow checks ID uniqueness and binary integer flags, matches exact IDs, and retains all unmatched records in an inclusion table.

| Population | Problems | Recorded samples | Use in this analysis |
|---|---:|---:|---|
| Baseline file | 25 | 100 | All IDs find edited counterparts |
| Edited file | 500 | 2,000 | Full-file summary is background, not the paired comparison |
| Common subset, per version | 25 | 100 | Same IDs and denominators for the principal result |
| Edited-only exclusions | 475 | 1,900 | Retained with missing baseline values; no invented before/after change |

A problem is the paired unit. The four samples within a problem are repeated observations. A shared seed does not prove that baseline and edited answers are matched generation trajectories, so the analysis pairs problem-level counts rather than individual sampled answers.

## Define what is counted

For each common problem, the correct count is the sum of its four supplied binary grader flags, giving an integer from zero to four. The change is edited count minus baseline count, from −4 to +4. Mean recorded correctness divides all correct flags by 25 × 4.

```text
Correct count for a problem = sum of its four saved correctness flags
Problem-level change       = edited count − baseline count
Matched mean correctness   = total correct flags / 100
```

| Recorded evaluation setting | Value in both versions |
|---|---|
| Temperature / top_p / top_k | 0.6 / 0.95 / 20 |
| Presence penalty | 1.5 |
| Maximum tokens | 32,768 |
| Seed | 0 |
| Thinking | Enabled |

Those equal settings establish a recorded configuration, not independent sample alignment or a complete causal design. No confidence interval, significance test, population extrapolation or independent verification of mathematical correctness is added here.

## The average improves, but it answers a limited question

| Result | Baseline | Edited | Interpretation |
|---|---:|---:|---|
| Correct flags on the same 25 problems | 5/100 | 47/100 | **+42 percentage points** in the matched subset |
| Problems with at least one correct flag | 3/25 | 18/25 | Broader observed coverage, not universal improvement |
| Full edited-file summary | Not comparable | 51% across 500 problems | Different population from the 47% matched result |

The source brief also cites an original-blog score of 48.1%. That reported result, the rerun's full-file 51.0% and this common-subset 47% are three distinct quantities. They should not be substituted for one another.

The 25 shared problems come from a publisher smoke-test subset. The calculations describe those saved records; they do not establish a representative benchmark-wide gain or quantify general side effects of editing weights.

## Look at the changes problem by problem

The paired-count figure retains all 25 IDs, including coincident zero-to-zero points. The distribution then makes the different gain sizes explicit.

| Change in correct count, out of four | Problems | Share of common problems |
|---|---:|---:|
| Any decline, −4 through −1 | 0 | 0% |
| No change, 0 | 7 | 28% |
| +1 | 7 | 28% |
| +2 | 3 | 12% |
| +3 | 3 | 12% |
| +4 | 5 | 20% |
| **Total** | **25** | **100%** |

The 18 improving problems account for all 42 additional correct flags: 7 × 1 + 3 × 2 + 3 × 3 + 5 × 4 = 42. All seven ties have four zero flags in both versions. There are no nonzero ties in this subset.

Zero observed declines means no problem-level count falls among these 25 IDs. It does not establish that the edit has no adverse effects on the other 475 problems, for which baseline comparisons are absent. A zero flag also does not reveal why the grader marked an output unsuccessful.

## Check the transition structure

The transition matrix cross-tabulates baseline correct count against edited correct count, assigning each problem to one cell. Its marginal counts show the starting and ending distributions without turning totals into extra observations.

| Correct samples per problem | Baseline problems | Edited problems |
|---|---:|---:|
| 0 | 22 | 7 |
| 1 | 2 | 6 |
| 2 | 0 | 3 |
| 3 | 1 | 1 |
| 4 | 0 | 8 |
| **Total** | **25** | **25** |

Most baseline problems have no correct recorded sample. After editing, eight have four correct flags and seven still have none. These margins complement the paired change table: they describe each version's distribution, while the transition cells preserve which IDs moved between counts.

## Ask how much recorded coverage is required

| Required correct samples per problem | Baseline | Edited |
|---|---:|---:|
| At least one | 3/25 (12%) | 18/25 (72%) |
| At least two | 1/25 (4%) | 12/25 (48%) |
| At least three | 1/25 (4%) | 9/25 (36%) |
| All four | 0/25 (0%) | 8/25 (32%) |

These thresholds are nested: a problem meeting the four-correct threshold also meets the other three. Adding the counts across thresholds recovers five baseline and 47 edited correct flags, which checks the earlier averages. The percentages are observed coverage in these saved samples, **not pass-at-k estimates, confidence levels or future-success probabilities**.

## Read a few responses without inventing a mechanism

The attachment supplies six complete response text fields across three problem IDs. The review selects a largest-gain category, a smallest-positive-gain category and a zero-in-both category. Where preferred response texts were reportedly absent, it discloses a fallback to the lexicographically first same-category ID with text in both versions.

| Review category | Preferred ID | Inspected ID | Selection boundary |
|---|---|---|---|
| Largest gain | `test/algebra/2193.json` | `test/geometry/248.json` | Preferred text reportedly absent in both exports |
| Smallest positive gain | `test/algebra/1837.json` | `test/algebra/2036.json` | Same disclosed fallback rule |
| Zero correct in both | `test/algebra/1349.json` | Same ID | Preferred text available |

The baseline geometry passages repeat radius-label and coordinate statements, while the edited ending presents the supplied reference value. In the distance example, both endings present the reference expression even though a baseline passage contains a false divisibility claim about 117. In the zero-in-both example, baseline text repeats coordinate lists and edited text assumes a path interpretation.

These are bounded observations, with possible explanations stored separately from the evidence. The review is neither blind nor preregistered. It does not show that repetition caused failure or that the weight edit repaired a specific reasoning mechanism. The numerical script validates frozen excerpts and their offsets, rather than regenerating the qualitative judgments.

## Keep unresolved evidence gaps visible

| Missing or limited evidence | Consequence |
|---|---|
| Baseline records for 475 edited problems | No paired change or side-effect estimate for those IDs |
| Original response exports | Metadata reports 20 unique records per export, but those exports were not independently reloaded |
| More than six attached response texts | Three reviewed IDs cannot characterize all 25 paired problems |
| Sample index and exact exporter linkage | Saved text is not hard-linked to a particular `correct[0]` flag |
| Stop reasons and generated-token counts | Endings, repetition and character counts cannot establish token-cap hits |
| Rendered diagrams for two Asymptote question strings | Text inspection lacks those rendered visual inputs |
| Original solution text and independent regrading | Supplied reference expressions and flags remain source material |

Five common IDs reportedly lack text in both original exports. Their absence remains a recorded gap, not an opportunity to infer a response. Full-file timing, cutoff, token and throughput summaries concern different populations, so they cannot quantify efficiency changes for the matched subset. Correctness and token-cap hits are also not mutually exclusive categories.

## Saved materials and verification scope

The native session preserves five original inputs, conversation and execution evidence, the inclusion and paired-count tables, distributions, transition cells, coverage thresholds, response review and six figures. Its final `verified_delivery.zip` contains the corrected report, exact original inputs, 11 CSV tables, frozen review decisions, `rebuild_analysis.py` and audit records.

The archived audit reports 37 passing consistency checks against supplied arrays and tables. The final fresh-process verification supersedes an earlier report's subprocess limitation: a separate Python process read all five exact inputs, ran the unchanged rebuild script into an initially empty folder and exited successfully. All 11 CSV tables matched, all six PNGs were byte-identical to the compared saved versions, and their longest sides were at most 2160 pixels. Report-local links resolved inside the extracted delivery.

Those checks establish numerical and delivery consistency, not independent correctness labels or a causal explanation. This introduction was prepared without rerunning the model or executing the archived research script. Extract the complete inner ZIP to use its report's local resources. This published document uses ordinary Markdown tables and text equations, with no TeX-rendering dependency.

## Sources and provenance

The supplied brief attributes weight editing to the [authors' Weight-Space Programming report](https://rikiyat.github.io/blog/weight-space-programming/): GPT-6 Astra editing Qwen3.5-0.8B using practice examples and bounded forward feedback, without gradient training or optimizer fitting. That description is attributed background, not an experiment performed in this case. Absence of gradient training does not mean absence of data or feedback, and the proposed reasoning-failure mechanism remains an interpretation.

Score provenance points to [RikiyaT/Qwen3.5-0.8B-weight-space-programming at revision d1671a178705bcab7644806d23c535517f35723b](https://huggingface.co/RikiyaT/Qwen3.5-0.8B-weight-space-programming/tree/d1671a178705bcab7644806d23c535517f35723b). The brief attributes that rerun to akhaliq using Hugging Face Jobs and ML Intern. Question/reference provenance is [HuggingFaceH4/MATH-500 at revision 6e4ed1a2a79af7d8630a6b768ec859cb5af4d3be](https://huggingface.co/datasets/HuggingFaceH4/MATH-500/tree/6e4ed1a2a79af7d8630a6b768ec859cb5af4d3be), matched by `unique_id`. External sources were not freshly fetched in the saved analysis; third-party materials retain their original attribution.

This document summarizes the supplied AIPOCH Open-Science session. The original native package remains byte-for-byte intact; publication normalizes only its external filename to hyphens. The generated photographic-sticker cover is illustrative. Transfer integrity and an actual native import test establish package compatibility, not model quality or the scientific validity of every saved judgment.
