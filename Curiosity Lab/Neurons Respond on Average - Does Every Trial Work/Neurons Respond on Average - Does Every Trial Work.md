# Neurons Respond on Average - Does Every Trial Work

## Research question

Can a large average firing-rate response coexist with failures on individual pulses?

Separates average optotagging responses from individual-pulse reliability in the same archived recordings. The analysis compares zero-spike trials, response timing, baseline windows, and light levels.

## Data and comparison design

Reuse the reference responder set and compare matched 2–8 ms response and baseline windows pulse by pulse. Count zero-spike observations, conditional first-spike timing, and bursts rather than using only a mean rate.

## Recorded findings

**No—a clear average response does not mean every pulse produces a spike.** At the highest SST light level, **22 of 31 previously identified responders had zero-spike trials**, with individual reliability ranging from **40% to 100%**.

For those same 31 units, using a 2–8 ms response window and equally long matched baseline:

| Recorded light level | Trials with a response spike | Baseline spike probability |
|---|---:|---:|
| 1.3 | 21.5% | 6.5% |
| 1.7 | 68.9% | 5.8% |
| 2.0 | 87.0% | 6.3% |

At level 2.0, **101/775 unit–pulse observations contained no spike**, despite an average response rate of 229 Hz. Bursts on successful trials help explain that strong average. Among successful trials, the median within-unit timing IQR was **0.91 ms**.

The wild-type results remain descriptive. These two recordings cannot establish population-wide reliability, direct activation or artifact-free spiking. Zero-spike counts also assume uninterrupted spike detection and refer only to the chosen window.

## What the comparison shows

Trial reliability and average rate are different quantities. The count depends on the chosen window and on uninterrupted spike detection.

## Assumptions and limits

Two recordings cannot establish population-wide reliability, direct activation, or artifact-free spiking. Zero-spike counts rely on continuous detection and the selected response window.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
