# Can AI Keep Track of Corrections in Meeting Notes

## Research question

Can the final interpretation retain cancellations, transfers, and withdrawn deadlines rather than the first-mentioned facts?

Reviews meeting notes with superseded dates, ownership changes, cancellations, and unset deadlines. The final table records which interpretation matches each supplied excerpt.

## Data and comparison design

Reconcile each excerpt as a sequence of state changes. Check owner reassignment, deadline replacement, cancellation, timezone, and explicitly unknown information field by field. Preserve the reason for the chosen final state so a reviewer can trace it back to the excerpt.

## Recorded findings

| Excerpt ID | Final action | Owner | Deadline | Status | Assessment | Short reason |
|---|---|---|---|---|---|---|
| M01 | Send revised product brief | Maya | 2026-09-30 | Active | Correct | The corrected Wednesday deadline was used. |
| M02 | Upload final icons | Nina | 2026-10-02 | Active | Correct | Ownership was transferred from Leo to Nina and confirmed. |
| M03 | Send customer survey | Omar | None; former 2026-10-01 deadline revoked | Cancelled | Correct | The extraction separately identified the survey send as cancelled and did not list it as active. |
| M04 | Submit budget summary | Ben | 2026-10-02 | Active | Correct | The rejected October 5 proposal was excluded. |
| M05 | Send supplier comparison | Grace | 2026-09-30 | Active | Correct | The obsolete October 1 deadline was correctly superseded. |
| M06 | Upload demo video | Chen | 2026-09-30, 2:00 p.m. London time | Active | Correct | The final date, time, and timezone were all preserved. |
| M07 | Circulate final launch checklist | Tess | 2026-10-02 | Active | Correct | Final ownership was assigned to Tess; Ravi’s completed review was not made pending. |
| M08 | Send analytics report | Lina | Unspecified/TBD | Active | Correct | The task remained active while the withdrawn deadline was explicitly left unset. |
| M09 | Send partner deck | Hugo | 2026-10-02 | Active | Correct | The final return to October 2 was captured. |
| M10 | Publish revised release announcement | Ava | 2026-10-01 | Active | Correct | The revised announcement remained active; only the old draft was cancelled. |

Summary:

- Fully correct excerpts: **10/10**
- Field-level errors: **0**
- Invented active tasks: **0**
- Cancelled deadlines: **1** — M03’s former 2026-10-01 deadline was revoked when the task was cancelled
- Unknown deadlines: **1** — M08 remains active with no replacement deadline yet

## What the comparison shows

This overlaps with the action-item extraction collection: it emphasizes revision tracking rather than representing a separate large benchmark.

## Assumptions and limits

This is the same underlying package as the upstream final-action-items case, retained under both upstream names. The two entries must not be counted as independent evidence of extraction accuracy.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
