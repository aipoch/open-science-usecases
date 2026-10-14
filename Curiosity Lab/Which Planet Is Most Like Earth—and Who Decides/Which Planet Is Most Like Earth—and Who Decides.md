# Which Planet Is Most Like Earth—and Who Decides

## Research question

How do ties and weighting choices change an Earth-similarity ranking?

## Data and comparison design

The preserved analysis separates radius, temperature, distance, and composite rankings. It retains the unmodified source response and makes the handling of missing data, scaling, ties, and weights visible.

## Recorded findings

Yes—changing the definition changes the winner.

The archived analysis downloaded the NASA Exoplanet Archive’s current `pscomppars` table on September 23, 2026. It contained 6,366 confirmed planets; 5,763 had usable radius, equilibrium-temperature, and distance values.

| What is valued | Winner | Radius | Equilibrium temperature | Distance |
|---|---|---:|---:|---:|
| Radius alone | Eight-way tie at exactly 1.0 R⊕ | 1.00 R⊕ | varies widely | varies widely |
| Temperature alone | HD 40307 g | 2.56 R⊕ | 255 K | 12.94 pc |
| Distance alone | Proxima Centauri b | 1.02 R⊕ | 218 K | 1.30 pc |
| Equal weighting | Teegarden’s Star b | 1.05 R⊕ | 277 K | 3.83 pc |
| Earth-analogue weighting | Wolf 1069 b | 1.08 R⊕ | 250.1 K | 9.58 pc |
| Distance-heavy weighting | Proxima Centauri b | 1.02 R⊕ | 218 K | 1.30 pc |
| Size-heavy weighting | Proxima Centauri b | 1.02 R⊕ | 218 K | 1.30 pc |
| Temperature-heavy weighting | Wolf 1069 b | 1.08 R⊕ | 250.1 K | 9.58 pc |

The balanced ranking’s top five were:

1. Teegarden’s Star b
2. GJ 1002 b
3. Wolf 1069 b
4. Proxima Centauri b
5. TRAPPIST-1 e

The striking result is that single-variable rankings can be scientifically misleading. The eight planets recorded at exactly one Earth radius range from temperate or uncharacterized worlds to planets with equilibrium temperatures above 1,800 K. Conversely, the temperature-only list quickly fills with Neptune- and Jupiter-sized planets. Matching one Earth property does not make a planet Earth-like.

For the composite scores, I converted each criterion to a percentile rank among complete cases and applied explicit weights. Radius and temperature differences were calculated symmetrically in logarithmic space relative to 1 R⊕ and 255 K. The 255 K benchmark is Earth’s approximate black-body equilibrium temperature—not its 288 K mean surface temperature.

Important limitations:

- NASA defines `pl_eqt` as a black-body equilibrium temperature driven by stellar heating; it is not a measured surface temperature and does not incorporate an unknown greenhouse effect. [Parameter definitions](https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html)
- `sy_dist` is the distance to the planetary system in parsecs. It measures convenience or accessibility, not habitability.
- `pscomppars` provides one relatively complete composite row per planet, but NASA cautions that its values can come from different references and need not constitute a self-consistent solution.
- Some archive radii are model-derived rather than direct transit measurements.
- Atmosphere, mass, density, stellar activity, tidal locking, water, orbital stability, and uncertainties were not scored.
- The raw table is a dated snapshot; future archive updates can alter the ranking.

Thus, there is no value-neutral “most Earth-like planet.” **Teegarden’s Star b wins this particular balanced mathematical definition, Wolf 1069 b wins when Earth-like physical conditions dominate, and Proxima Centauri b wins when proximity or exploration value dominates.** The ranking documents our priorities as much as it describes the planets.

The data were retrieved through NASA’s documented synchronous TAP interface using an explicit ADQL query. [TAP documentation](https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html)

## What the comparison shows

A named winner is conditional on the selected definition. A similarity ranking is not a demonstration of habitability.
