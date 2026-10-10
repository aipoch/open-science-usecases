# Birthday Paradox: Any Pair or Your Birthday?

## Research question

Does a room of 23 people really have about a 50% chance of a shared birthday? Does that also mean a 50% chance that someone shares your birthday? This case combines an archived simulation with exact probability curves to distinguish those two events.

A shared-birthday room means **at least one pair** has the same birthday, regardless of which date or which people match. A room with several matching pairs still counts once. In the personal-birthday question, you are one of the room's `n` people, leaving `n - 1` other people who could match your fixed birthday.

## Model and method

The model assumes independent birthdays, each uniformly distributed across 365 days, with leap days ignored. It models dates within a year, not birth years or ages.

The archived Python simulation uses `random.seed(20260923)` and draws 23 birthdays for each of 10,000,000 rooms. A room counts as a hit when its set of birthdays contains fewer than 23 distinct dates. The saved Notebook output reports **5,076,297 hits**, or **50.76297%**. This is the recorded run, not a simulation rerun during this integration.

For a room of `n` people, the exact formulas are:

- **Any pair matches:** `1 - product((365 - k) / 365 for k = 0, ..., n - 1)`, for `1 <= n <= 365`.
- **Someone matches you:** `1 - (364 / 365)^(n - 1)`.

The first formula takes the complement of all birthdays being distinct. Although there are 253 pairs at `n = 23`, their match events are not jointly independent; treating 253 pair comparisons as independent trials is not the exact calculation.

## Results

The packaged CSV contains 56 rows, one for every room size from 5 through 60. Its probabilities are calculated from the exact formulas and rounded to two decimal places, rather than estimated with a separate simulation for each size.

| People in the room | Any pair shares a birthday | Someone shares your birthday |
| ---: | ---: | ---: |
| 5 | 2.71% | 1.09% |
| 10 | 11.69% | 2.44% |
| 20 | 41.14% | 5.08% |
| 23 | 50.73% | 5.86% |
| 30 | 70.63% | 7.65% |
| 40 | 89.12% | 10.15% |
| 50 | 97.04% | 12.58% |
| 60 | 99.41% | 14.94% |

The two curves answer different questions: 23 people suffice for an any-pair probability above 50%, while matching your particular birthday remains below 6% at that size.

## Evidence notes and limits

The original conversation and Notebook are preserved unchanged, including two numerical caveats checked while preparing this introduction:

1. **The personal-birthday 50% threshold is 254 total people.** The archived follow-up cell calculates `log(0.5) / log(364 / 365)`, approximately 252.652, but that quantity counts the *other* people. Adding yourself gives a continuous threshold of approximately 253.652. The first integer room size at or above 50% is therefore 254: the probability is approximately 49.9105% at 253 people and 50.0477% at 254. The conversation's claim of a 253-person crossing is off by one.
2. **The simulation difference slightly exceeds its reported 95% half-width.** The recorded estimate differs from the exact 23-person probability by approximately 0.03325 percentage points. The Notebook's normal-approximation 95% half-width is approximately 0.03099 percentage points. Thus the exact probability lies just outside that particular interval, despite the conversation describing the difference as within it. One such interval need not contain the true value; this does not disprove the birthday formula.

The chart/CSV cell saved both files before failing with `StopIteration` when it searched for the personal-birthday 50% crossing only within 5–60 people. Both files are present in the archive. The later crossing-point cell completed, but retained the missing-`+1` issue described above.

These probabilities apply to the specified independent, uniform model. They are not measurements of real birthday distributions or evidence that people in an actual room were sampled independently. The full 10-million-room simulation was not rerun during integration; the CSV formulas, rounded values, crossing threshold, and interval arithmetic were checked separately.

## Outputs and provenance

The package preserves the conversation, Notebook code and run outputs, `birthday_two_questions.csv`, `birthday_two_questions.png`, managed-file provenance, and execution evidence. The CSV and chart are also represented by managed-file artifacts whose original storage paths are retained.

The `.science` package and cover PNG are imported byte-for-byte from [aipoch/open-science-usecases at a1d1bfcb7d1c7a85d3e4a465060fa87fddc6d284](https://github.com/aipoch/open-science-usecases/tree/a1d1bfcb7d1c7a85d3e4a465060fa87fddc6d284/Birthday%20Paradox%20Simulation%20Verifying%20the%2023-Person%2050%25%20Claim). Shanruoyu contributed the case in [53aaf940](https://github.com/aipoch/open-science-usecases/commit/53aaf9404dcda39e2d395a43002ebf8b95a724bd). This introduction summarizes the recorded evidence and explicitly distinguishes it from integration-time arithmetic checks.
