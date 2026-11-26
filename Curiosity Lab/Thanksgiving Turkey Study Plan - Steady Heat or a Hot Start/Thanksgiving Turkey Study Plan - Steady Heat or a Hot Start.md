Would a short, hot start heat a turkey's interior more effectively than steady oven heat? This case turns that Thanksgiving question into a study plan, a deliberately simplified heat-transfer model, sensitivity scenarios and a template for collecting real measurements. The reported temperatures and times are **illustrative model predictions, not cooking instructions or observations from a real turkey**.

The main finding is conditional: one schedule reaches the chosen two-site endpoint first under the baseline assumptions, but the ordering can reverse when the assumed heat paths or schedule-specific oven exposure change. That makes the assumptions and the next useful measurement more important than declaring a universal winning recipe.

## Research question and comparison

The study considers a fully thawed, unstuffed turkey described as 5 kg and compares three proposed oven histories. Mass is contextual: the model does not reconstruct a three-dimensional 5 kg body, and mass alone cannot determine the distances heat must travel to an interior probe.

| Schedule | Prescribed model boundary | Comparison role |
|---|---|---|
| A | Constant 165°C | Lower steady-temperature history |
| B | Constant 180°C | Higher steady-temperature history |
| C | 220°C for 20 minutes, then 165°C | Hot-start history followed by the same setting as A |

The endpoint is the first time **both representative slab centers** reach approximately 74°C. Breast and thigh are modeled separately. This two-point endpoint is not evidence that every part of a real bird has reached a safe temperature.

## Model, evidence and unsupported inputs

Two independent one-dimensional planar half-slabs solve transient conduction, using symmetry at the center and a fixed effective heat-exchange boundary at the surface. Backward Euler finite volumes provide the numerical solution. The center of each slab is the reported representative site.

| Input or assumption | Retained value or treatment | Interpretation |
|---|---|---|
| Breast center-to-surface path | 35 mm | Unsupported demonstration geometry, not a measurement inferred from mass |
| Thigh center-to-surface path | 45 mm | The longer assumed path makes this site the limiting one in the baseline. |
| Starting temperature | Uniform 4°C | Demonstration assumption |
| Thermal properties | `k = 0.464 W/(m K)`, `rho = 1050 kg/m³`, `cp = 3530 J/(kg K)` | Constant poultry-property proxies, not calibrated turkey measurements |
| Surface exchange | Fixed effective coefficient about 19.252 W/(m² K) | Combines convection and radiation; a separate radiation term is not added. |
| Oven history | Instantaneous response to the specified schedule | Loading recovery, cycling and finite cooldown are omitted. |

Both sites use identical material properties. Their heating difference comes from the assumed path lengths; swapping the lengths would swap the trajectories. The study preserves evidence and parameter tables distinguishing public guidance, research-property proxies and unsupported demonstration choices. It does not digitize new temperature measurements or calibrate against a real bird.

## Baseline model predictions

The values below are simulated threshold times, rounded to one decimal minute. They must not be used as a cooking timetable.

| Schedule | Breast center to 74°C (min) | Thigh center to 74°C (min) | Both-site endpoint (min) | Site gap (min) |
|---|---:|---:|---:|---:|
| A | 121.2 | 176.4 | 176.4 | 55.2 |
| B | 110.4 | 161.1 | 161.1 | 50.6 |
| C | 113.8 | 169.2 | 169.2 | 55.4 |

For these inputs, B reaches the endpoint before C, which reaches it before A. That is a conditional model ordering, not an optimal cooking recommendation. The model omits evaporation and moisture transport, and its overshoot temperatures are not validated measures of dryness, tenderness or eating quality.

## Does the ordering survive changed assumptions?

The requested matched scenarios increase both heat paths by 20%, lower every oven schedule by 10°C, or combine those changes. These are selected perturbations, not random draws or statistical confidence intervals.

| Chosen scenario | A endpoint (min) | B endpoint (min) | C endpoint (min) | Earlier to later |
|---|---:|---:|---:|---|
| Baseline | 176.4 | 161.1 | 169.2 | B, C, A |
| Both paths 20% longer | 233.8 | 213.7 | 226.6 | B, C, A |
| All oven histories 10°C lower | 189.1 | 170.9 | 181.4 | B, C, A |
| Longer paths and cooler histories | 250.2 | 226.5 | 242.6 | B, C, A |
| Both paths scaled to 0.4 of baseline | 48.2 | 43.6 | 39.9 | C, B, A |
| Only B runs 10°C below its nominal setting | 176.4 | 170.9 | 169.2 | C, B, A |

For B, the selected thickness increase changes the endpoint by about 52.7 minutes, or 32.7%, while the common 10°C reduction changes it by about 9.8 minutes, or 6.1%. Those are effects of particular perturbations, not standardized sensitivities or a global ranking of parameter importance.

### Two different reversal examples

With much shorter assumed paths—14 mm and 18 mm in the 0.4× example—the hot start reaches the interior sooner relative to the later sustained heating. The refined B/C tie occurs near a common length multiplier of 0.599, corresponding to about 21.0 mm and 27.0 mm. That is a model crossover, not a measured anatomical boundary for a 5 kg turkey.

The B-only temperature error is a different comparison. A and C retain their nominal histories while B is cooler. The archived search finds a B/C tie near a B-only offset of −8.4°C on the baseline grid. It must not be described as the result of a common oven calibration error applied equally to all three schedules.

In the shared-input passive conduction model, B's boundary stays hotter than A's and C's is never cooler than A's. That boundary ordering explains why A does not win these matched scenarios. B and C have crossing oven histories, so their relative ordering depends on heat propagation and exposure.

## Numerical checks and the three final figures

The baseline grid uses 60 intervals per site and 5-second steps; the refined grid uses 120 intervals and 2.5-second steps. Threshold times are interpolated. Across six scenarios at both resolutions, the saved sensitivity table contains 36 rows.

The largest retained endpoint shift between resolutions is about 0.01845 minutes, or 1.11 seconds. Temperature-bound and discrete-energy checks pass in the archived records. These are numerical consistency checks, not an uncertainty interval, anatomical calibration or experimental validation.

| Final figure | Question it addresses | Reading boundary |
|---|---|---|
| Heating trajectories and endpoint comparison | How do two assumed heat paths respond to the three schedules? | Simulated temperatures; not probe readings |
| Sensitivity and reversals | Which chosen changes preserve or reverse the B/C order? | Selected scenarios; not a statistical distribution |
| Recording one real trial | What would need to be measured next? | An experimental recording design, not an experiment already performed |

The organized ZIP retains a clean rerun record matching baseline histories and threshold times, all 36 sensitivity rows and all three final figures pixel-for-pixel. The recorded baseline history difference is at floating-point scale, about `2.84e-14°C`. Reproducing the same model output does not validate its physical assumptions.

## What would one real turkey teach us?

The study proposes recording actual oven temperature over time, representative breast and thigh temperatures, elapsed time, geometry and exact probe placement. The limiting thigh heat path is a useful next measurement because it is unsupported in the baseline and strongly affects the selected scenarios. Recording the oven transition is also important for distinguishing actual exposure from a dial setting.

One trial can compare one measured schedule with its corresponding prediction and expose mismatches. It cannot establish the counterfactual result of the other schedules, estimate population variability or prove a generally optimal method. Real eating quality would need an appropriate outcome measure beyond simulated temperature overshoot.

## Safety and physical limits

The model does not include bone, skin and fat, cavity or pan exchange, three-dimensional coupling, changing material properties, oven recovery, evaporation, carryover heating or pathogen-lethality integration. The two slab sites omit other possible cold spots, including the wings.

For actual cooking, use current official food-safety guidance rather than this simulation. [USDA FSIS](https://ask.fsis.usda.gov/article/What-is-the-internal-temperature-and-cooking-time-for-turkey) specifies a minimum internal temperature of 165°F (73.9°C) measured with a thermometer, checking the innermost thigh and wing and the thickest breast. [CDC guidance](https://www.cdc.gov/food-safety/foods/holiday-turkey.html) also describes the required measurement locations, avoiding bone. A simulated two-site threshold cannot establish whole-bird safety.

## Retained materials and verification scope

The final 28-file study ZIP contains the README, evidence and parameter tables, portable Notebook, model code and settings, simulated data, three final figures, reports, a recording template and provenance records. Its portable Notebook organizes a verified workflow but does not replace the full native Notebook history.

The native export separately records seven explicitly excluded artifact-version contents. Those omissions remain disclosed; import compatibility does not make every historical content version available. Publication preparation verifies the bytes actually included, the declared exclusion boundary, ZIP checksums and the saved result-table relationships. It does not rerun the archived solver or collect any real-turkey measurements.

This AIPOCH Open-Science case shows how to move from a seasonal question to testable assumptions, conditional predictions and a measurement plan. The question-led cover is illustrative artwork, and the original native package is preserved without internal edits.
