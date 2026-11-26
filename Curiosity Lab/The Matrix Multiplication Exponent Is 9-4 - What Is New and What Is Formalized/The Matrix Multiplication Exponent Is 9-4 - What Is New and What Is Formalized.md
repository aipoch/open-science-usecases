A headline that the matrix multiplication exponent equals 9/4 raises several different questions: which bound is new, what computational model is being discussed, and what does the accompanying Lean source actually cover? This case compares a paper edition, release documentation, a shared formalization scope and theorem declarations. It audits documentary correspondence; it does not independently prove the theorem, compile Lean or measure a practical speedup.

## Research question and source edition

The final review uses the supplied 111-page paper dated **24 November 2026**, together with attachments identified by OpenAI Math commit `3344da59991ed94f9ba711217b29c1d760badfa6`. The hotspot database date, 26 November, is distinct from the paper edition date.

The paper was added in a follow-up. An earlier audit correctly recorded that its initial inputs did not include the PDF. The final report supplements that earlier state rather than rewriting it as though the paper had always been available.

| Source | Role in this case | Verification boundary |
|---|---|---|
| Attached paper PDF | Theorem, model definitions, corollaries and prior-work attribution | 111 pages and a recorded hash; selected passages and bibliography entries inspected, not a complete proof review |
| Release README | Publisher's headline and description of Lean coverage | Does not itself contain the earlier upper-bound attribution that an initial operator note assigned to it |
| Shared scope document | Scope stated for a formalization accompanying four papers | Not automatically the scope of this single paper |
| `ExactExponent.lean` attachments | Square, dual and rectangular theorem declarations | Source text inspected; imported definitions and bridges were not fully checked or built |
| Operator-prepared claim register and brief | Starting questions and source locations | Their attributions require checking against primary sources |

The final archive preserves original and commit-labelled attachments. The Lean attachment pair is byte-identical; the README and scope pairs differ. Commit-pinned links provide provenance locators, but the archived investigation did not fetch and authenticate every remote byte at that commit.

## What the paper claims is new

The publisher presents the square exponent equality over every field. The reviewed paper attributes an upper bound of 9/4 to earlier work and claims a matching lower bound within its defined formal arithmetic-circuit model. Those are different contributions: the headline equality should not be paraphrased as this paper first discovering both directions.

| Statement | Attribution in the retained review | What the case establishes |
|---|---|---|
| Square exponent `omega_F = 9/4` | Paper Theorem 1.1, page 1 | The paper states the equality; its mathematical proof was not independently validated here. |
| Earlier upper bound | Paper introduction and Section 1.5, page 5, with cited prior works | The attribution is supported by the newly inspected paper, rather than by the original uploaded README. |
| Matching lower bound | Claimed contribution of this paper for its circuit model | A publisher statement with model qualifications, not a new proof produced by this case |
| Dual exponent and rectangular claims | Paper corollaries versus a broader shared formalization | Different statement strengths and objects must remain separate. |

The cited earlier papers were identified through this paper's bibliography. They were not independently reviewed as complete works in this session.

## Which computational model is meant?

The paper's definition uses independent matrix-entry variables, constants in a field F, and scalar addition, subtraction, multiplication and division by a nonzero rational function. Outputs must be rational-function identities, including over finite fields. Agreement on a finite collection of evaluated inputs does not replace that identity requirement.

The exponent and the finite-size gate lower bound also count different things. The exponent concerns asymptotic scalar-operation complexity. The stated finite-size corollary counts nonscalar multiplication or division gates and may treat linear operations as free.

For integer matrix side length `n >= 2`, the paper states a bound of `ceil(n^(9/4) / 2)` on those nonscalar gates. That is not a wall-clock lower bound, a memory-use estimate or a statement that every category of instruction has the same cost.

## Paper statement versus Lean scope

The attached Lean file declares a square-exponent equality, a dual-exponent equality and a weighted rectangular-exponent formula. Its proof terms invoke imported results. Reading those declarations does not establish that the complete project compiles with its pinned toolchain and dependencies.

| Dimension | Paper description | Shared scope / Lean source | Retained conclusion |
|---|---|---|---|
| Fields | Every field F | Field type assumptions in the declarations | Textual agreement; a semantic bridge is not verified. |
| Operations | Formal arithmetic circuits allowing qualified division | Division-free programs counting addition, subtraction and multiplication | Different descriptions; model equivalence is not established by the attached file alone. |
| Exponent | Infimum of powers permitting the stated asymptotic scalar-operation bound | Imported `formalOmega` definition | Similar headline notation does not substitute for checking definitions. |
| Square claim | Equality combining attributed upper and claimed lower bounds | `square_exponent` declares `formalOmega F 1 1 1 = 9/4` | Statement correspondence at the headline level, not verified proof correspondence |
| Finite-size gate count | A quantified nonscalar-gate corollary for `n >= 2` | No corresponding finite-size theorem in this attached file | Coverage remains unestablished. |
| Dual exponent | An interval from 1/2 to 2/3 under the paper's definition | `dual_exponent` declares `formalAlpha F = 1/2` | A stronger numerical claim with definition/domain questions still open |
| Rectangular case | Rank lower bounds for positive integer side parameters | An exact formula using real weights, clamping and sorting | Different quantities, domains and strengths; do not attribute the whole exact formula to this one paper. |
| Coverage | This paper's theorem and corollaries | Scope document explicitly accompanies four papers | Not evidence that every statement of this paper has been formalized |

The rectangular declaration also has boundary conventions involving Lean's totalized division. A formula copied into ordinary arithmetic without those conventions can lose its intended meaning. This is another reason to inspect definitions rather than treating a displayed formula as a complete translation.

## What an exponent of 9/4 would mean

Under the paper's infimum definition, the equality supports an asymptotic statement of the form `O(n^(9/4 + epsilon))` for each positive epsilon, with the relevant constants allowed to depend on the field and epsilon. It does not by itself promise an algorithm attaining exactly `O(n^(9/4))` with a useful implementation constant.

The growth exponent describes arithmetic complexity as matrix size increases. It does not determine elapsed time on a GPU or CPU, bit costs, memory traffic, communication costs or the practical crossover point against another implementation. No runtime benchmark was performed in this case.

## Evidence map and reproducibility

The saved evidence map connects paper claims, source documents and formal declarations through explicit source locations. Its edges represent documentary attribution and statement correspondence, not inferred proof dependencies.

| Label | Meaning in the retained audit |
|---|---|
| Stated | A paper or document makes the claim. |
| Formally declared | A Lean theorem declaration appears in inspected source. |
| Source inspected | The relevant source passage was read. |
| Compiled / verified: not checked | No successful Lean build was established. |

The final self-contained ZIP contains 38 files. Its recorded fresh-process rebuild checks ten input hashes and five output hashes; the final report, claim register, scope table and evidence-map outputs match their retained versions. Editorial source-location tables and a report template are declared inputs to that documentary rebuild. Rebuilding them is not an independent derivation of the mathematical claims.

Publication preparation checked the package inventory, declared evidence references, ZIP checksums and agreement between the standalone final files and their bundled copies. It did not rerun the archived rebuild script, reproduce the proof or compile Lean.

## Assumptions and limits

The unresolved questions include equivalence between the paper's division-allowing model and the shared division-free formalization, the meanings of imported exponent definitions, and coverage of finite-size and rectangular statements. No full-paper proof review, independent mathematical validation, external peer-review determination or successful project build is established.

The useful outcome is a precise account of which source supports which claim, including the historical correction of an unsupported README attribution. It keeps a publisher's theorem claim, inspected formal source and an executed proof-assistant build as distinct evidence states.

## Sources and retained materials

- [Paper at the supplied commit](https://github.com/openai/math/blob/3344da59991ed94f9ba711217b29c1d760badfa6/preprints/The-matrix-multiplication-exponent-is-nine-fourths-November-24-2026/paper.pdf) — Theorem 1.1 and definition on page 1, corollaries on page 2, attribution in Section 1.5 on page 5.
- [Release README](https://github.com/openai/math/blob/3344da59991ed94f9ba711217b29c1d760badfa6/preprints/The-matrix-multiplication-exponent-is-nine-fourths-November-24-2026/README.md) — publisher framing and formalization links.
- [Shared formalization scope](https://github.com/openai/math/blob/3344da59991ed94f9ba711217b29c1d760badfa6/lean/docs/107.md) — four-paper scope and model description.
- [ExactExponent.lean](https://github.com/openai/math/blob/3344da59991ed94f9ba711217b29c1d760badfa6/lean/OAI/LinearAlgebra/SpectralBooks/ExactExponent.lean) — square, dual and rectangular declarations.

The native AIPOCH Open-Science export preserves the original investigation and follow-up. Its outer publication filename is normalized without changing internal bytes. The cover is an illustration of source inspection, not evidence of mathematical validity.
