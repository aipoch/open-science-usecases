# Neutrino Energy - Does Higher Mean Sharper

## Research question

Does the overall energy–uncertainty trend hold across sky directions?

Compares reconstructed muon-energy indicators with estimated angular uncertainty in a supplied IceTracks season. The session examines sky-direction strata, calendar subsets, reporting floors, rounding, and counterexamples.

## Data and comparison design

The comparison uses reconstructed muon-energy indicators with estimated angular uncertainty, then stratify by declination and calendar subset. Audit the reporting floor and rounding before treating a strong overall correlation as uniform across the detector’s field of view.

## Recorded findings

**Overall, yes—but the relationship depends strongly on sky direction.** Across 127,695 events from May 2021–May 2022, higher reconstructed **muon** energy accompanies smaller **estimated** angular uncertainty: Spearman ρ = **−0.530**, with 95% bootstrap CI **[−0.535, −0.526]**.

| Population | Spearman ρ | 95% bootstrap CI |
|---|---:|---:|
| 2021 | −0.535 | [−0.540, −0.529] |
| 2022 | −0.523 | [−0.530, −0.517] |
| Declination −90° to −30° | **+0.224** | [+0.211, +0.238] |
| Declination −30° to 0° | −0.368 | [−0.381, −0.356] |
| Declination 0° to 30° | −0.203 | [−0.212, −0.194] |
| Declination 30° to 90° | −0.164 | [−0.174, −0.153] |

All four right-ascension sectors look similar. The southern reversal persists in both years and after excluding floor-valued events. Finer declination bands also reveal reversals hidden by broader grouping.

The quantiles show a substantial overall decrease, followed by an upturn: median uncertainty falls from **1.10°** in the lowest energy bin to **0.20°** in the ninth, then rises to **0.26°** in the highest.

- **Reporting floor:** 14.74% of events equal the documented 0.20° minimum. Excluding them weakens the overall correlation to **−0.377**, but does not eliminate it.
- **Rounding:** perturbing values within their reporting precision barely changes ρ. Unreported values below the floor cannot be recovered.
- **Counterexamples:** event `136407 / 18743252 / 0` has log-energy **5.87** but uncertainty **5.13°**; event `135352 / 47825884 / 2` has log-energy **2.70** and reported uncertainty **0.20°**.

These findings concern reconstructed muon energy—not true neutrino energy—and estimated uncertainty—not measured error against a true direction. **No independent event-quality flag is supplied.**

## What the comparison shows

Reconstructed muon energy is not neutrino energy, and an uncertainty estimate is not measured source-location error.

## Assumptions and limits

Reconstructed muon energy is not true neutrino energy, and estimated uncertainty is not measured error against a known direction. An overall association need not hold within every sky region.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
