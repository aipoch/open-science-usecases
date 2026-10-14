# How Much Memory Does a Trillion-Parameter AI Need

## Research question

Why is weight storage only part of the memory needed to serve a very large model?

Calculates weight-storage requirements at several precisions and adds scenarios for quantization metadata, cache, and runtime overhead. The archived report keeps decimal and binary memory units and formulas visible.

## Data and comparison design

The calculation uses parameter storage from parameter count and bits per weight, then add quantization metadata, runtime reserves, and an explicitly parameterized KV cache. Carry bytes, decimal GB, and binary GiB separately and vary concurrent sequences and context length.

## Recorded findings

**Using Mistral Large 4’s published rounded count of 1 trillion parameters, weight storage is approximately 2,000 GB at 16-bit, 1,000 GB at 8-bit, or 500 GB at 4-bit.** I’ve updated the chart to attribute the parameter counts to the supplied announcement notes.

According to the supplied transcription of [Mistral’s October 6, 2026 announcement](https://mistral.ai/news/mistral-large-4/), ML4 has **1 trillion total parameters and 52 billion active parameters**—approximately **5.2% active**. The announcement anticipates releasing weights and further architecture details by the end of October. These are published facts **as reported in the supplied notes**; The archived analysis did not independently retrieve the page.

Weight payload is calculated as `P × b / 8` bytes. **GB = `10⁹` bytes; GiB = `2³⁰` bytes.**

| Precision scenario | Weights: GB / GiB | Illustrative inference total: GB / GiB |
|---|---:|---:|
| 16-bit | 2,000 / 1,862.65 | 2,285.90 / 2,128.91 |
| 8-bit | 1,000 / 931.32 | 1,220.27 / 1,136.47 |
| 4-bit | 500 / 465.66 | 670.27 / 624.24 |

**All memory figures are calculated estimates, not hardware measurements.** Precision scenarios do not establish official ML4 precision support. Decimal places show the unit conversions, not certainty about the rounded parameter count.

The plotted totals retain these **illustrative assumptions, not official ML4 specifications**:

- **Quantization metadata:** a 2-byte scale plus a 2-byte zero point per 128 quantized weights, adding **31.25 GB / 29.10 GiB** at either 8-bit or 4-bit. Actual formats and mixed-precision tensors can change this.
- **KV cache:** 128 layers, 8 KV heads, head dimension 128, four sequences of 32,768 cached tokens, and 16-bit keys and values. This contributes **68.72 GB / 64 GiB**. Under conventional attention, cache memory is `2 × L × B × T × H_KV × d × s`; doubling concurrent sequences or cached tokens doubles it. Weight quantization does not automatically reduce cache precision.
- **Other runtime allowance:** `10%` of weights plus metadata, then another **16 GiB**. This is an assumed allowance for activations, workspaces, communication, and allocator overhead. Replication and loading peaks are excluded.

**Only 5.2% active does not mean only 5.2% must be stored.** Different tokens can select different experts, so a fully resident deployment retains the other expert weights for subsequent routing. Sharding distributes those weights across devices without eliminating aggregate storage. Offloading can reduce GPU residency by keeping weights in RAM or storage, at a transfer and latency cost.

The table therefore estimates **aggregate inference memory for one resident model copy**, not per-GPU requirements or training memory. Exact ML4 runtime requirements remain undetermined from the supplied announcement.

## What the comparison shows

An architecture-specific scenario is not a measured deployment requirement. Weight precision, grouped-query attention, batching, and serving implementation can change the total.

## Assumptions and limits

Cache sensitivities use a hypothetical architecture and are estimates, not measured hardware usage. Active parameters alone do not describe the complete stored model; source specifications remain those archived at the time.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
