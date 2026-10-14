# One Neutrino - How Much Sky

## Research question

How large is an alert’s localization region compared with a familiar angular scale?

Audits archived IceCube alert notices and compares localization regions with an illustrative full-Moon area. Follow-up work reconciles checksums for HTML and text representations and preserves event classifications.

## Data and comparison design

Audit primary circular coordinates and uncertainty bounds, calculate areas with an explicitly described geometry, and compare 50% and 90% regions with a full-Moon reference. Keep event reclassification separate from the map arithmetic.

## Recorded findings

| Map summary | Recorded result | What it describes |
| --- | --- | --- |
| Included candidate maps | 19 after excluding an air-shower-muon case | Keeps event interpretation distinct from map geometry. |
| Median 50% area | 1.29 full-Moon areas | Area enclosing half the map probability. |
| Median 90% area | 4.34 full-Moon areas | A larger containment region, not an exact source position. |
| Provenance checks | HTML and text checksums reconciled | Document identity, not independent astrophysical validation. |

After excluding an event identified as an air-shower-muon case, the archive reports median areas of 1.29 Moons at 50% and 4.34 at 90% for 19 candidates. Later checks reconcile HTML and text checksums.

A localization map assigns probability over an area. Its 50% and 90% contours answer different containment questions, and neither contour is the event’s exact source. Expressing area in full-Moon units gives the scale without changing the probability definition. The air-shower-muon exclusion is an event-interpretation correction; it is kept separate from the later agreement between HTML and text checksums.

## What the comparison shows

A Moon-equivalent area is an illustration, not a complete probability-map description. Circular approximations and notice revisions remain relevant.

## Assumptions and limits

Confidence definitions and notice revisions matter. The final provenance correction does not verify the latest FITS versions or completeness of the full notice history.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
