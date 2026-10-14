# One-Shot vs Chunked

## Research question

When do intermediate summaries offset the savings from avoiding a long-context pricing tier?

Models token costs for reading a long document in one request versus processing chunks and aggregating their summaries. The archived analysis varies document length, chunk count, intermediate summaries, cache modes, and a tiered pricing boundary.

## Data and comparison design

Charge every chunk input, intermediate output, aggregation input, and final output under the supplied rates. Vary chunk count and summary length while keeping the instruction overhead visible, rather than comparing only original-document token counts.

## Recorded findings

The crossover is primarily a pricing discontinuity, not a gradual break-even point. With 250 instruction tokens, one-shot remains cheaper through a **99,750-token paper**; immediately above that, its prompt enters the expensive tier and segmentation becomes much cheaper for normal chunk-summary lengths.

For ordinary uncached aggregation, once one-shot is above the threshold, the break-even chunk-summary length is:



`S* = [0.4L + 0.1(4 − N)I + 2O] / (0.6N)`



where `L` is paper tokens, `N` is chunk count, `I = 250` instruction tokens, and `O = 1,000` final-output tokens.

| Paper length | 2 chunks | 4 chunks | 8 chunks |
|---:|---:|---:|---:|
| 100K | 35.0K/chunk | 17.5K/chunk | 8.7K/chunk |
| 106K | 37.0K/chunk | 18.5K/chunk | 9.2K/chunk |
| 126K | 43.7K/chunk | 21.8K/chunk | 10.9K/chunk |

Thus a 500-token chunk summary is nowhere near erasing segmentation’s advantage above 100K. Below 100K, one-shot is always cheaper under this model because both workflows use the same cheap tier while segmentation adds intermediate output and aggregation input.

The script exposes prices, tier boundary, instruction lengths, output lengths, cache mode, chunk size/counts, sensitivity ranges, paper estimates, and output filenames in the top-level `CONFIG`. Its cache modes are `none`, `write`, and `read`.

This analysis is exclusively about token cost. It makes no inference about comprehension, summary fidelity, information loss, or which workflow produces better summaries.

## What the comparison shows

The result concerns token cost only. It cannot establish which workflow better preserves reasoning or summary fidelity.

## Assumptions and limits

This is a pricing calculation, not a comparison of comprehension or summary quality. Outcomes depend on the supplied prices, token counts, and aggregation assumptions; the historical model and pricing claims were not independently reverified.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from Hugging Face snapshot `b0218fea4fc3fc9aa37ac616aba20e619e242c1e`. The package contains the archived conversation, session metadata, and resources listed in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this reorganization.
