# AI Math Citations - Do They Check Out

## Research question

Does a bibliography entry identify a real work, and does that work support the surrounding claim?

Audits a sample of bibliography entries from AI-written mathematics papers and checks a smaller set of nearby claims. The final revision separates direct publication-record evidence from later user-supplied notes.

## Data and comparison design

The sample contains five references from each of 20 papers, selected with a recorded seed. Bibliographic identities are first reconciled with publication records. The smaller claim-support exercise distinguishes metadata, abstract-level evidence and inspected theorem text. Later operator-supplied notes are retained as a separate evidence layer rather than silently promoted to direct source verification.

## Recorded findings

| Reference classification | Direct publication-record pass | Final pass including supplied notes |
| --- | --- | --- |
| Match | 80 | 88 |
| Minor bibliographic difference | 8 | 7 |
| Demonstrated genuine mismatch | 0 | 0 |
| Unresolved | 12 | 5 |


| Final reference classification | Count |
|---|---:|
| Match | 88 |
| Minor bibliographic difference | 7 |
| Demonstrated genuine mismatch | 0 |
| Unresolved | 5 |

Seven identity upgrades rely on supplied notes; Popa’s historical date is also resolved through them. Unverified dates, editions and pagination remain explicit.

For the ten claims: **3 supported narrow attributions, 3 qualified/version-limited, and 4 unverifiable**. All six favorable assessments rely on supplied operator notes—not independently inspected theorem text. The unresolved claims remain Stark, Kasteleyn, Osterwalder–Schrader and Eskin.

## What the comparison shows

An online-first versus print-year difference is not automatically a false citation. Equally, a matching DOI does not establish that the cited source proves the mathematical statement.

## Assumptions and limits

Some identity upgrades and favorable claim assessments rely on supplied notes rather than independently inspected theorem text. Unresolved references and version-dependent support remain explicit.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
