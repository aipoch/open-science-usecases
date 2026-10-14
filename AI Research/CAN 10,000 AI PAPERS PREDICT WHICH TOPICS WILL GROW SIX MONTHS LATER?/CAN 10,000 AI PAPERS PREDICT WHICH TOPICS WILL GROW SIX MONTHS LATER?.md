# CAN 10,000 AI PAPERS PREDICT WHICH TOPICS WILL GROW SIX MONTHS LATER?

## Research question

Do earlier changes in topic shares persist in a later period?

Tracks the shares of five AI research themes across three supplied arXiv datasets. It compares changes before and after July 2024 using percentages and uncertainty rather than raw counts alone.

## Data and comparison design

The comparison uses the supplied dated topic flags across adjacent periods and distinguish counts from shares of the available paper pool. Adjust the ten period-comparison tests together with Benjamini–Hochberg correction, rather than highlighting one nominally significant result.

## Recorded findings

The AI-agent increase is too small to distinguish reliably from period-to-period variation; generative AI’s later decline is also not statistically clear.

| Theme | 2023 H2 | 2024 H1 | 2024 H2 | Before July | Later |
|---|---:|---:|---:|---:|---:|
| Retrieval-augmented | 27/5,000 (0.54%) | 80/5,000 (1.60%) | 451/17,274 (2.61%) | +1.06 pp | +1.01 pp |
| Generative AI | 80/5,000 (1.60%) | 131/5,000 (2.62%) | 378/17,274 (2.19%) | +1.02 pp | −0.43 pp |
| Large language model | 945/5,000 (18.90%) | 1,250/5,000 (25.00%) | 4,818/17,274 (27.89%) | +6.10 pp | +2.89 pp |
| Multimodal | 193/5,000 (3.86%) | 234/5,000 (4.68%) | 1,067/17,274 (6.18%) | +0.82 pp | +1.50 pp |
| AI agent | 31/5,000 (0.62%) | 41/5,000 (0.82%) | 172/17,274 (1.00%) | +0.20 pp | +0.18 pp |

Using two-proportion tests with 95% confidence intervals:

- Large language models: strong, sustained growth. Both increases are clearly nonzero (pre-July +6.10 pp, later +2.89 pp; both p < 0.001).
- Retrieval-augmented: sustained and meaningful growth relative to its low baseline (both changes about +1 pp; both p < 0.001).
- Multimodal: later growth is clear (+1.50 pp; p < 0.001). Its pre-July increase is modest and borderline (+0.82 pp; 95% CI +0.03 to +1.61; p = 0.043).
- Generative AI: the pre-July rise is clear (+1.02 pp; p < 0.001), but the subsequent −0.43 pp decline is not conclusive (95% CI −0.93 to +0.06; p = 0.072). Treat this as leveling off, not firm evidence of decline.
- AI agents: neither adjacent increase is statistically distinguishable from zero (pre-July p = 0.237; later p = 0.261). The observed rise from 0.62% to 1.00% is worth watching, but is not strong enough here to call a sustained trend.

So the conservative conclusion is: LLMs and retrieval-augmented work clearly kept gaining share; multimodal work also likely did, especially in 2024 H2. Generative AI plateaued after its early rise, and the AI-agent signal remains too small for a confident trend claim.

## What the comparison shows

The supplied selection and classification process is not documented well enough to treat this as a validated population-wide forecasting system.

## Assumptions and limits

The findings are limited to the supplied files, theme definitions, and comparison periods. Multiple comparisons and uncertain smaller changes prevent treating every apparent increase as a reliable prediction.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
