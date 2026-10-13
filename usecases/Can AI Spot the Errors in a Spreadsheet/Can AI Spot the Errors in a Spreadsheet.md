# Can AI Spot the Errors in a Spreadsheet?

## Research topic and question

- Can you check this spreadsheet for mistakes before I use it? Tell me what looks wrong, which cells are affected, and how you would fix it.
- Here's the answer key. How many of the planted mistakes did you catch, and did you flag anything that wasn't actually wrong?

## Research findings

**I found 10 issues across the 60 order rows. The displayed net sales total of $100,455.85 is unreliable.** I checked against the workbook’s stated rules and Catalog prices; I haven’t changed the file.

All cell references below are on **Orders**.

| Affected cells | What looks wrong | Suggested fix |
|---|---|---|
| **I5** | `=SUM(I12:I68)` excludes rows 69–71, currently worth **$379.20**. | Change to `=SUM(I12:I71)`. |
| **I18** | Formula treats **4,000 g as 4,000 kg**, producing **$93,600 instead of $93.60**. | Use `=ROUND(IF(F18="g",E18/1000,E18)*G18*(1-H18),2)`. |
| **G29 → I29** | CF-103 is priced at **$26/kg**, but Catalog!C8 specifies **$30/kg**. | Set G29 to **30**. Net sales become **$128.25**, up from $111.15. |
| **I36** | Formula adds the 10% discount instead of subtracting it: **$264 instead of $216**. | Replace `(1+H36)` with `(1-H36)`. |
| **H62 → I62** | Discount is **15**, meaning **1,500%**, and produces **−$1,848**. Allowed discounts are 0–20%. | Confirm the intended discount. If it is **15%**, enter `15%` or `0.15`; net sales become **$112.20**. |
| **A22:J22 and A47:J47** | Both rows contain order **SO-1011**, with identical order details and **$168.30** net sales each. | Verify whether this is a duplicated order. If so, remove one row; if they are separate orders, recover the correct unique ID. |
| **B42** | Order date **August 31, 2026** falls outside the September 1–20 reporting period. | Verify the source date. Correct a typo, or exclude the order from this report if August 31 is accurate. |
| **C55**, compared with **B55** | Delivery is **September 17**, before the **September 18** order date. | Verify both dates. Delivery must be on/after the order date and no later than September 20. |
| **D65 → G65/I65** | **CF-999** is not one of the five permitted Catalog SKUs. | Recover the actual SKU, then apply its Catalog price and recalculate. The $28 price suggests CF-104, but does not prove it. |
| **A70** | Required order ID is blank. | Recover the ID from the source record and check uniqueness. Don’t assign one solely from the surrounding sequence. |

Resolve the uncertain source-data issues before treating any revised total as final. To prevent recurrence, add validation for IDs, SKUs, dates and discounts, and use an Excel Table so the total automatically includes new rows.
