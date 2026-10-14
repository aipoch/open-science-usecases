# Can AI Extract Final Action Items, Owners, and Deadlines

## Research question

Can extraction preserve the final state of a task after a meeting changes its owner, date, or status?

Extracts final actions, owners, deadlines, and cancellation status from meeting excerpts containing corrections. The archived review checks the output against supplied excerpt identifiers and records reasons for each judgment.

## Data and comparison design

Identify each task by its excerpt and resolve revisions in context. Score the final action, owner, deadline, and active/cancelled status separately; preserve unknown deadlines rather than inventing replacements. A completed review should not become a new pending task.

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

The ten-item result is a check against these supplied excerpts, not evidence of a general error-free meeting assistant.

## Assumptions and limits

This is a supplied-document extraction exercise, not evidence that any real action was assigned or completed. This package also appears upstream under the meeting-corrections case title; the two entries are not independent replications.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
