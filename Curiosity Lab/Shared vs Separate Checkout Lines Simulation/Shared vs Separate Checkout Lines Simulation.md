# Shared vs Separate Checkout Lines Simulation

## Research question

Does queue organization change typical waits and the experience of the unluckiest customers?

Simulates shared and separate queues with the same customer arrivals and service times at three counters. The archive compares average waits and the slowest-customer tail under several fictional scenarios.

## Data and comparison design

Feed the same arrivals and service requirements through both three-counter layouts, repeat across fictional workload scenarios, and compare mean waits with the slowest-customer tail. Pairing the customer streams isolates the layout within each simulation.

## Recorded findings

| Queue design or scenario | Recorded mean wait | What is held comparable |
| --- | --- | --- |
| Shared queue, typical case | 4.6 minutes | Same supplied arrivals and service workload. |
| Separate queues, typical case | 5.0 minutes | Customers cannot redistribute perfectly after joining. |
| Slow-customer scenario | Larger contrast in the archive | Uneven service times magnify imbalance between separate lines. |
| Simulation scope | Fictional parameterized store | Not an observed causal estimate for a real shop. |

### The setup
A fictional shop with 3 identical counters. Every customer who walked in was fed through **both** layouts — same arrival times, same personal checkout times — so the only difference is how the lines are organized. The simulation runs 30 independent 8-day "shops" per scenario (~5,000 customers each) and averaged.

### What we learned (plain English)

1. **One shared line is faster — always.** Average wait was 4.6 min vs 5.0 min in the typical case. When I sprinkled in slow customers (3% take ~70 min, like a price check gone wrong), the average rose for everyone, but the shared line still won: 15.3 vs 16.9 min. A busier store (90% busy) widened the gap further.

2. **The shared line is much kinder to the unluckiest customers.** The slowest 10% of customers waited on average 21.7 vs 26.1 min in the typical case — and **78 vs 106 min** with slow customers in the mix. Separate lines punish the people who happened to stand behind a slow customer.

3. **Not a fluke.** Across all 30 runs per scenario, the shared line won on average wait 30/30, 26/30, and 25/30 times (and nearly always on the slowest-10% metric). The few losses were close calls in the harshest scenario.

4. **Why separate lines lose:** stuck-behind-a-slow-customer. If you pick a line and the person ahead of you takes an hour, you're trapped. In one shared line, a slow customer only blocks 1 of 3 counters; the others keep draining the queue. Measured directly: customers arriving during a slow checkout waited ~44 min shared vs ~53 min separate.

5. **The one caveat:** with a single shared line, a slow customer at the front is visible to *everyone*, which nudges up the typical (not extreme) wait — that's why separate lines occasionally win a short head-to-head. It never wins overall.

> **Bottom line:** one line feeding several counters is better — a bit faster on average, much better for the unluckiest, and the advantage grows exactly when it matters (busy store, slow customers). Banks and airport security figured this out long ago.

### Saved for sharing & reuse

One note on process: the chart was regenerated after a QA pass — the first render's footnote clipped outside the figure bounds, caught by the render-then-verify check, then fixed and re-verified clean (no text overlaps, nothing outside the canvas). The mixture sizing formula also got one pre-publication fix so the "slow customers" scenario truly keeps the average checkout at 6 min.

The comparison uses common arrival and service workloads so a queue rule, rather than an easier random draw, explains the simulated difference. Pooling customers lets the next free cashier serve the next waiting person; separate lines can leave one cashier idle while customers remain trapped behind a slow service elsewhere. The slow-customer scenario examines that mechanism. Arrival intensity, service-time variability and cashier count still determine the size of the benefit.

## What the comparison shows

These are simulated layouts, not observed stores. A result on mean waiting time does not fully describe fairness, balking, or service discipline.

## Assumptions and limits

The recorded summaries favor pooling on scenario averages, but some individual runs do not. The conversation's broad claim that one line is always faster should not be interpreted as a universal result.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
