# MiMo-V2.6 Pro vs. Flash - Is More RL Spending Worth It

## Research question

What can public cost and benchmark disclosures establish about additional reinforcement-learning spending?

Compares archived vendor reports of reinforcement-learning spending and shared benchmark results for MiMo Pro and Flash. The session records source provenance and separates reported costs from reproducible ratio calculations.

## Data and comparison design

Compute ratios from the recorded vendor cost figures, distinguish nominal rollout slots from actual generated tokens, and compare shared benchmark rows. Preserve the fact that the two backbones differ.

## Recorded findings

| Reported quantity | Pro | Flash | Comparison |
| --- | --- | --- | --- |
| RL-phase spending | $2.62 million | $0.85 million | 3.08× Pro/Flash |
| Nominal rollout slots | Reported nominal allocation | Reported nominal allocation | 1.00× ratio |
| Final training-token totals | Matched totals unavailable | Matched totals unavailable | Cannot normalize final performance by equal verified training tokens. |
| Benchmark results | Benchmark-specific scores | Benchmark-specific scores | Gaps vary by benchmark; cost alone is not an efficiency proof. |

Xiaomi reports **$2.62 million** for Pro’s RL phase and **$0.85 million** for Flash’s, a **3.08× cost ratio**. Both runs had 30 stated steps and the same batch configuration, implying a **1.00× ratio of nominal rollout slots**. The archive does not verify matched final token totals, so The archived analysis does not calculate a token ratio. These costs are Xiaomi’s RL estimates, not total development costs. [Xiaomi release](https://mimo.mi.com/docs/en-US/news/latest/v2-6), accessed September 29, 2026.

In eight shared rows from Xiaomi’s released-model table, Pro’s largest reported leads were **ExploitBench (+22.6 points)** and **ExploitGym (+11.8)**. Flash came within **0.5–0.8 points** on ProgramBench and AutomationBench and scored **1.1 points higher** on CyberGym. The scores do not show that extra RL spending *caused* Pro’s advantages: the models have different backbones, and the available results lack matched independent reruns and variability estimates. [Pro model card](https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Pro-RL#3-evaluation-results), [Flash model card](https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Flash-RL#3-evaluation-results), accessed September 29, 2026.

## What the comparison shows

The calculation does not isolate a causal effect of RL budget. Reported RL costs are not total development costs or independently audited expenditure.

## Assumptions and limits

Reported RL-phase estimates are not total development costs. Different backbones, absent matched token totals, and lack of independent matched reruns prevent causal conclusions about spending and performance.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
