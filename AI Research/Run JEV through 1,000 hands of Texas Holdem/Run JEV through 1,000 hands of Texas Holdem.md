# Run JEV through 1,000 hands of Texas Holdem

## Research question

What was actually evaluated under the requested poker-agent label?

Runs a reproducible heads-up poker simulation with hand logs, seed, chip accounting, and a fixed opponent. The archive reports the outcome under a per-hand rebuy format.

## Data and comparison design

The archived experiment uses a deterministic hand-strength/pot-odds bot and a hand-built heads-up engine, with a recorded seed and a rebuy to 10,000 chips each hand. Separate cumulative net chips from a conventional persistent bankroll.

## Recorded findings

### Result

**JEV finished the 1,000 hands at net **−14,050 chips** (final bankroll **−4,050** against the 10,000 per-hand buy-in).** Its opponent finished at **+14,050**.

| Metric | Value |
|---|---|
| Hands played | 1,000 (of 1,000 requested) |
| Format | Heads-up No-Limit Texas Hold'em cash game, rebuy to 10,000 each hand |
| Seed | `20260929` (Mersenne Twister) |
| JEV win rate | 46.7% (467 wins / 528 losses / 5 ties) |
| JEV net chips | **−14,050** |
| Opponent net chips | +14,050 |
| Chip conservation check | ✅ 20,000 conserved across all hands |

### Important caveats (what "JEV" actually was)

1. **"JEV" is not a real model** and isn't available in this session. I substituted a **deterministic rule-based bot** (`bot_decision()`: hand-strength + pot-odds heuristic) as the poker player, per the recorded "let the agent decide" answer. This is *not* a neural/reinforcement-learning agent.
2. **No RLCard or RL skill exists** in this session, and there was no Skill marketplace search available. I **hand-rolled** a self-contained Texas Hold'em engine (deck, 7-card best-5 hand evaluator, heads-up betting rounds, pot accounting) in Python instead.
3. **The engine was verified**: 5,000-hand chip-conservation test passed with zero leaks, and the betting-round logic was fixed after correction of an early infinite-loop/scoping bug.

### Design decisions worth flagging

- **Rebuy format**: a continuous-bankroll heads-up match naturally ends when someone busts — the bot busted at hand ~56 with either strategy pairing. To genuinely play **exactly 1,000 hands** (the literal ask), The archived analysis used a cash-game **rebuy** design (each hand starts at 10,000), which is standard for this kind of simulation and makes "final chip count" a well-defined cumulative net figure.
- The bot's fixed strategy is slightly too loose (over-raises marginal hands), so it systematically lost to the tighter opponent. That's a real result, not a bug.

### Artifacts

- jev_poker_1000_hands.science — `.science` package (zip) containing the seed, environment config, hand logs, and README for forking

**To fork it and swap in a real model:** replace `bot_decision` / `opponent_decision` in the notebook with any model that maps (stage, hole cards, visible board, to-call, pot, stack) → `fold/call/raise`, then re-run the run cell. The engine and package are fully reproducible from the seed.

## What the comparison shows

The label must not become a model-performance claim. Engine correctness, per-hand rebuys, and the fixed opponent constrain interpretation.

## Assumptions and limits

The player labeled JEV was a deterministic heuristic bot, not the requested live model, and the engine was custom rather than RLCard. Rebuy accounting should not be read as a continuous real bankroll or a model benchmark.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
