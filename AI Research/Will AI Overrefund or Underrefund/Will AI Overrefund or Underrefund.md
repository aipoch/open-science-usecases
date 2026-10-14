# Will AI Overrefund or Underrefund

## Research question

Can a policy-based calculation distinguish the charge components that remain eligible in an edge case?

Applies a supplied refund policy to individual requests and reviews edge cases involving deadlines, coupons, shipping, tax, and digital delivery. The archive shows arithmetic and explicit choices when policy clauses overlap.

## Data and comparison design

The analysis applies the same supplied rules to request date, damage, discounts, shipping, tax, missing accessories, duplicates, and digital access. Keep the item amount and each ancillary charge separate, and record which clause resolves an overlap.

## Recorded findings

The calculation remains **$721.61** after reviewing the specified edge cases.

| Edge case | Cases | Review outcome |
|---|---|---|
| Late requests | R03, R10, R14, R19 | All correctly receive $0. R11 remains eligible because damage was reported on day 28. |
| Coupons | R09, R17 | Restocking fee correctly uses the discounted price actually paid: 90% × $60 = $54; 90% × $50 = $45. |
| Shipping | R01, R11, R16 | Refunded for damaged-on-arrival items. |
| Shipping | R02, R09, R13, R17 | Not refunded for change-of-mind returns. |
| Duplicate shipping | R08, R15 | Refunded because it was attached to the duplicate charge. |
| Tax | Damaged, eligible digital, missing-accessory, and duplicate cases | Refunded fully or proportionally under rule 10. |
| Tax | Change-of-mind cases | Not refunded because rule 3 explicitly excludes it. |
| Gift cards | R07 | Correctly receives $0. |
| Missing accessories | R04, R18 | Listed accessory value refunded, plus proportional tax. |
| Missing accessory without value | R12 | Correctly receives $0. |
| Download eligibility | R05, R20 | Eligible because the link failed and no download succeeded. R06 is ineligible because it was downloaded. |

Ambiguities and assumptions:

- **Change-of-mind tax:** Rule 3 explicitly says tax is non-refundable, while rule 10 generally says tax follows the refundable-item proportion. I treated the specific change-of-mind exclusion as controlling, so R02, R09, R13, and R17 receive no tax.
- **Missing-accessory tax:** Rule 7 identifies the accessory value as the partial refund, while rule 10 requires proportional tax. I therefore included tax proportional to the accessory’s share of the item price: R04 = $12 + $1.07 and R18 = $8 + $0.70.
- **Duplicate-charge tax:** Rule 8 says the duplicate charge is refunded “in full,” explicitly including attached shipping. I treated “in full” as including the supplied tax, giving R08 $32.40 and R15 $23.76.
- **Digital requests after 30 days:** Rule 5 does not separately state a deadline. I applied the general 30-day limit and rule 4’s sole late exception for timely reported arrival damage, making R14 ineligible.
- **Damaged-item tax:** Rule 2 mentions the item and shipping but not tax. Under rule 10, a fully refundable item carries 100% of its supplied tax, so tax was included for R01, R11, and R16.
- **Rounding:** Proportional tax was rounded to the nearest cent per case before totaling.

## What the comparison shows

The total is conditional on that supplied policy and its explicit ambiguity choices. It is not a claim about another merchant’s obligations.

## Assumptions and limits

The policy and requests belong to the exercise. A chosen precedence rule is an assumption to inspect, not a statement of consumer law or authorization to issue real refunds.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
