# Can AI Find the Shortest Paris Sightseeing Route

## Research question

How does a fixed landmark order compare with simple heuristics and an exact distance minimum?

## Data and method

Keep the Eiffel Tower start and Sacré-Cœur finish fixed, verify coordinates, and save the initial order before optimization. Enumerate all 40,320 orders of the eight intermediate stops, then compare nearest-neighbor and 2-opt routes using the same straight-line metric.

## Recorded findings

Saves a fixed Paris landmark order before comparing it with nearest-neighbor, 2-opt, and exhaustive route search. Coordinates, route tables, and a map document the straight-line-distance comparison.

The saved order and nearest-neighbor route measured 13.374 km; 2-opt and exact search reached 12.118 km. The initial route was 10.359% longer under that metric.

## What the findings mean

The calculation concerns geographic distance, not pedestrian accessibility, opening hours, queues, or live traffic.

## Interpretation and limits

The optimization fixes the start, finish, and eight intermediate stops. Straight-line distance excludes streets, queues, accessibility, and traffic, so the output is not a live walking itinerary.

## Package and provenance

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.

## Import provenance

This introduction was imported from the GitHub case description. The archived export and poster retain their original contents. This reorganization did not rerun the study or independently reverify its external sources or conclusions.
