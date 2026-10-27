# How Much Gas Does It Take to Make a Tesla Roadster Hover for 5 Seconds?

A car hovering on gas thrust sounds like a question about engine power. This case shows why it is also a question about carrying—and continuously losing—mass. It follows a hypothetical Roadster-like vehicle through a one-metre ascent, a five-second hover and a controlled descent, checking both the gas budget and the thrust required at every stage.

**In the adopted model, 200 kg of gas is enough for the ascent but only 3.370 seconds of subsequent hover.** Completing the prescribed two-second ascent, five-second hover and two-second descent requires approximately **347.634 kg of initial gas at the zero-reserve boundary**, with dry mass fixed at 1,800 kg. This is a calculation for an idealized propulsion system, rather than a measurement or specification of a Tesla vehicle.

## The question: lifting off is only the first requirement

The study separates three nested tasks. Each task includes the preceding stages of the same flight; the vehicle does not receive a fresh tank between stages.

| Task | What counts as success | Why the distinction matters |
| --- | --- | --- |
| Rise one metre | Reach 1 m after 2 s, with height error at most 0.02 m and vertical-speed magnitude at most 0.02 m/s | Having enough thrust to leave the ground does not establish enough fuel for the remaining mission. |
| Hover for five seconds | Complete the ascent, then remain within both tolerances for five continuous seconds | The hover consumes gas while vehicle weight steadily falls. |
| Descend and land | Complete the hover, descend under control, contact the ground at no more than 0.2 m/s and remain grounded | A mathematically smooth touchdown does not establish rebound-free ground contact. |

The model also requires nonnegative gas and upward thrust between zero and 35 kN. Once gas is exhausted, available thrust is zero. Continuing a mathematical mass curve below the retained vehicle mass would not represent a possible flight.

## What the model assumes

| Input | Baseline | Added-payload comparison |
| --- | ---: | ---: |
| Dry vehicle mass | 1,800 kg | 1,800 kg |
| Retained payload | 0 kg | 200 kg |
| Initial gas mass | 200 kg | 200 kg |
| Initial total mass | 2,000 kg | 2,200 kg |
| Maximum upward thrust | 35 kN | 35 kN |
| Effective exhaust velocity | 500 m/s | 500 m/s |
| Gravity | 9.81 m/s² | 9.81 m/s² |
| Target height | 1 m | 1 m |
| Planned ascent / hover / descent | 2 / 5 / 2 s | 2 / 5 / 2 s |

Motion is vertical only. Exhaust velocity is held constant, thrust responds instantly, and the model omits wind, drag, tilt, tank-pressure changes and actuator delay. The gas-load scan keeps the 1,800 kg dry mass fixed even when more gas is added: larger tanks and their installation mass are not included.

## How the calculation works

The vehicle follows a prescribed smooth path, rather than a simulated flight controller. The quintic shape `q(s) = 10s³ − 15s⁴ + 6s⁵` produces an ascent that starts and ends at rest, a constant-height hover, and a corresponding descent. Velocity and acceleration vanish at the phase boundaries.

For instantaneous total mass `m`, acceleration `a`, upward thrust `T` and effective exhaust velocity `vₑ`, the governing relations are:

```text
Required thrust:       T = m × (g + a)
Gas-driven mass loss:  dm/dt = −T / vₑ
Mass along the path:  m(t) = m₀ × exp(−[g × t + v(t) − v(0)] / vₑ)
Gas remaining:        m(t) − retained vehicle mass
```

Hovering therefore does not require constant thrust: gravity stays constant, but weight decreases as gas is expelled. For a rest-to-rest trajectory lasting `t_f`, the ideal minimum gas budget is `retained mass × [exp(g × t_f / vₑ) − 1]`. The full target flight lasts nine seconds. This endpoint budget must still be checked against the thrust limit throughout the trajectory.

The saved study first used fourth-order Runge–Kutta integration and then compared it with the analytic trajectory and mass law. Supplemental scans refine gas-exhaustion and thrust-limit crossings. These checks test numerical consistency; exact tracking of a prescribed path does not demonstrate a working controller.

## What happens with 200 kg of gas

The baseline begins with 19.620 kN of weight and a maximum thrust-to-weight ratio of 1.784. It can complete the prescribed ascent without using the full 35 kN capacity.

| Stage or requirement | Recorded result | Interpretation |
| --- | --- | --- |
| Two-second ascent | Reaches 1 m with effectively zero vertical speed | The first task is feasible in the ideal model. |
| Ascent gas consumption | 76.960 kg | 123.040 kg remains for hover and descent. |
| Fueled hover after ascent | 3.370 s | Falls short of the requested five seconds. |
| Exhaustion time from launch | 5.370 s | Occurs before the planned 7 s hover endpoint. |
| Controlled descent | Not reached | A zero in an uncompleted descent budget does not mean descent needs no gas. |
| Ground-contact behavior | Not modeled | No conclusion about rebound or structural safety follows. |

If thrust is set to zero after exhaustion, an ideal fall from one metre at rest takes **0.452 s** and reaches **4.429 m/s** at first contact. That is far above the study's 0.2 m/s contact-speed limit. This separate ballistic calculation is a failed uncontrolled fall, not completion of the planned descent.

## Does carrying more gas solve the problem?

More gas extends endurance, but it also increases the mass that must be lifted. The saved gas-load scan captures both effects for the same prescribed nine-second flight.

| Initial gas | Required peak thrust | Recorded outcome |
| --- | ---: | --- |
| 100 kg | 21.192 kN | Gas exhausted 2.756 s after launch. |
| 200 kg | 22.307 kN | Gas exhausted at 5.370 s. |
| 300 kg | 23.422 kN | Gas exhausted during descent, at about 7.952 s. |
| 347.634 kg | 23.954 kN | Ideal zero-reserve touchdown. |
| 400 kg | 24.538 kN | Ideal touchdown with 43.89 kg gas remaining. |
| 1,000 kg | 31.230 kN | Ideal touchdown with 546.77 kg remaining. |
| 1,300 kg | 34.576 kN | Prescribed airborne trajectory remains within the thrust cap. |
| 1,400 kg | 35.691 kN | Required thrust exceeds the cap about 0.232 s into ascent. |
| 1,800 kg | 40.153 kN | Initial weight alone exceeds 35 kN, preventing immediate lift-off. |

The resulting trajectory-feasible interval is approximately **347.634–1,338.010 kg of gas**. Its lower end comes from fuel consumption; its upper end comes from peak thrust demand. This interval applies to this trajectory with unchanged dry mass. It is not an optimized design range, and the lower boundary contains no operational reserve.

## Shorter hover or extra payload: two different changes

With the original 200 kg gas load, shortening hover to one second permits the prescribed descent and leaves about 13.12 kg of gas. The baseline's maximum fueled hover is 3.370 s if no descent reserve is held back, but only **1.370 s** when the two-second descent is included.

Adding 200 kg of retained payload moves the budget in the opposite direction:

| Quantity | Baseline | With 200 kg payload |
| --- | ---: | ---: |
| Ascent gas consumed | 76.960 kg | 84.656 kg |
| Gas left after ascent | 123.040 kg | 115.344 kg |
| Fueled hover without descent reserve | 3.370 s | 2.858 s |
| Hover with prescribed descent reserve | 1.370 s | 0.858 s |
| Minimum gas for the full nine-second path | 347.634 kg | 386.260 kg |

The payload version still completes the ascent, but its five-second hover fails earlier. Retained payload matters throughout the flight, while gas mass gradually disappears.

## What is preserved in the research record

| Evidence | What it supports |
| --- | --- |
| `final_research_report.md` | Consolidated assumptions, methods, results and corrections. |
| `baseline_phase_budgets.csv` and `baseline_task_timeseries.csv` | Shared ascent, partial hover, exhaustion and phase-by-phase gas accounting. |
| `final_gas_scan.csv` and `final_failure_cases.csv` | Gas-load outcomes and the first constraint reached in failure variants. |
| `hover_budgets_v2.csv` | Comparisons of one-, five- and ten-second requested hovers. |
| `payload200_parameters.json`, budgets and time series | Explicit retained-payload version. |
| Saved analysis scripts, PNGs and PDFs | Numerical checks and graphical presentation of the recorded calculations. |

The original study records analytic checks for zero thrust, hover, constant acceleration and constant thrust, alongside timestep refinement. For example, ascent height discrepancies were approximately `1.64 × 10⁻¹¹ m` at a 4 ms step and `1.04 × 10⁻¹² m` at a 2 ms step. Such small numerical discrepancies do not quantify uncertainty in real propulsion hardware.

## What the case establishes

The useful result is a constrained budget: **lifting off, hovering and returning under control are separate requirements, and added gas helps only while its weight remains compatible with available thrust.** The baseline completes the first requirement and fails the five-second hover; a larger gas load can complete the prescribed airborne path in the ideal model.

Measured blowdown and mass-flow curves, credible tank and installation masses, disturbance control, and a contact model are still needed to evaluate an actual vehicle. Neither a zero-reserve touchdown nor numerical agreement establishes a practical flying Roadster.
