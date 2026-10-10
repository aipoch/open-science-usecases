# Coin Flip Streaks: Selection, Luck, and a Fresh Test

## Research question

If 1,000 people independently guess the same ten fair coin flips, how often will someone look like a perfect predictor by chance? Does selecting the first-round winners give them an advantage on a fresh sequence?

This case records a survivor simulation, a crowd-size sweep, and a two-round comparison. The model assumes independent fair guesses, independent fair coin outcomes, and fresh guesses and outcomes in the second round. No skill or correlation between guessers is built into it.

## Recorded experiments

The first example uses NumPy's `default_rng(42)`. Its shared outcome sequence is `THHTTHTHTT`. Starting with 1,000 guessers, the saved output records:

| Flip | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Still correct on every flip | 522 | 239 | 119 | 57 | 29 | 13 | 6 | 4 | 2 | 1 |

The expected survivor count after flip `k` is `1000 / 2^k`; actual counts fluctuate rather than halving exactly. A subsequent recorded batch of 20,000 experiments reports at least one perfect guesser in 62.4% of runs.

The completed crowd sweep uses seed `20260923` and **100,000 runs per crowd size**. A ten-flip sequence is encoded as one integer from 0 through 1023. Every run draws a shared true sequence and an independent guessed sequence for each participant. The following are archived simulation results, not new runs from this integration:

| Crowd size | Someone perfect | Nobody perfect | Mean perfect guessers |
| ---: | ---: | ---: | ---: |
| 10 | 1.0% | 99.0% | 0.010 |
| 100 | 9.4% | 90.6% | 0.099 |
| 1,000 | 62.4% | 37.6% | 0.980 |
| 10,000 | 100.0% | 0.0% | 9.759 |

The full saved sweep also includes 50, 200, 500, 2,000, and 5,000 people. Its 100,000 repetitions are **five times**, not ten times, the earlier 20,000. Percentages rounded to 100.0% are not guarantees: the exact probability for 10,000 guessers is approximately 99.9943%.

## Probabilities that must stay separate

Let `p = 1/1024`, the probability that a given guesser gets one ten-flip sequence entirely right.

| Question | Probability under the model |
| --- | --- |
| Someone in a crowd of `N` gets one round right | `1 - (1 - p)^N` |
| A first-round winner gets the second round right, conditional on winning the first | `p = 1/1024`, approximately **0.09765625%** |
| A specified person gets both rounds right, assessed before either round | `p² = 1/1,048,576`, approximately **0.0000953674%** |
| Someone in a crowd gets both rounds right | `1 - (1 - p²)^N` |

For 1,000 people, the exact crowd-level probabilities are approximately **62.3576%** for one perfect round and **0.0953220%** for at least one person perfect across both rounds. A selected first-round winner still has an expected score of **5 out of 10** on the next independent round.

The archived two-round experiment uses seed `20260924` and 100,000 runs for each of 100, 1,000, and 10,000 people. At `N = 1,000`, it reports a conditional repeat rate of **0.1012%** among first-round winners, **0.0981%** second-round perfection among non-winners, a winner second-round mean score of **5.00/10**, and **0.099%** of crowds containing a two-round winner. Those are distinct denominators, not interchangeable estimates.

## Evidence notes and limits

The original package preserves several caveats that matter when interpreting the narration:

- The two-round table's `repeat_rate` divides two-round winners by first-round winners, while its printed `Theory` column uses the unconditional `p²`. The conversation further confuses their percentages. The formulas above distinguish the correct conditional, unconditional, and crowd-level events.
- The code generates second-round guesses for everyone so it can measure non-winners as a control group, although the printed description says only first-round winners return.
- In the initial 20,000-run batch, a `(trials, 1, 1)` true-outcome array broadcasts one bit across all ten positions, rather than generating ten separate true flips. Independent fair guesses still give the same perfect-count distribution conditional on any fixed outcome sequence, but that batch does not implement the narrated ten-independent-outcomes construction. The later crowd sweep uses complete 1,024-way sequences.
- An initial crowd-sweep cell completed its simulation loop but failed while printing `len(RUNS)` for an integer. The corrected run and its output are retained. Matching rounded percentages across runs do not mean the results are identical or free of sampling noise.

The main lesson is about selecting a visible winner from many attempts. In this model, a past perfect record does not change the probability of success on independent future data; it does not make another lucky success impossible. The model alone cannot determine whether a real person has predictive skill, whether guesses are correlated, or whether a test was fairly designed.

## Outputs and provenance

The package contains the conversation, Notebook scripts and recorded numerical outputs, dependency-analysis data, and execution evidence. Exact probabilities were independently recalculated during integration; the large stochastic simulations were not rerun, and their numbers remain labeled as archived results.

The `.science` package and cover PNG are imported byte-for-byte from [aipoch/open-science-usecases at a1d1bfcb7d1c7a85d3e4a465060fa87fddc6d284](https://github.com/aipoch/open-science-usecases/tree/a1d1bfcb7d1c7a85d3e4a465060fa87fddc6d284/Coin%20Flip%20Streak%20Simulation%20Luck%20vs.%20Skill%20Across%201%2C000%20Guessers). Shanruoyu (@shanruoyu) contributed the case in [53aaf940](https://github.com/aipoch/open-science-usecases/commit/53aaf9404dcda39e2d395a43002ebf8b95a724bd).
