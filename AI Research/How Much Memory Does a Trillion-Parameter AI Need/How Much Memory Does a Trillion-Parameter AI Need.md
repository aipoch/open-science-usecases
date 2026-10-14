# How Much Memory Does a Trillion-Parameter AI Need

## Research question

Why is weight storage only part of the memory needed to serve a very large model?

## Data and method

Calculate parameter storage from parameter count and bits per weight, then add quantization metadata, runtime reserves, and an explicitly parameterized KV cache. Carry bytes, decimal GB, and binary GiB separately and vary concurrent sequences and context length.

## Recorded findings

Calculates weight-storage requirements at several precisions and adds scenarios for quantization metadata, cache, and runtime overhead. The archived report keeps decimal and binary memory units and formulas visible.

The archived cache scenarios range from 4 GiB for one 8,192-token sequence to 64 GiB for four 32,768-token sequences under the same hypothetical architecture.

## What the findings mean

An architecture-specific scenario is not a measured deployment requirement. Weight precision, grouped-query attention, batching, and serving implementation can change the total.

## Interpretation and limits

Cache sensitivities use a hypothetical architecture and are estimates, not measured hardware usage. Active parameters alone do not describe the complete stored model; source specifications remain those archived at the time.

## Package and provenance

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.

## Import provenance

This introduction was imported from the GitHub case description. The archived export and poster retain their original contents. This reorganization did not rerun the study or independently reverify its external sources or conclusions.
