# Can AI Find the Cheapest Checkout with 100 Discount Rules

## Research question

How close is a saved intuitive purchase plan to the exact minimum under the same discount rules?

Constructs a small basket with 100 discount rules, saves an initial purchase plan, and compares it with a programmatic minimum. The archive includes the search, an independent optimality check, and an executed notebook export.

## Data and comparison design

The record freezes the uncoded plan before running the search. Enumerate the 203 receipt partitions for six products, enforce coupon exclusivity and stacking constraints, and compare the minimum with an independent bound. This makes the target a defined optimization problem rather than an open-ended shopping recommendation.

## Recorded findings

| Plan | Recorded checkout cost | Difference from exact search |
| --- | --- | --- |
| Saved manual plan | $58.30 | +$1.60 |
| Exact-search purchase allocation | $56.70 | Baseline |
| Rule inventory | 100 discount rules | The objective is the full checkout, not the sum of isolated shelf discounts. |

The session could not install Jupyter’s notebook runner because package access was blocked, so I executed the cells in the available notebook kernel and embedded those outputs in the `.ipynb`.

A checkout is a joint optimization problem. The winning allocation must specify which items are purchased together, which eligible rules are applied, and which combinations are excluded. The exact search provides a reference against which the saved manual proposal can be measured. Its $1.60 difference is a concrete failure of that proposal to reach the optimum under the supplied rule set, rather than a general failure to understand discounts. The executed notebook retains the search cells and captured outputs; an independent check is described in the archive.

## What the comparison shows

An exact minimum is exact only within the written prices and rules. Different availability or undocumented checkout restrictions change the feasible set.

## Assumptions and limits

The rules and prices are a constructed scenario. A blocked notebook-runner installation was handled by capturing execution in the available kernel; this does not establish optimality for arbitrary real store rules.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
