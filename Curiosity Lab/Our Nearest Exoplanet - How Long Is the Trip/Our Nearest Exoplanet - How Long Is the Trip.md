# Our Nearest Exoplanet - How Long Is the Trip

## Research question

How does a simple distance–speed calculation change near relativistic speeds?

## Data and comparison design

The existing explanation distinguishes external travel time from traveler proper time and keeps its nearest-system selection, distance units, constant-speed assumption, and uncertainty treatment explicit.

## Recorded findings

The nearest confirmed exoplanets are **Proxima Centauri b and d**, tied because they orbit the same star. NASA’s current distance is **1.30119 ± ~0.00035 parsecs**, or **4.24391 light-years**.

### One-way travel times

Assuming the spacecraft travels the entire distance at a constant speed:

| Cruise speed | Lorentz factor γ | Earth-frame time | Time onboard |
|---|---:|---:|---:|
| 17 km/s | 1.0000000016 | 74,841 years | 74,841 years |
| 1% of light speed | 1.000050 | 424.39 years | 424.37 years |
| 10% of light speed | 1.00504 | 42.44 years | 42.23 years |
| 90% of light speed | 2.294 | 4.72 years | 2.06 years |

At 17 km/s, relativistic time dilation saves the travelers only about **1.05 hours**. At 1% light speed it saves about **7.8 days**, at 10% about **78 days**, and at 90% about **2.66 years**.

The calculation is:



`Earth-frame time = D / v`  
`onboard time = Earth-frame time / γ`  
`γ = 1 / √(1 − v²/c²)`



### Data provenance

Retrieved **23 September 2026** from NASA’s live `pscomppars` table using TAP. The downloaded table contains 6,338 confirmed-planet records with non-null distances. NASA documents `pscomppars`, synchronous ADQL queries, and CSV output in its [TAP guide](https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html).

The two closest rows were:

- Proxima Cen b — 1.30119 pc
- Proxima Cen d — 1.30119 pc

### What these journeys leave out

These are idealized cruise-time calculations. They assume instantaneous acceleration and braking, so a real trip would take longer and the onboard proper time would depend on the acceleration profile. They also omit:

- The enormous propulsion energy and reaction mass required—especially near 0.9c.
- Heating and potentially catastrophic impacts with interstellar dust and gas.
- Radiation shielding, life support, maintenance, and reliability over decades to millennia.
- Navigation and interception of a star that continues moving during the flight.
- Slowing down at Proxima Centauri rather than simply passing through the system.
- The approximately 4.24-year one-way communication delay after arrival.
- Distance uncertainty, which is small here—about 0.027%—but propagates linearly into every listed time.

Thus, the 90%-of-light-speed result is a valid special-relativistic comparison, not a presently credible mission design.

## What the comparison shows

The arithmetic does not supply propulsion, acceleration, shielding, or a feasible mission design. Retain that physical distinction beside the numerical table.
