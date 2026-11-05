# Kimi K3.1 Pro: What Would It Take to Run It Locally?

## The question

An accessible model repository is only the beginning of a local deployment. How much data must be acquired, how long might that transfer take, what storage allowance changes the answer, and which runtime requirements still need evidence?

This case uses five supplied records to audit a frozen Kimi K3.1 Pro file listing and compare explicit acquisition scenarios. The full listed payload is **1,561,355,966,963 bytes: approximately 1.561356 TB or 1.420045 TiB**. A hypothetical 2,000 GB already-free storage budget holds that payload with zero reserve, but falls short by 61.355967 GB after adding a 500 GB reserve. Those calculations do not establish that a computer can load or run the model. **Local inference remains unassessed.**

The saved session downloads no weights, tensor index or containers and executes no deployment commands. It analyzes metadata and recorded deployment evidence rather than benchmarking hardware or operating a model.

## Fix the checkpoint and the evidence scope

The supplied repository metadata names `moonshotai/Kimi-K3.1-Pro` at revision `6d0a0202956796543364d666ab19c6ad1a494ee1`. Its recorded API last-modified timestamp is November 2, 2026, at 04:13:51 UTC. November 5 is the records' preparation/access date, not an established first-release date.

| Supplied material | Role in the case | Boundary |
|---|---|---|
| Repository metadata | File paths, listed sizes, LFS fields and checkpoint identity | Reported remote metadata, without local weight-body verification |
| Deployment evidence | Configuration fields, publisher descriptions and three recipe routes | Documentary evidence, without executing a route |
| Planning scenarios | Four already-free storage budgets, reserves, bandwidths and effective-throughput fractions | Assumptions rather than measurements of the user's computer or connection |
| Source brief | Links, revisions, claimed document hashes and selection context | The session did not independently fetch the linked source bodies |
| Analysis notes | Calculation and evidence-review contract | Define the analysis rather than supplying experimental results |

All five attached input byte streams are preserved with locally verified hashes. A seven-source register retains original URLs, revisions and capture information. Checking an attachment's bytes does not independently verify the hash of an external document whose body is absent.

## Count actual listed files, not a parameter-count shortcut

The metadata contains 112 unique paths, including 96 sequential weight shards and 16 other files. Shard sizes vary from 92,289,328 to 16,990,916,912 bytes. The calculation sums each listed size; it does not multiply an assumed equal shard size by the shard count.

| Payload scope | Exact bytes | Decimal GB | Binary GiB |
|---|---:|---:|---:|
| All 112 listed files | **1,561,355,966,963** | 1561.355967 | 1454.126059 |
| Safetensors files | 1,561,293,160,568 | 1561.293161 | 1454.067566 |
| Non-safetensors files | 62,806,395 | 0.062806 | 0.058493 |

Decimal GB and TB use powers of 1,000; GiB and TiB use powers of 1,024. An LFS size repeats the payload size and is not an additional download. A pointer's size is not a shard's size, and a Git blob identifier is not a locally checked weight-file SHA-256.

The 16 non-weight files include a 59,776,878-byte tensor index. Its listing is retained, but the index body was not downloaded, leaving tensor-to-shard mapping completeness unverified. The API's `usedStorage` field is 234,231 bytes below the sum of listed files. That discrepancy remains unexplained; the analysis uses the explicit listing sum as the acquisition payload.

## A storage answer depends on the reserve

The scenario's available space means **already-free usable bytes**, not a drive's advertised capacity. The model subtracts the full listed payload and the chosen reserve from that budget, preserving negative margins. Equality meets this simplified storage rule.

```text
Storage margin = already-free available bytes − reserved bytes − payload bytes
```

| Already-free budget, decimal GB | Margin with zero reserve, GB | Initial result | Margin with 500 GB reserve, GB | Revised result |
|---|---:|---|---:|---|
| 500 | −1061.355967 | Exceeds budget | −1561.355967 | Exceeds budget |
| 1,000 | −561.355967 | Exceeds budget | −1061.355967 | Exceeds budget |
| 2,000 | **+438.644033** | Meets budget | **−61.355967** | Exceeds budget |
| 4,000 | +2438.644033 | Meets budget | +1938.644033 | Meets budget |

The 2,000 GB row is the only status change between these rounds. The 500 GB reserve is an illustrative allowance, not measured cache, loading-peak or temporary-workspace demand. Among the four supplied budgets, only the 4,000 GB scenario meets the revised rule; this does not establish a universal minimum drive or a runtime pass.

## Translate bandwidth into conditional transfer time

The calculation converts every payload byte into eight bits, giving 12,490,847,735,704 bits. It divides by the nominal link rate and an assumed effective-throughput fraction.

```text
Transfer seconds = payload bytes × 8 / (nominal Mbps × 1,000,000 × effective fraction)
```

| Nominal bandwidth, Mbps | Hours at 100% | Hours at 70% | Hours at 40% |
|---|---:|---:|---:|
| 100 | 34.6968 | 49.5669 | 86.7420 |
| 300 | 11.5656 | 16.5223 | 28.9140 |
| 1,000 | **3.4697** | **4.9567** | **8.6742** |
| 2,500 | 1.3879 | 1.9827 | 3.4697 |
| 10,000 | 0.3470 | 0.4957 | 0.8674 |

At 70% effective throughput, time is 10/7 of the ideal; at 40%, it is 2.5 times ideal. The table covers 15 assumed settings, not measured network performance. Setup, retries, transport overhead, Git history and temporary copies are excluded. No target deadline is supplied, so bandwidth receives no pass/fail judgment. A faster connection changes transfer time but does not change storage margin.

## Separate recorded weight format from runtime memory

The archived evidence identifies nested compressed-tensors, `mxfp4-pack-quantized` and four-bit weight configuration. The pinned recipe describes MXFP4 routed-expert weights with other weights in BF16. Publisher references to MXFP8 activations are a separate precision statement; general BF16 dtype, eight-bit tags or U8 summaries do not establish an all-FP8 checkpoint. Physical tensor headers were not inspected.

Publisher-reported 2.8T total parameters and 104B activated per token remain attributed model descriptions, not independently counted tensors. Activated parameters do not determine total stored bytes or runtime memory.

The evidence also records a `vram_minimum_gb` value of 1874. This is a source-maintainer heuristic, approximately the safetensors decimal-GB size multiplied by 1.2. It is not a measured minimum VRAM requirement. Loading peaks, CPU RAM, temporary buffers, KV cache, context length and concurrency require their own budgets.

## Treat deployment recipes as examples to investigate

| Recorded route | Hardware example in the source | Parallelism and evidence boundary |
|---|---|---|
| B300 tensor parallelism | One node with eight B300 GPUs | TP=8; expert parallelism not requested |
| GB300 multi-node tensor parallelism | Two trays, eight GPUs total in one TP8 group | Two-node route; the total is eight GPUs, not eight per tray |
| B300 tensor plus expert parallelism | One node with eight B300 GPUs | TP=8 with expert parallelism requested; no explicit expert-parallel size supplied |

These routes name the same model repository but omit its Hugging Face revision. The archived recipe records vLLM ≥0.34.0, a nightly requirement and a named Kimi container. Exact compatibility with the pinned model snapshot and a locally installed engine remains untested. Hardware examples establish neither minimum requirements nor impossibility of other configurations or offloading approaches.

A source conflict remains visible: the pinned YAML says Docker-only, no wheel yet and `install_pip=false`, while rendered Markdown refers to an unreleased version and a nightly wheel. The case preserves both statements instead of producing a single supposedly tested installation prescription. It executes no command, remote model code, container or conversion.

## Keep readiness decisions separate

| Readiness dimension | Recorded status | What is still missing |
|---|---|---|
| File listing | Metadata validated | Actual weight hashes and complete tensor-to-shard mapping |
| Storage | Scenario only | Measured already-free space and realistic workspace allowance |
| Bandwidth | Scenario only | Sustained throughput, service conditions and a deadline |
| Engine/checkpoint compatibility | Not assessed | A tested exact snapshot, engine and installation combination |
| Hardware | Not assessed | Actual accelerators, VRAM, CPU RAM, drivers and interconnect |
| Loading peak and KV cache | Not assessed | Context, concurrency, runtime memory and temporary-buffer measurements |
| Real inference | Not assessed | Successful loading and measured outputs, throughput, latency, quality or cost |

Model-license commercial-use rights were not evaluated. Another conversion or repository would need checkpoint-specific evidence rather than inheriting these listed sizes and route descriptions.

## What the six figures are for

| Figure | Question it addresses | Interpretation boundary |
|---|---|---|
| Actual shard sizes | Is the listing internally consistent and how uneven are shards? | Does not inspect payload tensors or verify remote weight bodies |
| Initial storage | Which already-free budgets hold the listed payload with zero reserve? | Storage fit is not runtime readiness |
| Ideal transfer | How does payload-only time vary with bandwidth? | No measured connection or completion guarantee |
| Throughput sensitivity | How do 40%, 70% and 100% assumptions change time? | Scenarios do not measure utilization |
| Reserved comparison | Which storage decision changes after adding 500 GB? | The reserve is illustrative rather than a measured need |
| Summary | Which answers are numerical and which remain unknown? | Does not turn missing deployment evidence into a pass or fail |

These are views of the same supplied records and scenarios, not six independent deployment experiments.

## Saved materials and verification scope

The native session preserves five original inputs, conversation and execution evidence, file and shard tables, planning calculations, reviewed routes and six figures. The final `kimi_verified_analysis.zip` includes the report, 16 CSV tables, exact inputs, frozen evidence decisions, `reproduce.py` and verification records. The review data is a declared input whose bytes remain unchanged during rebuilding; numerical code does not regenerate semantic judgments.

The archived fresh-process verification reports a successful new Python process using all five inputs, an initially absent output directory and no old images. All 16 CSV tables and six recreated PNGs matched saved results byte-for-byte. The report matched before its verification annotation, and all 36 final report-local link occurrences resolved. The recreated figures' longest sides were at most 1950 pixels. This verifies the saved analysis and delivery in that environment, not model inference or external weight integrity.

This introduction was written without executing the archived research script or rerunning deployment. Extract the complete inner ZIP to use its report's local files. The published document uses ordinary Markdown tables and text formulas without a TeX-rendering dependency.

## Sources and provenance

The archived register links the [revision-addressed Hugging Face metadata](https://huggingface.co/api/models/moonshotai/Kimi-K3.1-Pro/revision/6d0a0202956796543364d666ab19c6ad1a494ee1?blobs=true), [pinned model card](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/resolve/6d0a0202956796543364d666ab19c6ad1a494ee1/README.md) and [pinned configuration](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/resolve/6d0a0202956796543364d666ab19c6ad1a494ee1/config.json). Recipe provenance is the [vLLM source at c5d1d77d2bd50c985c16bc11bcacd0dabab52024](https://github.com/vllm-project/vllm/blob/c5d1d77d2bd50c985c16bc11bcacd0dabab52024/recipes/models/moonshotai/Kimi-K3.1-Pro.yaml). Rendered recipe URLs are mutable; their claimed capture hashes and links are preserved in the native delivery. The saved session did not freshly retrieve those external bodies.

This document summarizes the supplied AIPOCH Open-Science session. The original native package remains byte-for-byte intact; publication normalizes only its external filename to hyphens. The generated photographic cover is illustrative. Package checks and an actual native import test establish transfer integrity and compatibility, not successful local operation of Kimi or a universal minimum machine.
