# The 100K Cliff

## Research question

What happens when tokenizer changes move the same text across a rate boundary?

## Data and method

Apply the supplied tier rule to the full serialized request, hold rates in an editable configuration, and compare uncached, caching, and batch scenarios. Convert token inflation into a text allowance by division rather than subtracting the inflation percentage.

## Recorded findings

Models a discontinuity in token costs at a supplied 100K-input-token pricing boundary. The archived script and editable pricing configuration explore discounts, workload assumptions, and tokenizer inflation.

Under the archive’s 30% inflation scenario, 100,000 new tokens correspond to about 76,900 old-token-equivalent text, roughly 23.1% less text—not 30% less.

## What the findings mean

This is a pricing model. Page counts are a planning approximation, and the historical service labels are not newly verified specifications.

## Interpretation and limits

The analysis is arithmetic on the session’s supplied pricing assumptions, not a live API billing experiment. Threshold semantics and serialized-request token counts matter; the model name and prices in the archive should not be treated as verified current service specifications.

## Package and provenance

The original `.science` export and matching poster are preserved byte-for-byte from Hugging Face snapshot `b0218fea4fc3fc9aa37ac616aba20e619e242c1e`. The package contains the archived conversation, session metadata, and resources listed in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this reorganization.
