# Can AI Find the Shortest Paris Sightseeing Route

## Research question

How does a fixed landmark order compare with simple heuristics and an exact distance minimum?

Saves a fixed Paris landmark order before comparing it with nearest-neighbor, 2-opt, and exhaustive route search. Coordinates, route tables, and a map document the straight-line-distance comparison.

## Data and comparison design

The design keeps the Eiffel Tower start and Sacré-Cœur finish fixed, verify coordinates, and save the initial order before optimization. Enumerate all 40,320 orders of the eight intermediate stops, then compare nearest-neighbor and 2-opt routes using the same straight-line metric.

## Recorded findings

The fixed order was saved **before** the notebook ran:

Eiffel Tower → Arc de Triomphe → Place de la Concorde → Palais Garnier → Louvre Museum → Sainte-Chapelle → Notre-Dame de Paris → Panthéon → Luxembourg Gardens → Sacré-Cœur.

| Route | Straight-line distance | Gap to shortest |
|---|---:|---:|
| Fixed order; nearest neighbor | 13.374 km | 10.359% |
| 2-opt; exact shortest | 12.118 km | 0.000% |

The exact search checked all 40,320 orders of the eight intermediate stops. The comparison report gives both distinct orders and links to each coordinate source, including the [Eiffel Tower](https://www.wikidata.org/wiki/Q243) and [Arc de Triomphe](https://www.wikidata.org/wiki/Q64436) records. **This is not a live walking or traffic plan.**

## What the comparison shows

The calculation concerns geographic distance, not pedestrian accessibility, opening hours, queues, or live traffic.

## Assumptions and limits

The optimization fixes the start, finish, and eight intermediate stops. Straight-line distance excludes streets, queues, accessibility, and traffic, so the output is not a live walking itinerary.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
