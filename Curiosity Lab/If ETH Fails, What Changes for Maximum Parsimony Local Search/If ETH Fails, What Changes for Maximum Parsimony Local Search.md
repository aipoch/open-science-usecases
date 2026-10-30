# If ETH Fails, What Changes for Maximum Parsimony Local Search?

## The question

What happens to a computational lower bound when the assumption supporting it is removed? This case follows that question through a concrete phylogenetics problem: finding a nearby tree that explains observed character states with fewer changes.

The archived investigation reads the CPM 2023 paper *On the Complexity of Parameterized Local Search for the Maximum Parsimony Problem*, checks a synthetic four-taxon example, and separates three kinds of statement: a published hardness classification, a conditional runtime exclusion, and an algorithm that can actually be run. Its answer is precise: **if ETH were false, the ETH-based exclusion would lose its premise. That would neither erase the hardness classifications nor supply a faster local-search algorithm.**

The case treats ETH being false as a hypothetical. It does not verify the external SAT proof claim discussed in the session.

## What the problem asks

The starting input contains an unrooted binary phylogenetic tree, fixed taxa and character observations, and a radius limiting how far the topology may change. A character assigns an observed state to each leaf; its parsimony score is the smallest number of state-changing edges possible after assigning states to the internal vertices. Scores add across characters.

| Object | Meaning in this case | Why it matters |
|---|---|---|
| Taxa X | The observed leaves | They remain fixed while topology changes. |
| Character sequence S | Observed states across the leaves | It determines the score being minimized. |
| Starting tree T | The topology being improved | Local search starts here, rather than searching without a reference tree. |
| Radius k | The allowed neighborhood budget | Its meaning depends on the chosen tree operation. |
| Input size I | The complete encoded input | It must not be silently equated with the number of taxa. |
| Success | A tree within the radius with a strictly lower score | A nearby tree with an equal score does not satisfy the decision problem. |

Fixed-tree scoring, local improvement, and globally optimal tree inference are different tasks. A fast scoring routine does not by itself solve the topology search.

## Neighborhoods change the question

| Neighborhood | Allowed operation | What k counts |
|---|---|---|
| NNI | Nearest-neighbor interchanges around internal edges | Successive moves |
| ECR | Contract selected internal edges, then choose a binary refinement | Contracted edges; selections may be separated |
| sECR | Contract and refine a connected internal region | Contracted edges forming a connected subtree |
| SPR / TBR | Subtree prune-and-regraft / tree bisection-and-reconnection | Successive moves under the corresponding distance |

The connected-region restriction is essential: the paper's fixed-parameter algorithm for sECR cannot simply be assigned to unrestricted ECR. The four-taxon example has only one internal edge, so its radius-one NNI, ECR, and sECR neighborhoods coincide; it cannot demonstrate their larger-tree differences.

## A small calculation makes the score tangible

The session uses synthetic binary observations, unit character weights, and a cost of one for each changing edge:

| Taxon | Character 1 | Character 2 | Character 3 |
|---|---:|---:|---:|
| A | 0 | 0 | 0 |
| B | 0 | 0 | 1 |
| C | 1 | 0 | 0 |
| D | 1 | 1 | 0 |

The starting split is AC∣BD. The archived calculation applies Fitch scoring and independently enumerates all four assignments to the two internal binary states, for each character and topology.

| Topology | Character 1 | Character 2 | Character 3 | Total |
|---|---:|---:|---:|---:|
| AC∣BD: starting tree | 2 | 1 | 1 | **4** |
| AB∣CD: alternative | 1 | 1 | 1 | **3** |
| AD∣BC: alternative | 2 | 1 | 1 | **4** |

The two methods agree on nine minimum scores across 36 enumerated internal-state assignments. AB∣CD is therefore a strictly better neighbor. This is a finite check of the scoring example, not a runtime benchmark, biological finding, or proof of a complexity theorem.

## Exactly what would change if ETH were false

The session examines Theorem 4.1 for NNI, ECR, SPR, and TBR, including its binary-character restriction. The following distinctions prevent a removed assumption from being mistaken for a constructive breakthrough.

| Statement examined | Status under the ETH-false hypothetical | What still cannot be concluded |
|---|---|---|
| NP-completeness | The classification remains | A polynomial-time exclusion needs a separate class-separation assumption. |
| W[1]-hardness in radius k | The classification remains | ETH being false does not settle FPT versus W[1]. |
| Under ETH, no `f(k) × size(I)^{o(k)}` solver | The conditional theorem remains; its premise is absent | Neither existence nor nonexistence of that faster solver follows from this implication alone. |
| The published reductions | Their direction and constructions remain | An easier source problem does not reverse the reduction. |
| Existing constructive upper bounds | They remain available | Their practical speed is not measured by the theorem. |

Here `f(k)` is an arbitrary computable function of the radius, and `o(k)` denotes an exponent sublinear in k. A smaller constant multiplying a linear exponent is a different claim.

The archived source analysis traces a reduction from Clique with parameter q to local search: k equals q for SPR/TBR and 2q for NNI/ECR. A fast target solver would solve the constructed Clique instance. This transfer direction is why a hypothetical improvement in SAT does not automatically become a parameter-efficient tree-search algorithm.

## Algorithms that remain available

| Published result | Scope | Runtime form | Practical reading |
|---|---|---|---|
| Theorem 5.4 | Connected-contraction sECR | `2^{O(k log k)} × n² × m` | Fixed-parameter tractable in k; the connected restriction must be retained. |
| Theorem 5.6 | NNI, SPR, TBR, unrestricted ECR | `n^{O(k)} × m` | Polynomial for fixed k, with a k-dependent exponent. |

Here n is the number of taxa, m is the number of characters, and `size(I)` above is the total encoded input size. These algorithms do not depend on ETH. Their inputs use the paper's unordered-parsimony model; the constructive results do not require every character to be binary.

A possible route through SAT would need an explicit encoding of valid candidate trees, neighborhood distance, and score improvement. It would then need bounds on SAT variables, encoded bits, and translation overhead. Polynomial-size reducibility alone does not establish a runtime advantage over the parameterized algorithms above. The session constructs no competitive SAT encoding and reports no phylogenetics software speedup.

## What the archive contains and what remains open

| Archived material | Role |
|---|---|
| `maximum-parsimony-eth-report.md` | Detailed source reading, hypothetical analysis, and conclusions |
| `audit.md` and source-version notes | Qualification and source-location record |
| Audited score and enumeration CSVs | The finite quartet calculation |
| Quartet-scoring and map-generation Python files | Recorded calculation and explanatory-figure code |
| Original and revised explanatory figures | Separate views of definitions, theorem assumptions, reductions, and algorithmic implications |

The session checked focused passages in the supplied proceedings version. Some proofs are explicitly deferred in that version; it did not obtain and verify every deferred proof. Its external SAT-page reading used mutable main, while a repository HEAD was observed separately; an exact pinned-content match was not established. No Lean verification, comprehensive current-literature survey, realistic-data benchmark, or new faster local-search algorithm is claimed.

For someone evaluating a proposed algorithmic breakthrough, the useful next step is to identify which premise has changed, then demand a concrete algorithm and parameter-sensitive runtime analysis. A removed lower-bound premise creates a research question; it does not answer that question.

## Sources and provenance

The principal published source is Komusiewicz, Linz, Morawietz, and Schestag, [*On the Complexity of Parameterized Local Search for the Maximum Parsimony Problem*, CPM 2023](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CPM.2023.18). The archived discussion also records an [external SAT statement](https://github.com/openai/math/blob/main/lean/docs/378.md), treated as a reported claim rather than a verified proof.

This introduction was prepared from the supplied AIPOCH Open-Science session and its final report. The original native export, its conversation, artifacts, and evidence records are preserved; publication changes only its external filename to replace spaces with hyphens. Preparing this page did not rerun the research or independently verify its proofs.
