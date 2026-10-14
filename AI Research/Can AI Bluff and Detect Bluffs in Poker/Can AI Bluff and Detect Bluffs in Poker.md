# Can AI Bluff and Detect Bluffs in Poker

## Research question

Do calling and raising decisions change when opponents bluff more often?

Records a simplified poker experiment with preset opponent bluff frequencies and saved model actions and confidence scores. The archived report compares calling and raising behavior across the three opponent groups.

## Data and comparison design

The analysis uses a simplified scenario generator with three preset bluff frequencies and save actions and stated confidence for 30 hands per level. Compare call rates across conditions and against whether a particular opponent bet was actually designated a bluff.

## Recorded findings

### Can AI bluff, and can it detect bluffs?

**Experiment:** I built a simplified heads-up poker scenario, had an LLM (`deepseek-v4-pro`) decide fold/call/raise on the river against three opponent archetypes with preset bluff frequencies (low 15% / medium 45% / high 75%), and asked it for a confidence score on each of 90 hands (30 per level).

### Result

| Bluff level | Bluff freq | Hands | Call rate | Call-or-raise | Mean confidence |
|---|---|---|---|---|---|
| Low | 15% | 30 | 0.367 | 0.433 | 0.777 |
| Medium | 45% | 30 | 0.233 | 0.233 | 0.809 |
| High | 75% | 30 | 0.367 | 0.367 | 0.804 |

**Bluffing (producing deception):** The model essentially never raised (2/90 = 2.2%) and was heavily passive (59 folds, 29 calls). It did **not** exhibit aggressive bluffing.

**Bluff detection (call rate vs. bluff frequency):** The call rate did **not** rise with opponent bluff frequency — it was 0.367 → 0.233 → 0.367 (no monotonic trend). Reported confidence was also flat (~0.78–0.81), so it carried no discrimination signal either.

**One suggestive hint:** In the low-bluff group, the model called more when the opponent was *actually* bluffing (0.75 vs 0.31). But that rests on only 4 actual-bluff hands, so it's too thin to trust.

In this simplified setup the model did **not** convincingly bluff, and showed **weak-to-absent** bluff-detection signal — it did not reliably call more against higher bluffing frequencies.

### Important caveats
- This measures **emergent behavior of a general LLM under prompting**, not a trained poker agent; it is not a rigorous test of poker skill.
- 30 hands/level is statistically thin; call-rate differences of this size are within noise.
- The scenario generator used simplified hand/board text rather than full hand evaluation, so correctness wasn't scored — only behavior trends.

### Files (versioned artifacts)

## What the comparison shows

The scenario measures prompted behavior, not competitive poker skill. Stated confidence is not calibrated evidence of detecting a bluff.

## Assumptions and limits

This small artificial river-decision task does not establish general poker strength or reliable bluff detection. Sparse bluff cases and the simplified environment limit the reported comparisons.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
