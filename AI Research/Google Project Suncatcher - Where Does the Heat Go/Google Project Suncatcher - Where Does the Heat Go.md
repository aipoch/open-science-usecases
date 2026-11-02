# Google Project Suncatcher: Where Does the Heat Go?

## The question

Moving AI computation into orbit changes where the electricity comes from, but it does not make the resulting waste heat disappear. How can a spacecraft reject that heat without surrounding air, and how much radiator area would a simplified calculation require?

This case uses Project Suncatcher as the starting point for five **hypothetical teaching studies** of spacecraft radiator heat balance. It varies waste heat, radiator surface temperature, infrared emissivity, absorbed environmental heating, and prescribed emitting area. The calculations explain the dependencies; they are **not measured Google spacecraft parameters**, a reconstructed prototype design, or evidence of sustained operation.

The main result is conditional: a radiator can reject a positive internal heat load at a specified surface temperature only when its emitted flux exceeds its already-absorbed environmental flux. More area helps when that margin is positive. When the margin is negative, increasing area increases net environmental heating at that temperature.

## Separate the reported milestone from the thermal model

| Evidence | What the case uses | Boundary |
|---|---|---|
| Project progress | Google's October 30, 2026 report of an AI-generated response from its prototype satellite | A returned text response does not supply radiator dimensions or demonstrate sustained thermal endurance. |
| Further testing | The report describes thermal-stress and radiation testing as subsequent work | Planned testing must not be represented as completed validation. |
| Thermal background | Heat transport through hardware and internal fluid systems, followed by radiation from external surfaces | Vacuum removes surrounding-air convection; it does not prohibit enclosed fluid circulation. |
| Quantitative scenarios | A supplied CSV of 1,095 teaching inputs | Heat loads, temperatures, emissivities, environmental fluxes and prescribed areas are assumptions. |

The source brief's November 2 campaign-selection date is not the launch or announcement date. The original research session did not independently retrieve its external source URLs; this introduction keeps the archived scenario results separate from the linked project reporting.

## Follow the heat, and define the area

The physical route has two distinct parts: moving heat away from the computing hardware, and rejecting it from the spacecraft. Package interfaces, heat spreaders, fluid loops or heat pipes can transport heat internally. The external radiator exchanges energy by radiation while also absorbing energy from its environment.

The teaching model assumes steady state, a uniform grey radiator surface, and an ideal 0 K radiative sink. That sink is a mathematical approximation, not a measured space temperature. Incoming environmental energy is represented separately as an already-absorbed flux.

| Symbol or input | Meaning | Convention that must stay visible |
|---|---|---|
| Q | Positive internal waste heat, watts | Specified for area-sizing studies; left unspecified in the fixed-area capacity study |
| T | Radiator surface temperature, kelvin | Not chip junction temperature or a certified operating limit |
| ε | Infrared emissivity | Distinct from solar absorptivity |
| q_abs | Already-absorbed environmental flux, W/m² | Normalized to the same effective emitting area; not raw incident sunlight |
| A_eff | Total effective emitting surface area, m² | Not panel footprint; no automatic one-sided/two-sided conversion |
| σ | 5.670374419 × 10⁻⁸ W m⁻² K⁻⁴ | The supplied rounded decimal representation of the Stefan–Boltzmann constant |

The equations are:

```text
Emitted flux:           q_emit = emissivity × sigma × T^4
Net outward flux:      q_net  = q_emit − q_abs
Required emitting area: A     = Q / q_net, only when q_net > 0
Fixed-area capacity:   Q_net  = A_eff × q_net
Energy balance:        emitted power − absorbed power = net rejection
```

Temperature must be in kelvin in the radiation equation; Celsius is obtained by subtracting 273.15 for labels. Computing a hotter radiator does not establish that a particular chip, thermal interface or spacecraft can operate at that temperature.

## Study 1: emitted power must cover two inputs

At an assumed 1,000 W internal heat load, 300 K radiator surface and emissivity 0.9, the emitted flux is approximately 413.3703 W/m². Environmental heating reduces the portion available to reject the internal load.

| Already-absorbed flux, W/m² | Net outward flux, W/m² | Required area, m² | Absorbed power, W | Gross emitted power, W |
|---|---:|---:|---:|---:|
| 0 | 413.3703 | **2.4191** | 0.0000 | 1000.0000 |
| 100 | 313.3703 | **3.1911** | 319.1113 | 1319.1113 |
| 200 | 213.3703 | **4.6867** | 937.3376 | 1937.3376 |

Each row sizes a different radiator under the stated assumptions. The larger gross emission in the final row does not mean the internal workload produces more heat: the surface must also emit the environmental power it absorbs. In every feasible row, emitted minus absorbed power equals the 1,000 W waste-heat input.

## Studies 2 and 3: heat load and temperature set the scale

Holding temperature, emissivity and absorbed flux fixed makes required area proportional to waste heat. The power–area study contains 18 input rows, six at each of three radiator temperatures. At emissivity 0.9 and zero environmental absorption, its areas per kilowatt are:

| Radiator surface | Celsius equivalent | Required area per kW at zero absorbed flux | Area for 1 kW at 200 W/m² absorbed flux |
|---|---:|---:|---:|
| 300 K | 26.85 °C | **2.4191 m²** | **4.6867 m²** |
| 350 K | 76.85 °C | **1.3058 m²** | **1.7673 m²** |
| 400 K | 126.85 °C | **0.7654 m²** | **0.9038 m²** |

These are model comparisons, not selected hardware operating points. With zero environmental heating, area follows an inverse fourth-power dependence on temperature. With absorption present, the denominator is instead `emissivity × sigma × T^4 − q_abs`; approaching zero from above drives the required area sharply upward.

The temperature study retains a revealing failure case: at 250 K, emissivity 0.9 and absorbed flux 200 W/m², net outward flux is approximately **−0.650899 W/m²**. There is no finite positive area that rejects a positive internal load while maintaining that specified temperature. The zero-flux threshold is about **250.2038 K**; positive rejection requires a temperature strictly above it. Undefined required area is not a negative physical area or a point to silently drop.

## Study 4: emissivity and environment determine feasibility

At fixed temperature, higher infrared emissivity increases emission and greater already-absorbed heating reduces the outward margin. The emissivity–environment study evaluates 969 hypothetical combinations at 1,000 W and 300 K. It retains 489 finite positive areas and 480 combinations with no finite positive area.

The finite sampled areas range from approximately **2.1772 to 2467.4375 m²**. Very large values near the boundary are kept rather than clipped. The archived figure uses a logarithmic scale for finite values and masks nonpositive net flux; the corresponding CSV still contains those masked rows with explicit statuses.

Across all area-sizing studies, the feasibility condition is `q_abs < emissivity × sigma × T^4`. Absorbed flux and emissivity are independent teaching inputs here, rather than a prediction of a physically realized coating, orbit and orientation combination.

## Study 5: a fixed area can have negative capacity

This comparison prescribes the effective emitting area and calculates its signed net rejection at 300 K and emissivity 0.9. The input waste-heat field is intentionally blank, rather than assumed to be zero.

| Absorbed flux, W/m² | 1 m² capacity, W | 2.5 m² capacity, W | 5 m² capacity, W |
|---|---:|---:|---:|
| 0 | 413.37 | 1033.43 | 2066.85 |
| 100 | 313.37 | 783.43 | 1566.85 |
| 200 | 213.37 | 533.43 | 1066.85 |
| 500 | **−86.63** | **−216.57** | **−433.15** |

Positive values are heat-rejection capacity. Negative values mean net environmental heating at the prescribed surface temperature. Increasing area multiplies either signed outcome; it does not turn a negative per-area margin into cooling.

At an absorbed flux of approximately **413.3703 W/m²**, emitted and absorbed powers would balance, leaving no positive capacity for internal waste heat. This is a calculated boundary. None of the 12 supplied fixed-area scenarios is exactly on it.

## Keep every scenario, including failures

| Study | Retained input rows | Outcome |
|---|---:|---|
| Baseline budget | 3 | 3 feasible areas |
| Power versus area | 18 | 18 feasible areas |
| Temperature versus area | 93 | 92 feasible; 1 undefined required area |
| Emissivity versus environment | 969 | 489 feasible; 480 undefined required areas |
| Fixed-area capacity | 12 | 9 positive capacities; 3 negative heating values |
| **Total** | **1,095** | All rows and scenario identifiers retained |

The 481 infeasible area rows stay undefined with explicit statuses. The three negative fixed-area results stay signed. Blanks distinguish unspecified inputs from inapplicable or undefined outputs; they are not filled with zeros. The five views are applications of one conditional heat-balance model, rather than five independent spacecraft experiments.

## What this says about orbital AI—and what it cannot say

| Question | Interpretation supported by the case |
|---|---|
| Does space make cooling free? | The radiator still needs a positive radiative margin and a thermal path from the hardware. |
| Does a successful text response establish endurance? | No thermal time history or sustained workload qualification is supplied by that milestone. |
| Is the calculated area a Google prototype specification? | No; it follows hypothetical heat loads, temperatures, emissivities and absorbed fluxes. |
| Can it be read as panel footprint? | Not without geometry, exposure and one-sided/two-sided emitting-area conventions. |
| Does radiator temperature determine chip temperature? | Internal thermal resistances, heat transport and local heat flux are missing. |
| Is this a complete cooling design or universal minimum area? | The simplified model omits transients, detailed geometry, view factors, eclipse timing and coating changes. |

The practical lesson is to examine the full heat path and the sign of the net radiative flux before comparing radiator areas. Claims about chip temperature, endurance, efficiency, cost or commercial feasibility need additional system data and testing.

## Saved materials and verification scope

The native session retains four original inputs, the conversation and its evidence records, study tables, explanatory figures, and `thermal_verified_bundle.zip`. The final inner bundle includes the report, six figures, five study CSVs and their combined table, `regenerate_thermal.py`, numerical checks, and all four inputs.

The archived fresh-process verification reports that the script ran successfully, reproduced all six tables exactly, and recreated six figures within a 2400-pixel maximum dimension. The largest reported absolute energy-balance residual is approximately **1.82 × 10⁻¹² W**, below its 10⁻⁹ W tolerance. Regenerated PNG pixels differ from an earlier notebook rendering; numerical agreement does not require byte-identical plots.

The archive also records that the original report Artifact could not be reopened directly. Its exact submitted text was recovered into the delivered report with a verification note. The final ZIP and its links were checked; this does not imply the earlier inaccessible Artifact was independently reopened. To use that report's local figures and links, extract the complete inner ZIP.

For publication, the native package and linked content evidence were checked and actual import into AIPOCH Open-Science was tested. The research script was not rerun for this introduction. Package integrity and import compatibility do not establish the realism of the teaching assumptions or qualify flight hardware.

## Sources and provenance

The project context is Google's [prototype-satellite response report](https://blog.google/innovation-and-ai/models-and-research/google-research/project-suncatcher-satellite-response/) and [Project Suncatcher background](https://blog.google/innovation-and-ai/models-and-research/google-research/google-project-suncatcher-facts/). Thermal background is available in [NASA's SmallSat thermal-control reference](https://www.nasa.gov/smallsat-institute/sst-soa/thermal-control/); the physical constant is linked to the [NIST Stefan–Boltzmann entry](https://physics.nist.gov/cgi-bin/cuu/Value?sigma%7Csearch_for=stefan+boltzmann).

This introduction summarizes the supplied AIPOCH Open-Science session. The generated photographic-collage cover is illustrative, not an image of verified prototype hardware. The original native package is preserved byte-for-byte; publication changes only its external filename to replace spaces with hyphens. No internal conversation, scientific result or immutable execution evidence is rewritten.
