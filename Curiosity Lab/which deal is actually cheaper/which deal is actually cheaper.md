# which deal is actually cheaper

## Research question

Which promotion minimizes checkout cost when the two products have different prices?

Models buy-one-get-one, half-price, and second-item-half-price promotions for equal and unequal item prices. The archive separates pair cost, per-item cost, and the case where only one item is wanted.

## Data and comparison design

Let the lower price be p and the higher q. Under the stated cheaper-item-free rule, compare pair totals q for BOGO, (p+q)/2 for half-price each, and q+p/2 for a half-price second item. Keep pair cost separate from average item cost and the need for only one item.

## Recorded findings

The answer depends on what you mean by “cheaper”:

- For a qualifying two-item pair, **50% off each is never worse than BOGO** under the stated assumptions.
- They are equal only when the two item prices are equal.
- If the prices differ at all, **50% off each is cheaper**.
- **BOGO is always cheaper than “second item half price”** for positive prices.
- If you only wanted one bottle, the promotions are operationally different: 50% off lets you buy one; BOGO and second-item-half require buying two.

Let the cheaper item cost `p`, the pricier item cost `q`, with `0 < p ≤ q`.

| Promotion | Two-item trip cost | Average cost per item |
|---|---:|---:|
| BOGO — cheaper item free | `q` | `q / 2` |
| 50% off each item | `(p + q) / 2` | `(p + q) / 4` |
| Second item half price | `q + p/2` | `q/2 + p/4` |

Break-even in plain language:

- BOGO vs. 50% off each:

  

`q = (p + q) / 2  ⇒  q = p`



  They match only when the two items cost the same. If the pricier item costs even one cent more, 50% off each is cheaper. The trip-cost advantage of 50% off is `(q − p) / 2`, and the per-item advantage is `(q − p) / 4`.

- BOGO vs. second item half price:

  

`q = q + p/2  ⇒  p = 0`



  With any positive-priced item, BOGO is cheaper. “Second item half price” costs exactly `p / 2` more per trip, or `p / 4` more per item, than BOGO.

For a one-bottle purchase:

- Under 50% off each, one bottle costs `p / 2`.
- Under BOGO, you must buy two bottles and pay `q`.
- Under second-item-half-price, you must buy two bottles and pay `q + p/2`.

So if you only wanted one bottle, the 50%-off offer is usually the practical winner even in cases where the two-item unit-price comparison looks close.

Assumptions used:

- Promotions apply to one qualifying pair.
- `p` is the cheaper item and `q` the pricier item.
- No coupons, loyalty points, tax effects, minimum spend, caps, or expiry constraints.
- “BOGO” means the cheaper item is free.
- “50% off” means both items are half price.
- “Second item half price” discounts the cheaper item, since that minimizes the pair cost.
- Per-item cost is the pair total divided by two items.

The table, figure, and assumptions were generated from the same executable model run.

## What the comparison shows

The algebra depends on eligibility and which item receives the discount; it does not describe every retailer’s promotion wording.

## Assumptions and limits

The arithmetic assumes the stated eligibility and cheaper-item rules. Taxes, exclusions, quantity needs, and store-specific terms can change a real purchase comparison.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
