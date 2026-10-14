# Can AI Pick the Right Contact

## Research question

Can an email draft be matched to the intended person when several contacts share a name?

Matches supplied email drafts to a contact list using addressee, company, project, and role context. The archived response gives a reason for each match and is explicitly limited to preparing matches.

## Data and comparison design

The analysis uses the addressee, organization, project, and role together. Distinguish the actual requested work from background mentions of another company or project; do not choose a recipient from a name match alone.

## Recorded findings

| Matching priority | Evidence used | Decision boundary |
| --- | --- | --- |
| Addressee | The person named in the draft | A name alone is insufficient where contacts overlap. |
| Organization | The company associated with the conversation | Separates similarly named contacts in different organizations. |
| Project and role | Task context and relevant responsibility | Explains why a particular record is the best contextual match. |
| Action taken | Matching table only; no emails sent | Correct routing is evaluated separately from sending. |

The archived matching table gives an address and contextual reason for each supplied draft. It explicitly records that no emails were sent.

The recorded task ends at proposing the contact match. Its hierarchy starts with the named addressee, then uses company, project and role to disambiguate records. This matters when two people share a name or when an email draft mentions someone other than its intended recipient. The matching explanation is the inspectable output. No sending action occurred, and this description does not reproduce contact addresses from the source record.

## What the comparison shows

The output is a reviewable proposed mapping. Context-based matching does not authenticate that an address is current or authorize transmission.

## Assumptions and limits

No messages were sent. The exercise uses supplied contact records and does not establish identity beyond that dataset; ambiguous matches should remain unresolved.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
