# Lyra 2.0: Better Pictures, but Do They Still Match?

## The question

A generated walkthrough can look attractive while its views drift apart. Does a higher perceptual-quality score also mean better style consistency, camera control and geometric agreement? This case examines that question using a fixed published ablation table rather than generating new scenes.

The session reanalyzes **five configuration aggregates across seven metrics** from Table 3 of arXiv:2604.13036v1. Removing self-augmentation raises reported Subjective Quality by **4.53 score units**, while Style Consistency falls by **7.09** and Camera Controllability falls by **9.95**. Yet Reprojection Error improves by **0.003**. The evidence supports a qualified tradeoff across these configurations, not a claim that every consistency measure gets worse or that attractive images prove faithful geometry.

No Lyra training, inference, new video generation or independent metric measurement is performed in this case. It audits published aggregates, calculations and source interpretations.

## Start with the table's actual scope

The supplied five inputs comprise analysis notes, a source brief, the unchanged 25-page paper, a CSV transcription and metric definitions. The table's 35 numeric cells were checked against the fixed-version PDF, retaining printed decimal precision and the original directions for better performance.

| Source element | What it supplies | Scope to preserve |
|---|---|---|
| Table 3, paper p. 13 | Five configurations × seven metrics | Configuration aggregates, not five scenes or repeated experiments |
| Section 5.4, pp. 12–13 | Ablation descriptions and author interpretations | Explanations are attributed to the paper, not locally tested mechanisms |
| Sections 5.1–5.2, pp. 9–10 | DL3DV training context and Tanks and Temples evaluation | The examined table is described as out-of-domain evaluation |
| Figure 6, p. 14 | Three selected qualitative example rows | Static author-provided examples, not newly rendered walkthroughs |
| Supplied CSV and definitions | Machine-readable values and metric directions | A transcription and review layer checked against the source |

The paper cover says April 15, 2026; its arXiv v1 stamp says April 14. November 9 is the preparation date of this case's records, not the model's release date. The supplied PDF's bytes match its declared hash.

## Give each metric its own meaning

| Metric | Preferred direction | What the paper-based review uses it to describe | What it does not establish |
|---|---|---|---|
| SSIM | Higher | Structural similarity to reference frames | Percentage of rooms reconstructed correctly |
| LPIPS | Lower | Perceptual image distance | An interchangeable unit with FID or WorldScore scores |
| FID | Lower | Distribution-level visual distance | Per-scene geometric correctness |
| Subjective Quality | Higher | WorldScore perceptual-quality metric | A local human preference study or a percentage of beautiful images |
| Style Consistency | Higher | Visual drift between first and last frames | Certified geometric consistency |
| Camera Controllability | Higher | Camera-pose accuracy metric | Percentage of rooms or entire trajectories reconstructed correctly |
| Reprojection Error | Lower | A 3D-consistency proxy using SLAM-estimated per-frame depth | A complete geometry validation or substitute for style/camera scores |

Section 5.2 names standard SSIM, LPIPS and FID protocols and the WorldScore metrics. Exact implementations and aggregation cannot be reconstructed from the five reported rows. The metrics have different units and meanings, so the analysis does not average them into an overall score or treat their raw magnitudes as comparable.

## Read the complete published comparison

| Configuration | SSIM ↑ | LPIPS ↓ | FID ↓ | Quality ↑ | Style ↑ | Camera ↑ | Reprojection ↓ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Full model, Ours | 0.384 | 0.552 | 51.33 | 43.35 | 85.07 | 63.87 | 0.069 |
| With Global Point Cloud | 0.368 | 0.562 | 52.54 | 44.58 | 82.42 | 49.86 | 0.067 |
| With Explicit Correspondence Fusion | 0.370 | 0.554 | 49.13 | 45.71 | 83.28 | 57.29 | 0.071 |
| Without FramePack | 0.362 | 0.549 | 50.98 | 45.27 | 80.61 | 62.62 | 0.079 |
| Without Self-Augmentation | 0.363 | 0.568 | 55.15 | 47.88 | 77.98 | 53.92 | 0.066 |

The full model has the highest displayed SSIM, style and camera scores, but is not best on every metric. Without self-augmentation has the highest Subjective Quality and lowest Reprojection Error. Without FramePack has the lowest LPIPS; Explicit Correspondence Fusion has the lowest FID. These observations already rule out a simple universal-winner reading of the table.

The actual-value figure uses independent axes for the seven metrics. A second figure shows signed variant-minus-full differences in original units. Color identifies better, tied or worse according to direction; it does not encode statistical significance or a shared effect-size scale.

## Keep every self-augmentation difference, including the exception

Differences use the printed numeric strings with decimal arithmetic. Here, a positive difference favors the variant only for a higher-is-better metric; a negative difference favors it only for a lower-is-better metric.

| Metric | Without self-augmentation − full | Direction for the variant |
|---|---:|---|
| SSIM | −0.021 | Worse |
| LPIPS | +0.016 | Worse |
| FID | +3.82 | Worse |
| Subjective Quality | **+4.53** | Better |
| Style Consistency | **−7.09** | Worse |
| Camera Controllability | **−9.95** | Worse |
| Reprojection Error | **−0.003** | Better |

Section 5.4 attributes the style/camera decline without self-augmentation to brittle inference under imperfect history conditioning. That explanation does not remove the favorable reprojection change: the paper section does not explain that exception, and this case lacks per-scene depth estimates, trajectories and metric internals to resolve it.

Thus “higher perceptual quality does not guarantee better consistency” is supported within these reported configurations. “Removing self-augmentation worsens every geometry metric” is contradicted by the displayed reprojection result. Neither statement establishes a repeatable causal effect across scenes or runs.

## Ask whether the metric set changes the ranking

Instead of assigning weights, the analysis uses a precise dominance rule: one configuration must be no worse on every included metric and strictly better on at least one. It evaluates all 25 ordered pairs in each metric set, including five self-comparisons that are false by definition. There are 20 non-self comparisons per set.

| Declared metric set | Dominance relations | Meaning |
|---|---:|---|
| Quality, Style Consistency and Camera Controllability | **1 of 25 ordered pairs** | Explicit Correspondence Fusion dominates Global Point Cloud |
| All seven metrics | **0 of 25 ordered pairs** | The initial relation no longer meets the rule |
| Pairwise relation changes | **1 of 25** | The other 24 ordered-pair decisions are unchanged |

The changed pair illustrates why broader evidence can weaken a confident-looking comparison:

| Metric | Explicit Correspondence Fusion | Global Point Cloud | Favorable to Explicit Fusion? |
|---|---:|---:|---|
| Subjective Quality | 45.71 | 44.58 | Yes |
| Style Consistency | 83.28 | 82.42 | Yes |
| Camera Controllability | 57.29 | 49.86 | Yes |
| SSIM, added | 0.370 | 0.368 | Yes |
| LPIPS, added | 0.554 | 0.562 | Yes |
| FID, added | 49.13 | 52.54 | Yes |
| Reprojection Error, added | **0.071** | **0.067** | **No: lower is preferred** |

The favorable added SSIM, LPIPS and FID evidence remains visible. Reprojection is the blocking witness that removes the dominance relation. Zero relations under seven metrics means this particular no-worse-on-all rule finds none; it does not mean the methods are equal or that their differences are insignificant. No tolerance, pooled score or inferential test is used.

## Separate source explanations by stage

| Stage in the paper | Archived interpretation | Boundary |
|---|---|---|
| Training self-augmentation, Section 4.3 | Corrupt history latents probabilistically and perform one-step denoising, while retaining clean target latents | Training-time technique, not inference-time retraining or a locally rerun test |
| Generation-time geometry and retrieval, Section 4.2 | Keep per-frame geometry and choose history frames for target-view coverage | Source interpretation; no local retrieval traces or controlled intervention |
| Correspondence and appearance conditioning | Canonical-coordinate correspondence routing and learned aggregation differ from retrieved RGB and FramePack conditioning | These signals should not be collapsed into one undifferentiated geometry mechanism |
| Final reconstruction | Downstream of generated views | Attractive frames alone do not validate the reconstructed geometry |

The global-point-cloud ablation changes both cache representation and conditioning. Its row cannot isolate a single additive component benefit. The conceptual diagram is a source-attributed explanation rendered from frozen review decisions, not experimental evidence that the proposed mechanism has been independently demonstrated.

## What the six figures add

The six saved views cover actual values, raw differences, the focused self-augmentation tradeoff, metric-set relation matrices, a conceptual mechanism and evidence limits. They use the same aggregate table and source review; they are not six independent validations.

No per-scene raw videos or metric outputs, repeated runs, seeds, variances or sufficiently unrounded scores are supplied. Confidence intervals, p-values, bootstrapped scene distributions and population correlations cannot be recovered from five configuration aggregates. Printed rounding determines table-level ties and limits fine distinctions. Static selected examples do not fill those gaps.

## Saved materials and verification scope

The native session preserves the five original inputs, conversation and execution evidence, source-cell checks, calculation and interpretation audits, tables and six figures. The final `lyra_verified_package.zip` includes the latest report, exact input bytes, `rebuild.py`, frozen source judgments and diagram decisions, numerical outputs and historical audit snapshots.

The archived fresh-process verification reports successful execution of the unchanged rebuild script with an initially empty working directory and output directory, without copying old figures. All six new PNGs decode and match saved figures byte-for-byte; their maximum side is 2340 pixels. All 13 CSV tables match both bytes and parsed strings, retaining decimal precision. The five original inputs match their preserved bytes, and the latest report's 41 local links resolve.

**The report itself has an explicit reproducibility limit:** script-generated Markdown does not reproduce the delivered report's manually added Methods section and post-run audit/verification links byte-for-byte. The final report preserves and discloses those editorial additions. Historical arithmetic, pairwise and interpretation audits were copied into the package for completeness; they were not regenerated by the fresh numerical build or used to produce its figures.

Semantic judgments and conceptual-diagram decisions are declared frozen inputs, not recreated by numerical rebuilding. This publication does not execute the archived research script or rerun Lyra. Extract the complete inner ZIP to preserve its report's local resources. This introduction uses ordinary Markdown tables and text, without a TeX-rendering dependency.

## Sources and provenance

The fixed primary source is [Lyra 2.0, arXiv:2604.13036v1](https://arxiv.org/abs/2604.13036v1). The relevant locations are [Table 3 and Section 5.4, p. 13](https://arxiv.org/pdf/2604.13036v1#page=13), [metric definitions in Section 5.2, p. 10](https://arxiv.org/pdf/2604.13036v1#page=10), [self-augmentation in Section 4.3, pp. 7–8](https://arxiv.org/pdf/2604.13036v1#page=7), and [qualitative Figure 6, p. 14](https://arxiv.org/pdf/2604.13036v1#page=14). The paper's experiments and interpretations remain attributed to its authors; this case performs a public-record reanalysis.

This document summarizes the supplied AIPOCH Open-Science session. The original native package remains byte-for-byte intact; only the external publication filename replaces spaces with hyphens. The generated photographic-sticker cover illustrates the question and does not depict measured Lyra outputs. Package integrity and a native import test establish transfer and compatibility, not model performance or scientific validity.
