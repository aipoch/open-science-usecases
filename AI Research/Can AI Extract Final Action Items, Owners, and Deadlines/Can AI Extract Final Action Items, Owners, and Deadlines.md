# Can AI Extract Final Action Items, Owners, and Deadlines

## Research question

Can extraction preserve the final state of a task after a meeting changes its owner, date, or status?

## Data and method

Identify each task by its excerpt and resolve revisions in context. Score the final action, owner, deadline, and active/cancelled status separately; preserve unknown deadlines rather than inventing replacements. A completed review should not become a new pending task.

## Recorded findings

Extracts final actions, owners, deadlines, and cancellation status from meeting excerpts containing corrections. The archived review checks the output against supplied excerpt identifiers and records reasons for each judgment.

The archived review marks all ten excerpts correct, including an explicitly cancelled survey and an active report whose deadline remains unspecified.

## What the findings mean

The ten-item result is a check against these supplied excerpts, not evidence of a general error-free meeting assistant.

## Interpretation and limits

This is a supplied-document extraction exercise, not evidence that any real action was assigned or completed. This package also appears upstream under the meeting-corrections case title; the two entries are not independent replications.

## Package and provenance

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.

## Import provenance

This introduction was imported from the GitHub case description. The archived export and poster retain their original contents. This reorganization did not rerun the study or independently reverify its external sources or conclusions.
