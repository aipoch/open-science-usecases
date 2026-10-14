# AI Math Papers - Can You Check the Proofs

## Research question

What proof materials accompany a sampled research family, and which main claims do they actually cover?

Samples distinct research families from a fixed mathematics repository and inventories written proofs, Lean targets, implementation files, and dependencies. Supplementary files close some entry-module gaps in the recorded audit.

## Data and comparison design

The repository is pinned and distinct research families are sampled rather than counting nearby revisions as separate papers. The inventory distinguishes written proofs, challenge statements, selected Lean declarations, solution modules and dependencies. Each item is assessed for availability, statement coverage and checker execution separately. Supplied supplements are reconciled with the same fixed sample before the final coverage counts are updated.

## Recorded findings

| Material class | Papers in final supplied sample | Remaining boundary |
| --- | --- | --- |
| Main-result Lean targets | 11 | Statement-to-target coverage was inspected; compilation was not run. |
| Supporting or partial targets | 4 | Some targets cover narrower claims than the main theorem. |
| No linked Lean material found | 5 | Absence in this supplied sample does not prove absence elsewhere. |
| Written proof material | 20 of 20 | Inspectable manuscript material is distinct from a machine-checked proof. |

**All 20 papers have inspectable written proof material. Of these, 11 have Lean targets covering the main result, 4 have supporting or partial targets only, and 5 have no linked Lean material found. No proof checker was run.**

The archive retains the original sample—seed `20261008`, one first-listed paper per selected family—at commit [`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb). All 311 supplied records passed their size and SHA-256 checks; 287 also matched the earlier catalogue’s Git blob hashes.

“Main-result coverage” below means correspondence between the inspected paper statement, scope note, and Lean target. It **does not mean a successfully checked proof**.

All rows have PDFs and TeX proof material. Links point to the pinned scope notes; the report and CSV contain exact paper-statement and Comparator links.

| Family / selected paper | Lean coverage | Evidence from inspected contents |
|---|---|---|
| [015 — Prime-degree torus packets](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/015.md) | **Main** | Haar convergence and tightness for prime degree ≥5, with arbitrary local types. |
| [024 — Number of totients](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/024.md) | **Main** | Explicit asymptotic equivalent and `V(cx) / V(x) → c`. |
| 046 — Fourfold with non-Stein universal cover | None found | Written theorem and proof; no linked Lean material. |
| 065 — Virasoro constraints under projectivization | None found | Written theorem and proof; no linked Lean material. |
| [082 — Annular variation](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/082.md) | **Partial** | Maximal truncation bound; not the paper’s full `r`-variation theorem. |
| [113 — Perfect-matching FPRAS](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/113.md) | **Main** | Approximation guarantee, polynomial worst-case runtime, and exact zero output. |
| [115 — Exact contingency-table sampling](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/115.md) | **Main** | Exact uniform sampling, almost-sure termination, and polynomial expected bit time. |
| [127 — Polynomial-threshold sensitivity](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/127.md) | **Main** | `8d√n` bound, including the convention `sign(0) = 1`. |
| [148 — Self-similar measure dimension](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/148.md) | **Main** | Entropy-rate dimension formula, allowing exact overlaps and signed unequal ratios. |
| 154 — Multiple ergodic averages | None found | Written theorem and proof; no linked Lean material. |
| 164 — Monochromatic sums and products | None found | Written theorem and proof; no linked Lean material. |
| [192 — Square-root degree counterexamples](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/192.md) | **Main** | Unbounded violations of the claimed Fourier-degree bound. |
| [210 — Sixth-power Foulkes conjecture](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/210.md) | **Partial** | Target covers `b ≥ 30`; paper claims every `b ≥ 6`. |
| [215 — O(3) continuum limit](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/215.md) | **Supporting** | Finite-volume exponential decay; not the canonical continuum-limit construction. |
| [230 — Exact Hausdorff gauge for SLE](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/230.md) | **Supporting** | Positivity only; no finite-measure upper bound or finite-expectation conclusion. |
| [245 — Pure type-system normalization](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/245.md) | **Main** | Weak normalization implies strong normalization, including nonfunctional rules. |
| [296 — Finite-factor generation](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/296.md) | **Main** | Single-generation target plus a separate dense relative-generation target. |
| 351 — Ricci-flow curvature blowup | None found | Written theorem and proof; no linked Lean material. |
| [369 — Strict hot spots](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/369.md) | **Main** | Nonvanishing interior gradient and strict boundary-extrema inequalities. |
| [372 — Isotropic elasticity uniqueness](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/372.md) | **Main*** | Lamé-modulus uniqueness with the stated smoothness and positivity assumptions. |

\*The elasticity target uses a variational trace quotient; equivalence to the paper’s Sobolev boundary-space presentation was not independently proved.

**Files, instructions, and execution remain separate findings.** The Comparator challenge files contain `sorry` placeholders and specify separate solution modules. Nine implementation entry files were supplied, but dependencies are missing; this is not a complete build environment. Their presence cannot establish successful verification.

Also, **19 manuscript READMEs contain citation information only**. The Foulkes README supplies computational verification commands, distinguishing an expected-data check from actually compiling and running the C++ computations. Neither mode was executed. All 20 checker statuses are therefore **“not run,” not “failed.”**

The final supplied sample contains 20 paper families: 11 with main-result Lean targets, four with supporting or partial targets, and five without linked Lean material found. The supplemented materials support this final coverage classification. The supplement supplies the named solution modules for all 23 Comparator configurations and 15 added files with matched size/hash checks. Static inspection of 24 implementation files finds no implementation placeholders outside comments and strings, but four auxiliary declaration bodies and 270 distinct direct OAI imports remain unavailable. Thus the materials support a more detailed coverage audit while every checker-execution status remains “not run.”

## What the comparison shows

This is an inspectability audit. Absence from a partial catalogue is not proof that a formalization does not exist elsewhere.

## Assumptions and limits

No proof checker was run. Static inspection and file availability do not establish proof validity; missing auxiliary bodies and imports remain evidence gaps rather than demonstrated defects.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
