# Card Shuffle Adjacency Simulation

## Research question

How quickly does an idealized shuffle erase one visible trace of the original deck order?

Simulates repeated shuffles of an ordered deck and counts surviving original neighboring pairs. Example decks and repeated-run summaries show how this adjacency statistic changes under the chosen shuffle model.

## Data and comparison design

The record tracks whether neighboring cards in the original 52-card order remain adjacent after repeated idealized riffles. Compare example decks with repeated-run summaries and the same statistic in fully random decks.

## Recorded findings

Confirmed — the "≈2 pairs" number held up, and the comparison shows exactly where the crossover happens:

### First, the random baseline itself

I generated 1,000 completely random deck orders (every one of the 52! orderings equally likely) and counted neighbor pairs the same way:

- **Mean: 1.94 pairs** (theory says 1.96 — each of 51 pairs has a 1/26 chance of landing adjacent by coincidence)
- Typical range: 0–5, one deck even had 7
- **13% of fully random decks had zero original pairs at all**

So yes — even a perfectly random deck usually shows a couple of "original neighbors" together. It's pure coincidence.

### Now the head-to-head

| Shuffles | Shuffled mean | KS p-value | Verdict |
|---|---|---|---|
| 1 | 33.5 | ~0 | clearly different |
| 3 | 14.6 | ~0 | clearly different |
| 5 | 6.7 | 5×10⁻¹⁸² | clearly different |
| 7 | 3.5 | 2×10⁻⁴³ | **still detectably different** |
| 10 | 2.2 | 0.009 | close, nearly blended |

A more intuitive test: I asked **"could this deck have plausibly been random?"** by comparing each shuffled deck against the *single most-ordered* deck in the entire random sample (that one had 7 pairs):

- After **5 shuffles**: 33% of decks still beat the most extreme random deck — an observer could flag them as "not really mixed"
- After **7 shuffles**: only **6%** still stand out
- After **10 shuffles**: 0.3% — statistically invisible

### The answer to the stated question

The shuffled decks **start blending into the random population somewhere between 7 and 10 shuffles.** At 7 the *average* is still visibly elevated (3.5 vs 1.9), but the distributions now overlap heavily — most 7-shuffle decks look like ordinary random decks, with just a tail of stragglers. By 10, you need statistics to tell them apart, not card sense.

Worth noting the nuance: this neighbor-pair test only measures *one* kind of leftover order. Riffle shuffling also leaves subtler fingerprints (rising sequences — how many times the deck ascends in factory order — which are the classic way to count shuffles forensically). On those metrics, 7 shuffles is where Bayer–Diaconis says the deck becomes truly indistinguishable, which lines up neatly with what we're seeing here.

## What the comparison shows

Agreement on this adjacency statistic does not prove that the entire deck distribution is uniform. Real shuffling mechanics can differ from the idealized model.

## Assumptions and limits

Matching a random deck on adjacency alone does not prove that the entire deck distribution is uniform. Conclusions depend on the shuffle algorithm and the limited statistic being measured.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
