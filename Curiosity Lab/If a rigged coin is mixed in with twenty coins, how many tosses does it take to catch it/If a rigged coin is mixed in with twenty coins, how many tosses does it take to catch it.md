# If a rigged coin is mixed in with twenty coins, how many tosses does it take to catch it

## Research question

How do bias strength and the number of competing coins affect identification?

## Data and method

Simulate 20 fair coins and one specified biased coin, apply the same toss count to each, select the largest head count, and resolve ties uniformly. Increase counts on a recorded grid and evaluate identification probability over repeated trials.

## Recorded findings

Simulates finding one biased coin among twenty fair coins by comparing head counts. The archive varies bias and toss count and estimates identification probability under a fixed tie-breaking rule.

At a specified head probability of 0.75, the archive reaches its 95% target near 55 tosses per coin, or 1,155 tosses in total. Weaker bias requires much more data.

## What the findings mean

The grid crossing is approximate and depends on the selection rule. It is not an exact universal sample-size requirement.

## Interpretation and limits

The reported counts are approximate crossings on a simulated grid, not universal exact sample-size minima. The answer depends on bias, confidence target, selection rule, and the number of coins.

## Package and provenance

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.

## Import provenance

This introduction was imported from the GitHub case description. The archived export and poster retain their original contents. This reorganization did not rerun the study or independently reverify its external sources or conclusions.
