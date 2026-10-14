# Run JEV through 1,000 hands of Texas Holdem

## Research question

What was actually evaluated under the requested poker-agent label?

## Data and method

The archived experiment uses a deterministic hand-strength/pot-odds bot and a hand-built heads-up engine, with a recorded seed and a rebuy to 10,000 chips each hand. Separate cumulative net chips from a conventional persistent bankroll.

## Recorded findings

Runs a reproducible heads-up poker simulation with hand logs, seed, chip accounting, and a fixed opponent. The archive reports the outcome under a per-hand rebuy format.

The record reports 1,000 hands and net −14,050 chips for the bot. The player called JEV in the prompt was not a live JEV model.

## What the findings mean

The label must not become a model-performance claim. Engine correctness, per-hand rebuys, and the fixed opponent constrain interpretation.

## Interpretation and limits

The player labeled JEV was a deterministic heuristic bot, not the requested live model, and the engine was custom rather than RLCard. Rebuy accounting should not be read as a continuous real bankroll or a model benchmark.

## Package and provenance

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.

## Import provenance

This introduction was imported from the GitHub case description. The archived export and poster retain their original contents. This reorganization did not rerun the study or independently reverify its external sources or conclusions.
