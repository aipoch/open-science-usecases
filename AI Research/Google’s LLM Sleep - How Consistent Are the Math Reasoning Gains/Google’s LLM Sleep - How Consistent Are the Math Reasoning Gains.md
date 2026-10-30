# Google’s LLM Sleep: How Consistent Are the Math Reasoning Gains?

## The question

Does a method improve mathematical reasoning consistently across model sizes, tasks, baselines, and component choices—or does a broad headline hide uneven comparisons? This case audits the reported mathematical-reasoning results in *Language Models Need Sleep: Learning to Self-Modify and Consolidate Memories*, focusing on Tables 1 and 2 of arXiv version 2.

**Sleep has the highest displayed score in each of six model–task settings in Table 2.** All 24 Sleep-minus-baseline differences are positive, but their sizes vary substantially. Component benefits are less uniform: removing semantic reward raises the reported Qwen3-8B AIME-25 score from 69.0 to 69.2. Neither observation establishes repeated-run reliability or superiority at equal computational cost.

This is an audit of published scores and the archived analysis, not a new training replication. All differences below are absolute reported **score points**, not relative percentage increases.

## What is inside the comparison

| Source | Models | Configurations | Tasks | Recorded scores |
|---|---|---|---|---:|
| Table 1, p. 11 | Qwen3-8B | Sleep, three component-removal variants, OPSD, OPSD + Expansion | AIME-24, AIME-25, HMMT-25 | 18 |
| Table 2, p. 12 | Qwen3-1.7B and Qwen3-8B | Base (Instruct), SFT, GRPO, OPSD, Sleep | The same three tasks | 30 |

Six Qwen3-8B Sleep/OPSD scores recur across the tables. They are separately sourced records, not independent experiments. The Table 1 “+ Expansion” row belongs to OPSD and must not be misread as another consecutive Sleep stage.

The paper describes memory consolidation and a separate Dreaming phase. The mathematical experiments examined here evaluate **consolidation without Dreaming**. Knowledge seeding transfers knowledge from a smaller-state teacher to an expanded student using parameter learning; it should not be described as ordinary prompting or evidence that biological sleep has been reproduced.

## Metric and budget: what can actually be matched

Both tables label the metric **average@16**. The archived source review did not find a complete operational definition. A conventional interpretation involving multiple sampled responses is not a substitute for the paper's evaluation protocol; this metric must not be equated with pass@16, majority voting, or 16 independent training runs.

| Appendix B.4 parameter | GRPO | SFT | Sleep |
|---|---:|---:|---:|
| Learning rate | 5 × 10⁻⁶ | 5 × 10⁻⁶ | 5 × 10⁻⁶ |
| Effective batch size | 32 | 32 | 32 |
| Training steps | **500** | **100** | **100** |
| LoRA rank | 64 | 64 | 64 |
| LoRA alpha | 128 | 128 | 128 |

The comparison is not uniformly equal-step: GRPO has five times the listed steps. Matching some hyperparameters or active parameter counts would not establish equal compute. OPSD and individual ablation schedules are absent from this table. Separate author-reported efficiency claims do not prove that the displayed benchmark comparisons use equal budgets.

Prompts, decoding settings, grading, seeds, treatment of truncated outputs, and repeated-run uncertainty are not sufficiently specified in the archived review to reconstruct a complete evaluation. The appendix's reference to 8B or 3B models also leaves its exact applicability to the 1.7B configuration unclear.

## Reported scores versus Base

| Task | Qwen3-1.7B: Base → Sleep | Gain | Qwen3-8B: Base → Sleep | Gain |
|---|---|---:|---|---:|
| AIME-24 | 49.8 → 53.2 | +3.4 | 73.8 → 79.2 | +5.4 |
| AIME-25 | 34.5 → 40.2 | +5.7 | 68.1 → 69.0 | +0.9 |
| HMMT-25 | 25.7 → 29.3 | +3.6 | 42.4 → 46.1 | +3.7 |

The larger model has higher absolute scores on all three tasks. It does not have a larger improvement on all three: its AIME-25 gain is smaller. With only two sizes in one model family, these points cannot identify a scaling law or a causal effect of parameter count.

## All Table 2 baseline contrasts

Each entry below is calculated as `Sleep score − baseline score` from the archived comparison records.

| Model | Baseline subtracted | AIME-24 | AIME-25 | HMMT-25 |
|---|---|---:|---:|---:|
| Qwen3-1.7B | Base (Instruct) | +3.4 | +5.7 | +3.6 |
| Qwen3-1.7B | SFT | +5.9 | +4.1 | +6.4 |
| Qwen3-1.7B | GRPO | +2.2 | +1.6 | +3.2 |
| Qwen3-1.7B | OPSD | +1.6 | +0.2 | +1.2 |
| Qwen3-8B | Base (Instruct) | +5.4 | +0.9 | +3.7 |
| Qwen3-8B | SFT | +3.7 | +2.6 | +2.4 |
| Qwen3-8B | GRPO | +2.8 | +0.9 | +1.2 |
| Qwen3-8B | OPSD | +2.6 | +1.6 | +1.0 |

All 24 contrasts are positive, ranging from +0.2 to +6.4. Their direction is consistent within this evaluation, while their magnitude depends on the comparator. On 1.7B HMMT-25, for example, the advantage is +6.4 over SFT and +1.2 over OPSD. On 1.7B AIME-25, 40.2 versus 40.0 is a numerical lead of just +0.2.

These contrasts reuse Sleep scores within settings. Treating them as 24 independent replications would overstate the evidence. Confidence intervals and repeated-run results are not supplied, so the smallest positive differences cannot be called statistically reliable improvements.

## Components: preserve the negative exception

The signed ablation contrast is `full Sleep − component-removal variant` on Qwen3-8B.

| Component removed | AIME-24 | AIME-25 | HMMT-25 |
|---|---:|---:|---:|
| Imitation learning | +2.4 | +1.1 | +1.1 |
| Semantic reward | +0.3 | **−0.2** | +1.6 |
| Expansion | +1.0 | +1.1 | +1.2 |

Eight contrasts favor full Sleep; one does not. The retained calculation is **69.0 − 69.2 = −0.2** on AIME-25 without semantic reward. It contradicts the claim that every component improves every task, but it does not establish reproducible harm from semantic reward.

The semantic reward measures agreement in meaning between student and teacher continuations, not independent mathematical correctness. It is nested within imitation learning, so these component contrasts are conditional and cannot automatically be added as independent contributions. Paired question-level results could support evaluation uncertainty estimates; repeated training runs are additionally needed to characterize training variability.

## Expansion in two different contexts

| Task | OPSD → OPSD + Expansion | Sleep without expansion → full Sleep |
|---|---|---|
| AIME-24 | 76.6 → 77.9: **+1.3** | 78.2 → 79.2: **+1.0** |
| AIME-25 | 67.4 → 68.2: **+0.8** | 67.9 → 69.0: **+1.1** |
| HMMT-25 | 45.1 → 45.9: **+0.8** | 44.9 → 46.1: **+1.2** |

Expansion is positive in all six reported contrasts. These are comparisons under different surrounding configurations, not successive stages. Adding +1.3 and +1.0 on AIME-24 would therefore not explain Sleep's +2.6 over OPSD. A connected numerical partition, OPSD → OPSD + Expansion → Sleep, gives +1.3 +1.3 = +2.6, but the residual is not an isolated causal contribution of imitation learning.

## What the evidence supports

| Claim | Reading supported by the case |
|---|---|
| Consistency | Higher reported Sleep scores in the six Table 2 settings examined |
| Uniformly large gains | Unsupported; contrasts range from +0.2 to +6.4 and depend on the baseline. |
| Every component helps | Unsupported; the semantic-reward AIME-25 exception remains. |
| Equal-compute superiority | Unestablished; schedules differ and detailed cost accounting is missing. |
| Repeated-run reliability | Unestablished; shared scores and absent run-level uncertainty limit the inference. |
| Dreaming or long-term retention gains | Not isolated by these mathematical tables |

## Archived materials and version limits

The native session contains the source PDF and table images, the saved `sleep_reasoning_report.md`, a master results CSV, plotting and analysis scripts, score-comparison CSVs, and explanatory figures covering baseline differences, ablations, expansion, and claim-to-evidence relationships.

The conversation continues beyond the last saved report. A later recorded check states that 24 baseline, nine ablation, and six expansion contrasts match their source records, and retains the negative ablation exception. It also records that saving a revised report and unified script was rejected by the application's disk-reserve limit. **The last saved report therefore remains an earlier artifact**, with some earlier input-access limitations still in its text. This publication preserves both the artifact and that later conversation rather than pretending an unsaved revision is a delivered file. The tables in this introduction were checked directly against the CSVs present in the supplied package; the model training and research scripts were not rerun for publication.

The source is Behrouz and colleagues, [*Language Models Need Sleep: Learning to Self-Modify and Consolidate Memories*, arXiv:2606.03979v2](https://arxiv.org/abs/2606.03979v2). The case is tied to that paper version rather than an unspecified latest revision.

This introduction was prepared from the supplied AIPOCH Open-Science session and its retained artifacts. Publication preserves the original native package bytes and changes only its external filename to replace spaces with hyphens. It adds no missing training runs, regenerated research files, or unrecorded measurements.
