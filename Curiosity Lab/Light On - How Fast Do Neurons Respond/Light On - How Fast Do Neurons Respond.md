# Light On - How Fast Do Neurons Respond

## Research question

How quickly do recorded neurons respond to a light pulse under a fixed response definition?

Analyzes archived public optotagging recordings with fixed quality filters and response definitions. The package records before/after spike activity, onset estimates, artifact sensitivity, and individual-trial rasters.

## Data and comparison design

The analysis applies predetermined quality filters, compare short pre/post-pulse windows, estimate onset only where the timing resolution supports it, and inspect trial rasters. Repeat artifact exclusion to see whether the selection is driven by early light-related transients.

## Recorded findings

| Selection or timing result | Recorded count | Interpretation |
| --- | --- | --- |
| Reference responder set | 31 of 995 units | The latency question is conditional on selection. |
| Resolved onsets | 7 units, 2–6 ms | A resolved onset for a subset, not every selected unit. |
| Unresolved onsets | 24 units | No precise latency is inferred for these units. |
| Stricter artifact exclusion | 30 responders remain | Tests how much the selection depends on the exclusion choice. |

The reference selection contains 31 of 995 units; seven have resolved onsets of 2–6 ms while 24 remain unresolved. Thirty survive stricter artifact exclusion.

Latency is estimated only after defining a responder set, a light level, an onset rule and an artifact-exclusion window. A response averaged across trials can support unit selection while leaving a precise onset unresolved for that unit. Reporting seven resolved onsets alongside 24 unresolved cases prevents a reader from interpreting 2–6 ms as the latency of every light-responsive neuron.

## What the comparison shows

Unresolved onset is not absence of response. Spikes near stimulation can be artifacts, and wild-type trial counts limit comparisons.

## Assumptions and limits

Some onsets remain unresolved and the wild-type comparison is descriptive. Continuous observation and residual light artifacts limit what can be inferred about direct activation or general neural latency.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
