# Can a Layout Change Make AI Miss Parts of Your Resume

## Research question

Does changing layout alter extracted information when the underlying resume content is held fixed?

Extracts a resume into structured fields under two layouts and compares the resulting profiles. The archived comparison reports whether values, omissions, or meaning changed.

## Data and comparison design

The comparison uses structured profiles from the two supplied layouts field by field: contact information, jobs, dates, achievements, education, and skills. Track missing values separately from altered meaning and from formatting differences.

## Recorded findings

| Field comparison | Recorded outcome | What it tests |
| --- | --- | --- |
| Missing fields | None reported | Whether layout caused supplied information to disappear. |
| Added fields | None reported | Whether extraction invented information. |
| Value differences | None reported | Whether both layouts preserve the same structured values. |
| Scope | One supplied resume in two layouts | Not a guarantee for all multi-column or visually complex resumes. |

The archive retains both extraction outputs and their comparison, making omissions and wording changes inspectable rather than relying on visual similarity alone.

The two supplied layouts are converted into the same structured schema before comparison. Missing keys test omission, added keys test unsupported extraction, and changed values test corruption of retained information. Matching JSON outputs are stronger evidence for this particular pair than the statement that the pages look similar. They still do not test a full range of tables, embedded images, unusual fonts or reading-order ambiguities.

## What the comparison shows

This is a paired example, not a general benchmark for applicant ranking, identity checking, or resume-parser accuracy.

## Assumptions and limits

The result covers the supplied resume and layouts only. Identical extractions, including the same typo corrections, do not establish robustness across arbitrary resumes.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
