# Can AI Make Good Trade-Offs When Packing a Suitcase

## Research question

Can a packing choice balance utility with a hard weight limit, and can its claimed optimum be verified?

Sets up a suitcase-packing exercise with a strict weight limit and item utility scores. The conversation preserves the proposed trade-offs and attempts to verify a packing solution.

## Data and comparison design

Write each item’s weight and utility into a constrained selection problem, then compare the proposed choice with a dynamic-programming or exhaustive reference if execution is available. Separate feasibility, preference scoring, and proof of optimality.

## Recorded findings

| Evidence layer | Available material | Conclusion allowed |
| --- | --- | --- |
| Constraints and preferences | Supplied item weights, values and packing requirements | The candidate can be checked against a stated objective. |
| Saved AI selection | Candidate chosen before attempted verification | A fixed proposal, not a confirmed optimum. |
| Exact optimization attempt | Verification code and attempted notebook execution | The intended comparison is inspectable. |
| Final rerun | Blocked by shared runtime state | No newly verified optimum or optimality gap from that attempt. |

The archive retains the proposed selections and verification attempts, but its final rerun is blocked by the shared runtime state. It therefore does not provide a newly verified optimum from that attempt.

The useful comparison would evaluate the saved selection against an exact constrained solution using the same weights, values and required items. That would separate feasibility from optimality: a suitcase can satisfy every hard requirement and still leave avoidable value behind. In this record the final verification attempt is blocked, so the table deliberately distinguishes the available proposal and code from the missing verified optimum. A numerical gap would require a successful computation, not a plausible-looking packing list.

## What the comparison shows

A plausible item list is not equivalent to executed optimality checking. Utility scores also encode the scenario’s preferences rather than universal packing value.

## Assumptions and limits

The final rerun was blocked by a shell-cleanup failure. No Python or dynamic-programming verification ran in that final turn; the case must not be presented as a newly verified optimum.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
