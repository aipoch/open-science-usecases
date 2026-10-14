# Is Thinking Longer Worth It?

## Research question

When does extra reasoning effort buy enough improvement to justify more tokens?

Examines the relationship between recorded AI evaluation scores and estimated token costs across thinking-effort settings. The archive includes score-versus-cost charts and an analysis script.

## Data and comparison design

Place benchmark score changes beside modeled token costs for the same effort transitions. Distinguish recorded evaluation scores from estimated costs, and examine marginal improvement rather than comparing only the highest and lowest setting.

## Recorded findings

The captured effort comparison shows different score–cost tradeoffs by benchmark. High sometimes pays; max usually does not unless failure is unusually costly.

Key examples:

| Benchmark | Medium | Max | Cost increase | Score increase |
|---|---:|---:|---:|---:|
| HLE, no tools | 35.5% at $0.0069 | 45.9% at $0.2137 | 31× | +10.4 points |
| OSWorld 2.1 | 53.3% at $0.1257 | 72.4% at $0.6111 | 4.9× | +19.1 points |
| Terminal-Bench 4.0 | 20.3% at $0.6798 | 39.2% at $2.6433 | 3.9× | +18.9 points |
| FrontierCode 1.1 Main | 41.63 at $0.130 | 46.36 at $1.328 | 10.2× | +4.73 points |

The strongest warning is independent FrontierCode data:

- Medium → high costs an estimated **$48.46 per additional expected success**.
- Xhigh → max costs **$131.83 per additional expected success**.
- Medium captures about **90% of max’s score for 10% of its cost**.
- Max averages 181,387 output tokens per task versus 36,172 at medium.

Practical policy: use low for routine transformations, medium by default, high after failure or when verification is expensive, xhigh for genuinely difficult high-value work, and max only when a failed result costs substantially more than the applicable break-even value.

The saved snapshot includes every extracted effort point, cost calculations, source URLs, leaderboard versions and dates, methodological limitations, HTTP metadata, and SHA-256 hashes of the retrieved launch page, system card, and FrontierCode JSON.

## What the comparison shows

The historical model and price labels are supplied session inputs. A fresh routing decision would require current prices and a matched workload.

## Assumptions and limits

Scores and estimated costs have different evidence bases. Cost parity is modeled rather than measured across a common live workload. Model identities, pricing, and evaluation claims in the original session are historical inputs, not independently verified current product facts.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from Hugging Face snapshot `b0218fea4fc3fc9aa37ac616aba20e619e242c1e`. The package contains the archived conversation, session metadata, and resources listed in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this reorganization.
