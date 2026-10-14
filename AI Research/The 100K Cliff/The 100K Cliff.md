# The 100K Cliff

## Research question

What happens when tokenizer changes move the same text across a rate boundary?

Models a discontinuity in token costs at a supplied 100K-input-token pricing boundary. The archived script and editable pricing configuration explore discounts, workload assumptions, and tokenizer inflation.

## Data and comparison design

The analysis applies the supplied tier rule to the full serialized request, hold rates in an editable configuration, and compare uncached, caching, and batch scenarios. Convert token inflation into a text allowance by division rather than subtracting the inflation percentage.

## Recorded findings

| Request-level quantity | Recorded scenario | Implication |
| --- | --- | --- |
| Long-context boundary | 100,000 prompt tokens | A per-request boundary, not an aggregate task-token total. |
| Tokenizer inflation | 30% more tokens for the same text | New token count = 1.3 × old count. |
| Old-text equivalent at boundary | 100,000 / 1.3 ≈ 76,900 tokens | Approximately 23.1% less text fits before the boundary. |
| Discounts | Change the price level | Do not remove a ratio or boundary unless the pricing rule changes. |

The 30% tokenizer inflation moves the practical cliff substantially earlier: text that used to measure about **76.9K tokens now measures 100K**. That is **23.1% fewer pages**, not 30% fewer.

Using our 500-old-token page assumption:

- Old expectation: about **200 pages** before 100K.
- New tokenizer: about **154 equivalent pages**.
- Prompt wrappers, instructions, citations, and formatting consume part of that allowance, so a safer operational limit would be lower.

Plain-language conclusion:

- The cliff matters when one individual request lands near 100K input tokens. A tiny addition can reprice the entire input and output at 5× rates.
- Caching and Batch reduce the dollar amount, but neither moves or softens the threshold.
- It especially matters for repeated long-document workflows, because every request over 100K receives long-context pricing—even cache reads.
- It generally does not matter when requests remain comfortably below 100K, when only output length changes, or when documents are split into independent sub-100K requests.
- Splitting is not free: repeated instructions, lost cross-section context, and synthesis calls may offset some savings.
- Tokenize the complete serialized request—not merely the paper—and leave a buffer. With tokenizer drift this large, page count is only a rough planning proxy.

The pricing configuration is separated from the analysis code. Update the JSON and rerun:

```bash
python haiku55_cost_analysis.py
```

The script recreates the list-price chart, all three discounted charts, and the source CSV.

## What the comparison shows

This is a pricing model. Page counts are a planning approximation, and the historical service labels are not newly verified specifications.

## Assumptions and limits

The analysis is arithmetic on the session’s supplied pricing assumptions, not a live API billing experiment. Threshold semantics and serialized-request token counts matter; the model name and prices in the archive should not be treated as verified current service specifications.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from Hugging Face snapshot `b0218fea4fc3fc9aa37ac616aba20e619e242c1e`. The package contains the archived conversation, session metadata, and resources listed in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this reorganization.
