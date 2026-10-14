# Revised AI Papers - Did the Main Claim Change

## Research question

Which revision changes the mathematical claim rather than just its presentation?

Compares available versions of mathematics papers at pinned repository commits, focusing on assumptions, conclusions, gaps, and supporting files. The final record verifies supplied file hashes and preserves exact diffs.

## Data and comparison design

Pin both source versions, verify their supplied identities, and compare assumptions, conclusions, proof gaps, and implementation dependencies. An exact text diff locates a change; a separate mathematical reading explains its significance.

## Recorded findings

| Selected paper | Headline theorem | Substantive or supporting change |
| --- | --- | --- |
| Taming implies compatibility | Unchanged | Cone equality gains an extra hypothesis and a four-torus counterexample. |
| Incompressible Box Transport | Unchanged | Derivative requirements and effective analytic bounds become explicit. |
| BSD comparison | Unchanged in supplied mathematical sections | Introductory citation removal and newer companion editions; those editions are outside this archive. |
| Older-file provenance | 45 Git blob identities match | 12 Taming, 19 Box Transport and 14 BSD files. |

**In these three selected pairs, the main theorem statements remain unchanged—but the revisions are not all merely wording edits.** One retracts the generality of a subsidiary result; another repairs supporting analytic estimates; the third cleans up citations while changing which companion editions are referenced.

| Paper | Versions compared | Main result | Other changes |
|---|---|---|---|
| Taming implies compatibility | Sept. 23 → Oct. 6, 2026 | Existence theorem unchanged | Cone equality restricted; new characterization and counterexample |
| Incompressible Box Transport | Sept. 27 → Oct. 6, 2026 | Principal geometric and computational theorems unchanged | Projection proposition and clock proof substantially revised |
| Exact BSD from Low Selmer Corank | Oct. 3 → Oct. 7, 2026 | Assumptions and formula unchanged | Obsolete citation removed; companion references updated |

I compared all supplied source files and cross-checked key passages against the PDFs. All **91 manifest-listed paper files** match their supplied byte lengths, SHA-256 hashes, and Git blob hashes. This verifies the archive against its manifest; it is not an independent live verification against GitHub.

Both dated versions of every pair are pinned at [`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`](https://github.com/openai/math/commit/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb). The supplied history records initial commit [`adc7f1241b42e322a6451854ab7e4b4c146bf78a`](https://github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a), update commit [`301488868beec11bfd897168433b0a64f5258559`](https://github.com/openai/math/commit/301488868beec11bfd897168433b0a64f5258559), and that merge. The comparisons below use the retained snapshots at the merge, not reconstructed earlier checkouts.

**1. Taming: unchanged main theorem, substantively weaker cone-equality claim**

The main theorem is byte-identical in both versions, on PDF page 1:

> “Suppose that a smooth almost complex structure `J` on a closed connected smooth real four-manifold `X` is tamed by a symplectic form. Then there is a smooth symplectic form compatible with `J`.”

Both also explicitly say:

> “The conclusion imposes no condition on the cohomology class of the compatible form.”

The substantial correction concerns a **subsidiary cohomological claim**.

Before, Corollary 1.2 asserts, under the main theorem’s hypotheses:



`𝒦_Jᵗ = 𝒦_Jᶜ + H_J⁻`


Its short proof says:

> “Li and Zhang's four-dimensional cone comparison … therefore gives the cone identity…”

After, the equality appears in a corollary with an additional hypothesis:



`If h_J⁻ = b₂⁺(X) − 1, then`  
`𝒦_Jᵗ = 𝒦_Jᶜ + H_J⁻.`


Sources: [before introduction, lines 34–63](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Taming-implies-compatibility-on-four-manifolds-September-23-2026/build/sections/01-introduction.tex#L34) and [after introduction, lines 34–78](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Taming-implies-compatibility-on-four-manifolds-October-6-2026/build/sections/01-introduction.tex#L34).

The revision also introduces a new cone-characterization theorem. With
`𝒱 = (H_J⁻)⊥` and `𝒞 = 𝒦_Jᵗ ∩ 𝒱`, it asserts



`𝒦_Jᵗ = 𝒞 + H_J⁻`  
`𝒦_Jᶜ = {a ∈ 𝒞 : a · y > 0 for every nonzero y ∈ closure(𝒞)}`



This is accompanied by a new section, `08-cones.tex`, containing prescribed-class separation, current estimates, proofs, and an explicit four-torus example. The example states:

> “The closed forms `U ± V₀` have invariant projections `(1 ± f)F / r`, so both tame `J`. Their classes pair to zero, since `U² = V₀²`. Neither class can have a compatible representative, which would wedge strictly positively with a tamer in the other class.”

It concludes:



`𝒦_Jᶜ + H_J⁻ = 𝒦_Jᶜ ⊊ 𝒦_Jᵗ`


[New example, source lines 375–418](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Taming-implies-compatibility-on-four-manifolds-October-6-2026/build/sections/08-cones.tex#L375), PDF page 22.

**Assessment:** This is a substantive correction to the scope of a subsidiary result, not a stylistic clarification. The revision itself supplies a counterexample to the former unrestricted equality. The `b₂⁺ = 1` consequence remains. The main existence theorem and source sections 2–7 remain unchanged.

The supporting-file changes reinforce that distinction: a new proof section and example environment are added; the abstract advertises the cone characterization; a companion citation is updated. Separately, the introduction shortens its discussion of difficulties in earlier authors’ arguments. That is a change in exposition of prior work, not a repair to the unchanged existence proof.

**2. Box Transport: unchanged headline claims, substantive revision of estimates**

The principal routing theorem retains its assumptions: rational solid boxes, each family pairwise disjoint, positive diagonal scale factors with product one. Its conclusion remains an effective, compactly supported smooth solenoidal field realizing the prescribed affine maps near the boxes.

The computational theorem likewise retains this exact conclusion in both versions:



`There exists t ≥ 0 such that X(t; x*) ∈ (−1, 2)³`  
`if and only if the machine halts.`


The entire files `geometry.tex` and `balanced.tex`, containing these theorems and proofs, are byte-identical.

The changed statement is **Proposition 2.4, projection on a flat torus**. Before:

> “Uniform mixed-derivative bounds, temporal `L²` bounds of their spatial suprema, and separately imposed time periodicity, eventual stationarity, or orderwise decay bounds are preserved.”

After:

> “A quantitative envelope for time order `h` and output spatial order `r` passes to `Pg, Qg` through order `r` and to `φ` through order `r + 1` when the input derivatives through spatial order `r + 2` satisfy that envelope. The constants may depend on the derivative order.”

Sources: [before `analysis.tex`, line 164 onward](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Incompressible-Box-Transport-and-Finite-Computation-September-27-2026/build/analysis.tex#L164) and [after](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Incompressible-Box-Transport-and-Finite-Computation-October-6-2026/build/analysis.tex#L164), PDF page 6 in both.

The revised proposition supplies explicit estimates:



`max{‖∂ₜ^h(Pg)‖_{C^r}, ‖∂ₜ^h(Qg)‖_{C^r}} ≤ S_L × ‖∂ₜ^h(g)‖_{H^(r+2)}`




`‖∂ₜ^h(φ)‖_{C^(r+1)} ≤ S_L × d_L × ‖∂ₜ^h(g)‖_{H^(r+2)}`



It also explicitly requires computable `L`, effective evaluation, and supplied derivative bounds for its effectiveness conclusions. The proof adds Fourier-tail and quadrature estimates.

This matters because the old proof already controlled an output derivative using **higher input derivatives**, but its blanket “orderwise decay” wording did not spell out the required relationship between their decay envelopes.

The clock proof changes accordingly. Before:

> “This proves all the asserted bounded and temporal `L²` norms. The two profiles are separate choices. Torus projection may be applied to either with its corresponding changed pressure…”

After, it explicitly establishes:



`‖∂ₜ^h(U_(α₁)(t))‖_{C^r} + ‖∂ₜ^h(f_(α₁)(t))‖_{C^r}`  
`≤ C_(h,r) × (1 + t)^(−1−h).`


The new explanation says:

> “The exponent is common to all spatial orders, and the square of the envelope has integral `(1 + 2h)⁻¹`.”

It then applies the projection bounds through input spatial order `r + 2`, obtaining the same decay rate for projected force and pressure.

Sources: [before `clocks.tex`, line 115 onward](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Incompressible-Box-Transport-and-Finite-Computation-September-27-2026/build/clocks.tex#L115) and [after](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Incompressible-Box-Transport-and-Finite-Computation-October-6-2026/build/clocks.tex#L115).

## What the comparison shows

A verified file identity does not validate a theorem. Historical provenance supplied with an archive also differs from independently retrieving every source version.

## Assumptions and limits

Verified bytes and supplied historical provenance are separate evidence. A wording or theorem change does not by itself prove correctness, and papers without visible revisions are not thereby validated.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
