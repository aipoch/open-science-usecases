# One-Shot vs Chunked

## Research question

When do intermediate summaries offset the savings from avoiding a long-context pricing tier?

## Data and method

Charge every chunk input, intermediate output, aggregation input, and final output under the supplied rates. Vary chunk count and summary length while keeping the instruction overhead visible, rather than comparing only original-document token counts.

## Recorded findings

Models token costs for reading a long document in one request versus processing chunks and aggregating their summaries. The archived analysis varies document length, chunk count, intermediate summaries, cache modes, and a tiered pricing boundary.

With 250 instruction tokens, the archive’s one-shot threshold occurs at a 99,750-token document. Above that boundary, normal-sized intermediate summaries remain far below the modeled cost break-even lengths.

## What the findings mean

The result concerns token cost only. It cannot establish which workflow better preserves reasoning or summary fidelity.

## Interpretation and limits

This is a pricing calculation, not a comparison of comprehension or summary quality. Outcomes depend on the supplied prices, token counts, and aggregation assumptions; the historical model and pricing claims were not independently reverified.

## Package and provenance

The original `.science` export and matching poster are preserved byte-for-byte from Hugging Face snapshot `b0218fea4fc3fc9aa37ac616aba20e619e242c1e`. The package contains the archived conversation, session metadata, and resources listed in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this reorganization.
