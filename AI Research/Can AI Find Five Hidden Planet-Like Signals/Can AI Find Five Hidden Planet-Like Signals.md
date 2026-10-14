# Can AI Find Five Hidden Planet-Like Signals

## Research question

How well can numerical-summary judgments recover deliberately injected transit-like signals?

Places synthetic transit-like dips in five of 100 public stellar light curves and records reader decisions before revealing the answer key. The package compares judgments from compact numerical summaries with a periodic box-search baseline.

## Data and comparison design

The experiment starts with 100 public light curves. Synthetic changes are injected into exactly five, and reader decisions are saved before the answer key is revealed. The reader is allowed to flag any number of curves, so injection recovery and flags on the 95 unchanged curves can be counted separately. A fixed periodic box search provides the comparison; it is not treated as a verified catalogue of real planets.

## Recorded findings

The blinded challenge is complete. The archived analysis used 100 public Kepler Quarter 1 light curves from [MAST’s bulk download list](https://archive.stsci.edu/missions-and-data/kepler/kepler-bulk-downloads), injected synthetic dips into exactly five, and saved all AI decisions before revealing the key.

| Method | Injections detected | Injections missed | Flags on 95 unchanged curves |
|---|---:|---:|---:|
| AI reader | 4 | 1 | 52 |
| Periodic box search | 5 | 0 | 37 |

The AI missed C013. Its compact summary made the search score look inconsistent with the folded dip, although the close-up at the injected period shows the signal. **Flags on unchanged curves are not confirmed false discoveries**, and the injections are not new planets. The AI saw search-derived summaries, so this is a test of judgments on those summaries rather than an independent search from raw flux. Runtime and model settings were unchanged.

## What the comparison shows

These are synthetic injection recoveries, not planet discoveries. Unchanged real curves are not guaranteed negatives, and the reader sees search-derived summaries rather than raw flux alone.

## Assumptions and limits

The injected dips are not new planets, and flags on unchanged curves are not confirmed false discoveries. The reader saw search-derived summaries rather than independently analyzing raw flux.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
