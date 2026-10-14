# Can AI Find the Cheapest Checkout with 100 Discount Rules

## Research question

How close is a saved intuitive purchase plan to the exact minimum under the same discount rules?

## Data and method

Freeze the uncoded plan before running the search. Enumerate the 203 receipt partitions for six products, enforce coupon exclusivity and stacking constraints, and compare the minimum with an independent bound. This makes the target a defined optimization problem rather than an open-ended shopping recommendation.

## Recorded findings

Constructs a small basket with 100 discount rules, saves an initial purchase plan, and compares it with a programmatic minimum. The archive includes the search, an independent optimality check, and an executed notebook export.

The saved manual plan cost $58.30; the exact search found $56.70, a $1.60 gap. The archive retains all 100 rules and the winning purchase allocation.

## What the findings mean

An exact minimum is exact only within the written prices and rules. Different availability or undocumented checkout restrictions change the feasible set.

## Interpretation and limits

The rules and prices are a constructed scenario. A blocked notebook-runner installation was handled by capturing execution in the available kernel; this does not establish optimality for arbitrary real store rules.

## Package and provenance

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.

## Import provenance

This introduction was imported from the GitHub case description. The archived export and poster retain their original contents. This reorganization did not rerun the study or independently reverify its external sources or conclusions.
