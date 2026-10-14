# Can Jev Route Prompts as Well as General LLMs

## Research question

What does a specialized choice router gain and lose relative to a general language model?

Compares a specialized prompt router with general language models using archived public evidence on accuracy, latency, cost, deployment, and failure modes. The conversation distinguishes routing among supplied labels from free-form generation.

## Data and comparison design

The comparison uses matching-label tasks, matched test sets, latency, billed tokens, and deployment requirements. Separate public paired comparisons from runs on different samples; a fixed-label probability output and a generated explanation are not interchangeable products.

## Recorded findings

**Jev is a credible fast router for a defined set of choices, but the public evidence does not show that it is generally as accurate as a well configured LLM.** It accepts text and returns typed yes/no, choice, or score decisions with probabilities. It cannot produce explanations or choose a label outside the supplied set; it can still choose the wrong label. TypeSafe lists it at **$0.042 per million input tokens**, with output tokens unbilled. [TypeSafe primitives](https://docs.typesafe.ai/primitives); [model reference](https://docs.typesafe.ai/models).

| Option | Accuracy evidence | Latency and cost | Deployment and main risk |
| --- | --- | --- | --- |
| **Jev 1.13** | 81.0% on all 3,080 Banking77 test prompts | 175 ms median; $0.11 per 1,000 calls | Hosted API; literal instructions, incomplete labels, and distracting context can cause wrong routes. |
| **Claude Opus 5** | 84.4% on the *same* prompts | 2,266 ms median; $2.42 per 1,000 calls with prompt caching | Hosted; slower and costlier in this test. |
| **GPT-6 Luna** | 3.4 points ahead of Jev on a separate 500-prompt Banking77 sample | Jev was about 5–6 times faster; costs were roughly equal on that 77-label task | Hosted; generated output needs validation. This is not the same run as the Opus comparison. |
| **Qwen3.5-4B** | No comparable Jev routing result found | Depends on local hardware and serving setup | Open weights permit local deployment, but require an evaluation on the target prompt population. |

The Jev–Opus figures come from [OpenRouter’s paired test](https://openrouter.ai/blog/insights/jev-vs-claude-opus-5-classification/); the Luna findings come from a [separate public benchmark](https://github.com/PavelRavvich/jev-bench). Jev also reached **92.40% on Banking77** in another experiment that supplied retrieved labeled examples and developed fuller category definitions. That result shows how much the setup matters; it is not directly comparable with the one-line-label test. [Jev Banking77 experiment](https://github.com/simonmesmith/jev-banking77-experiment).

For the reproducible check here, a disclosed keyword router got **13/16** original support prompts right and missed three paraphrases. Separately, The archived check recomputed an exact paired test from OpenRouter’s published discordant counts: Opus alone got 175 right, Jev alone 72, giving **p = 4.51 × 10⁻¹¹**. This confirms the arithmetic of that reported gap, not the underlying predictions. No live model calls were made: provider credentials were unavailable, and notebook access to the raw prediction files was blocked.

**Practical choice:** trial Jev for high-volume, closed-set routing with an explicit review option and thresholds tested on a separately labeled deployment dataset. Compare it directly with a cheap structured LLM before committing: long label lists can erase Jev’s cost advantage. Keep exact rules in code and escalate ambiguous or consequential requests. [TypeSafe’s documented failure cases](https://docs.typesafe.ai/model-jaggedness/jev-1.13).

## What the comparison shows

Vendor pricing and model names are historical session inputs. Local deployment or prompt distributions need their own controlled evaluation.

## Assumptions and limits

Benchmarks, prices, and versions are those recorded in the session. Different datasets and operating conditions may not be comparable; this import does not rerun a live model evaluation.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
