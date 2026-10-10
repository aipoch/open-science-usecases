# Can One Extra Token Make AI Cost 5× as Much?

## Research topic and question

- Can a small increase in prompt length cause a sudden jump in estimated API cost when it crosses a pricing threshold?
- With output fixed at 1,000 tokens, how do uncached requests, initial cache writes, and repeated cache hits compare on either side of the threshold?

## Research findings

**Under the rates supplied in this session, increasing input from 100,000 to 100,001 tokens raises the uncached estimate from $0.0105000 to $0.0525005—about fivefold.** The assumed threshold reprices the entire request, including output, rather than just the excess input token.

These are conditional USD estimates, not measured bills. The session used a user-provided pricing transcription dated October 8, 2026, labeled as Claude Haiku 5.5 pricing. It could not independently retrieve the official pages, so the model identity, rates, and threshold remain unverified. This case illustrates the calculation under those supplied assumptions; it does not establish current provider pricing.

| Input tokens | Uncached request | First five-minute cache write | Repeated cache hit |
|---:|---:|---:|---:|
| 99,000 | $0.01040000 | $0.01287500 | $0.00149000 |
| 100,000 | $0.01050000 | $0.01300000 | $0.00150000 |
| 100,001 | $0.05250050 | $0.06500063 | $0.00750005 |
| 101,000 | $0.05300000 | $0.06562500 | $0.00755000 |

At 100,000 input tokens per request, ten uncached requests total **$0.105**. One five-minute cache write followed by nine hits totals **$0.0265**; a one-hour write followed by nine hits totals **$0.034**.

Caching assumes identical, fully cacheable input, successful hits before expiry, no accumulated conversation history, and newly billed output on every request. It also assumes that cache reads and writes count toward the same threshold used to select all rates. The supplied notes do not establish that cache-specific metering rule, so these cached scenarios are conditional even on the supplied pricing.

The package includes `haiku-pricing-threshold.png`, `haiku-pricing-estimates.csv`, and `haiku-pricing-methods.md`, with six input-length examples, formulas, and source notes. No paid API requests were made. The source notes cite the [official pricing page](https://platform.claude.com/docs/en/about-claude/pricing), but direct verification was unavailable in the recorded session.
