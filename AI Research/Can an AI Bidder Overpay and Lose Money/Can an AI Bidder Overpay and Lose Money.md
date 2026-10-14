# Can an AI Bidder Overpay and Lose Money

## Research question

Does a bidder respect its private valuation when the current price makes winning unprofitable?

Runs a small English-auction exercise and inspects bids, valuations, winners, and profits. The archive examines both final outcomes and individual bidding decisions for overpayment.

## Data and comparison design

Inspect every bid decision as well as completed-auction outcomes. Count opportunities above valuation, track budgets, preserve no-sale auctions, and compare the winner’s payment with its own value. A low loss count is more interpretable if the policy actually faced opportunities to overbid.

## Recorded findings

**In this design, no — the AI never overpaid, and never even came close.** Across 20 completed English auctions, 14 produced a winner. **Zero** paid above their own valuation. Mean winner profit **+$16.36**, median +$16.50, minimum **+$5**. The loss region was never entered.

| Competition | Auctions | Winners | No sale | Mean profit | Min profit | Overpaid |
|---|---|---|---|---|---|---|
| 2 bidders | 8 | 5 | 3 | +$17.60 | +$5 | **0** |
| 3 bidders | 8 | 6 | 2 | +$17.67 | +$7 | **0** |
| 5 bidders | 4 | 3 | 1 | +$11.67 | +$6 | **0** |

Allocative efficiency was **100%** — the highest-valuation bidder won every auction.

### The strongest evidence isn't the wins

"0 of 14 winners overpaid" is a weak claim; 14 auctions is a small sample. The tighter test is **every decision, not just the winning ones**:

- **43 times**, a bidder was asked to pay a price **above its own valuation** → said yes **0 times**
- **372 times** at or below valuation → declined only **3 times**

That second bullet matters: the model doesn't just avoid losing money, it barely leaves money on the table either. It is not bidding cautiously-then-getting-lucky; it is applying the correct rule.

Because the model said yes in 0 of 43 above-value opportunities, the 95% upper bound on its overbid rate is ~**7%** — a far tighter bound than the 14-auction sample gives.

Two framing checks from the original question: budgets were **never** the constraint (0 of 415 decisions hit a budget cap), so "even though its budget allows it" was genuinely tested. And the no-sale auctions aren't losses — nobody bought.

### The honest caveat: this design can't really produce the failure you asked about

I need to be direct about this, because it limits what the result means.

A **private-value** auction with a known own valuation and an explicitly stated payoff has no uncertainty in it. The dominant strategy is trivially "bid to the supplied private valuation," and there's no mechanism to generate an overpay except a reasoning error. **The winner's curse — the actual mechanism behind real overpayment — requires common value and noisy estimates, which this design structurally excludes.** So a competent reasoner *should* score 0 here, and the result is closer to a sanity check than a discovery.

It's also a best case for a second reason: my prompt stated the payoff outright ("profit is exactly V − P", "the item has no value beyond its resale value"). Real procurement doesn't hand you that.

What this does establish: claude-sonnet-5 does not botch a well-specified ascending auction, at any of the three competition levels, across 415 decisions.

### Limitations

- **n=14 winners**; level 5 got only 4 of 8 auctions — the run was interrupted (see below)
- Session `host.llm` **failed transiently** early on and recovered; inference is not dependable here
- The run was killed mid-flight — *"Notebook process tree could not be stopped"* — which has left the JS control kernel wedged and blocking further background experiments until it clears
- Tool permission calls failed intermittently throughout

### To actually answer the stated question

The test that bites is a **common-value auction**: bidders see only a noisy private signal of a shared, unknown value. That reintroduces estimation error, and the winner becomes the bidder whose signal was most optimistic — the mechanism that makes real AI bidders lose money. A cheap addition: **remove the explicit payoff statement** from the prompt, so the model must infer that bidding above value is unprofitable.

I'd suggest the common-value run next; it's the version where a null result would be genuinely surprising. Want me to build it? I'd also top up level 5 to 8 reps for a balanced design — worth doing whether or not you want the common-value variant.

## What the comparison shows

These observations describe a small prompted auction design. They do not establish economic rationality across formats, strategic opponents, or uncertain valuations.

## Assumptions and limits

The finite scenario and decision constraints matter more than a broad claim about AI bidding. No overpayment in the recorded sample does not rule out losses in other auction designs.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
