# AI Agents for Radio Astronomy: Is That Signal Worth Following Up?

## The question

A bright drifting feature in a radio observation can look persuasive on its own. What happens when a reference direction shows the same feature, calibration is uncertain or part of the observation is missing? This case asks what evidence should change the next action before any claim about a signal's origin is made.

The session works through **20 deliberately constructed, supplied-track teaching simulations**. It adds reference-beam evidence, coverage checks and instrument-status rules to a target-only screen, then tests how those decisions change across a frozen threshold grid. It does not operate a telescope, reproduce an ATA or NVIDIA system, evaluate an AI model's accuracy or report an astronomical discovery.

## Separate the motivating report from the experiment

| Material | Role in this case | Boundary |
|---|---|---|
| Supplied brief about AI agents at the Allen Telescope Array | Motivates pointing, calibration, data-handling and review questions | Event claims are attributed to the attachment, not independently verified in this session |
| Reported observation of the known Crab pulsar | Example of a natural astronomical source | It is not an extraterrestrial-civilization detection |
| Separate 3I/ATLAS observation and BLC1 verification background | Explain why reference observations and beam response matter | They are not the synthetic observations analyzed here |
| Five original teaching inputs | Define numerical arrays, metadata and the analysis contract | No measured telescope data or physical calibration solution is supplied |

The source brief attributes the motivating NVIDIA report to October 30, 2026. November 3 is the teaching-kit preparation date. The earlier July 2025 3I/ATLAS example is a separate observation, not another stage of that reported event.

## What the arrays contain

Each beam has a logical power-array shape of 20 cases × 32 times × 128 frequency bins. The paired table has 81,920 coordinate rows with target and reference measurements together; it should not be described as 81,920 rows per beam.

| Input property | Supplied value | Interpretation |
|---|---|---|
| Time grid | 0–31 seconds, 1-second spacing | A short synthetic observation window |
| Frequency grid | −64 to +63 Hz, 1-Hz spacing | Arbitrary offsets, with no observing band or sky coordinates |
| Power | Arbitrary linear units | Not Jy, dB, calibrated flux or coherent voltage |
| Metadata | 20 rows × 9 columns | Includes supplied status and caution information |
| Target missing cells | 2,048, or 2.5% | Kept unavailable, never zero-filled or interpolated |
| Reference missing cells | 9,216, or 11.25% | Tracked independently from target coverage |

The construction combines independent exponential noise with Gaussian-in-frequency power along predefined drifting trajectories. It omits realistic beam patterns, channelizer response, correlated receiver noise and physical calibration corrections. Seeds, injection families and amplitudes are construction information, not outcome labels. The assistant has seen that information, so this is not a blind detection experiment.

C09 has no reference measurements. C10 lacks reference time rows 0–23; C11 lacks target rows 8–23; C12 lacks reference rows 10–25. All coordinates remain in the tables with separate validity masks. Missing measurements must not become evidence that a reference feature is absent.

## Define the score before applying a threshold

The analysis follows a supplied trajectory `f(t) = start + drift × t`; it does not search every possible drift or unknown signal. Cells within 2 Hz of that trajectory form the track window. Background cells are at least 8 Hz away, leaving an excluded gap between regions.

```text
Background b = median(valid background power) / ln(2)
Excess E     = mean(valid track-window power) / b − 1
Coverage     = valid cells / geometric cells, for each window and beam
```

| Rule component | Frozen definition | Why it matters |
|---|---|---|
| Background estimate | At least 128 valid background cells and finite positive b | Fewer cells leave the score unavailable |
| Track estimate | At least one valid track cell | A computable value can still have inadequate coverage |
| Default excess threshold | h = 1, with equality passing | E = 1 means twice estimated background, not a significance or probability |
| Default coverage threshold | 0.9 in track and background for each beam | A high excess does not override missing data |
| Time-dependent excess | Same all-time beam background, with gaps for missing time rows | A noisy row crossing does not determine the aggregate classification |
| Aggregation | Valid cells receive equal weight | An unweighted average of time-row means can differ |

Target and reference use separate background normalizations. Negative excesses remain signed, unavailable values remain blank, and unsupported low-coverage scores remain visible. The score is **not calibrated SNR** and the thresholds are teaching choices, not validated astronomical cutoffs.

## Add evidence in three stages

| Stage | Evidence admitted | Recorded outcomes across 20 cases |
|---|---|---|
| A: target only | Target excess and target usability | 15 target features, 4 below threshold, 1 target-data insufficiency |
| B: add reference | Both beam scores and usable coverage | 8 shared, 4 target-local, 4 below threshold, 4 insufficient comparisons; 0 reference-only |
| C: quality and status | Calibration, instrument state and beam caution, with explicit precedence | 3 worth follow-up, 5 possible interference, 2 instrument checks, 4 insufficient, 2 beam-response follow-ups, 4 below threshold |

Stage C first checks instrument/calibration failure, then unusable beams. Only after those gates does it distinguish a shared feature with beam caution, an ordinary shared feature, a target-local feature, reference-only structure and no passing feature. A quadrant in a score plot must not override those higher-priority gates.

The opening examples show why that order changes the story:

| Case | Target E | Reference E | Target/reference view | Final action |
|---|---:|---:|---|---|
| C01 | 3.9424 | 0.0357 | Target-local, usable measurements | Worth follow-up; origin remains unresolved |
| C02 | 3.5361 | 3.9641 | Shared excess in both directions | Possible interference; check and repeat rather than assert a terrestrial source |
| C03 | 3.6017 | 0.0073 | Appears target-local before status review | Check instrument because calibration is not validated and instrument state needs review |
| C09 | 3.6780 | Unavailable | No reference coverage | Insufficient data, not a zero-reference detection |
| C13 | 12.4587 | 3.3973 | Shared, with supplied sidelobe caution | Follow up beam response before automatic interference rejection |

A real sky source can enter a reference direction through telescope response. Conversely, target-only visibility can arise from directional interference, limited reference sensitivity or missing data. Neither drift nor target-only appearance establishes extraterrestrial origin.

## Every final decision remains traceable

| Stage C outcome | Cases | Count | Appropriate next check |
|---|---|---:|---|
| Worth follow-up | C01, C16, C19 | 3 | Repeat observations and examine signal characteristics and beam response |
| Possible interference | C02, C06, C07, C08, C17 | 5 | Investigate interference sources and repeat directional observations |
| Check instrument | C03, C18 | 2 | Resolve calibration and instrument status before interpretation |
| Insufficient data | C09, C10, C11, C12 | 4 | Recover or repeat incomplete measurements |
| Follow up beam response | C13, C14 | 2 | Measure or model possible sky-source leakage into the reference |
| No feature above the teaching threshold | C04, C05, C15, C20 | 4 | Limit the result to this trajectory, usable data and specified rule |
| Reference-feature check | None | 0 | Retained as a possible rule outcome, without inventing examples |
| **Total** | **All supplied cases** | **20** | Each case appears once |

The result is a queue of next actions. “Worth follow-up” is not “confirmed source,” and “possible interference” is not proof of a terrestrial emitter. A below-threshold result says nothing about trajectories that were not evaluated.

## Test sensitivity without choosing a favorable setting

The frozen grid crosses four excess thresholds, h = 0.5, 1, 1.5 and 2, with three coverage thresholds, 0.5, 0.7 and 0.9. Each of the 12 settings includes all 20 cases once, producing 240 case-setting rows. Thirteen cases retain one outcome across the grid; seven change.

| Sensitive case | Recorded change | What it illustrates |
|---|---|---|
| C05 | Passes target excess only at h = 0.5 | A weak feature depends on the chosen excess threshold |
| C06 | Becomes target-local at h = 2 | Target and reference can cross the same cutoff differently |
| C08 | Falls below at h = 2 | Shared moderate excess need not survive a stricter rule |
| C14 | Becomes target-local at h ≥ 1.5 | A weaker reference feature can cease to trigger the shared-feature branch |
| C16 | Falls below at h ≥ 1.5 | A default follow-up result is not threshold-independent |
| C11 | Admitted as below threshold at coverage = 0.5 | Lowering the gate accepts incomplete data; it does not restore observations |
| C12 | Admitted as possible interference at coverage = 0.5 | Coverage policy changes whether a comparison is supported |

C09 and C10 remain insufficient throughout the grid. C03 and C18 retain their instrument checks. The default stays h = 1 and coverage = 0.9; no best setting or scientific optimum is selected. Stability means consistency under these particular rules, not certainty about signal origin.

## Saved materials and verification scope

The native session retains five original inputs, the conversation and evidence records, stage tables and figures. Its final `verified_radio_signal_review.zip` contains the report, `rebuild_analysis.py`, seven figures, ten result CSVs, input checksums and validation records. The all-case time series has 1,280 rows; the opening-example time series has 192; the sensitivity table has 240.

The archived fresh-process check reports regeneration from all five original inputs into an empty output directory: ten CSV tables matched, seven regenerated PNGs were readable and pixel-identical to their compared saved versions, and all 23 local report links resolved. Figure longest sides were at most 2400 pixels. The script accepts a new or existing empty output directory and refuses a nonempty one. Missing measurements are deliberately retained.

These are numerical and packaging checks. They do not calibrate detection significance, estimate telescope false-positive or false-negative rates, reconstruct absent observations or validate an AI agent. The research script was not rerun to write this introduction. Extract the complete inner ZIP for its report's local resources; this published document uses ordinary Markdown tables and text equations.

## Sources and provenance

The supplied brief links the [NVIDIA article on AI and radio-signal searches](https://blogs.nvidia.com/blog/ai-joins-the-search-for-extraterrestrial-signals/), [Breakthrough Listen's 3I/ATLAS observations](https://seti.berkeley.edu/atlas/) and the [BLC1 verification flowchart](https://seti.berkeley.edu/blc1/flowchart.html). It also cites the [setigen repository](https://github.com/bbrzycki/setigen) for methodological context; that library was not installed or used in the saved analysis.

This document summarizes the supplied AIPOCH Open-Science session. The native package remains byte-for-byte identical to the original, with only its external filename normalized to hyphens. The generated photographic-sticker cover illustrates the topic rather than documenting a particular observing setup. Publication integrity checks and an actual native import test establish transfer and compatibility, not astronomical validity.
