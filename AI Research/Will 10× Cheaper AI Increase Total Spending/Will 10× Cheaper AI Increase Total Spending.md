# Will 10× Cheaper AI Increase Total Spending

## Research question

How can a cheaper unit price coexist with a higher total bill?

Uses a supplied sample bill to model how lower per-unit AI prices interact with higher usage. The archive saves a spending curve and identifies the break-even usage multiplier under the stated assumptions.

## Data and comparison design

Hold task sizes, retry rates, and workload mix fixed and vary only price and usage. Express the new bill as the original bill multiplied by the usage multiplier divided by ten, then distinguish total spending from cost per successful task.

## Recorded findings

Yes—AI could become 10× cheaper while total spending rises, but only if usage grows by more than 10×.

Using the fictional three-month bill:

- Current total: **$31,205.83**
- Requests: **492,500**
- Successful tasks: **449,270**
- Average cost per successful task: **$0.0695**

Assuming all token prices fall 90% and workload characteristics remain unchanged:

| Usage after price cut | New total spend | Change |
|---:|---:|---:|
| 1× | $3,120.58 | 90% lower |
| 2× | $6,241.17 | 80% lower |
| 5× | $15,602.91 | 50% lower |
| **10×** | **$31,205.83** | **Break-even** |
| 15× | $46,808.74 | 50% higher |
| 20× | $62,411.66 | 100% higher |

The governing relationship is:



`new spending = current spending × usage multiplier / 10`



So the answer depends on the rebound in demand:

- **Less than 10× more usage:** the organization saves money.
- **Exactly 10×:** the bill remains unchanged.
- **More than 10×:** total spending increases despite cheaper AI.

For example, at 20× usage, the price of each unit is one-tenth as large, but twice as many dollars are spent overall.

One important distinction: even when total expenditure rises, AI is still cheaper per task. If quality, retry rates, and task sizes stay constant, the sample’s cost per successful task falls from about **6.95 cents to 0.695 cents**. Higher total spending would therefore represent substantially more work being performed—not failure of the price reduction.

This is a rebound-effect scenario similar to Jevons’ paradox. The workbook is synthetic and covers only token charges; fixed subscriptions, infrastructure, labor, demand saturation, changing task sizes, and volume discounts could shift the real-world result.

## What the comparison shows

The demand response is a scenario input, not an estimated elasticity or a forecast of actual organizational behavior.

## Assumptions and limits

This is a cost identity and scenario calculation, not a forecast of demand elasticity. Actual spending also depends on what usage and price components change.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
