# AI Math Counterexample - Does Exact Arithmetic Agree

## Research question

Can a small explicit construction be independently checked without relying on approximate numerical agreement?

Records an exact-arithmetic check of an explicit product-of-simplices construction from a pinned mathematics repository. The archived calculation reconstructs vertices and facets and compares independent determinant calculations with the stated claim.

## Data and comparison design

The check reconstructs the product of two ten-dimensional simplices from its integer vertices and facets. Compute the determinant quantities with two exact algorithms, then independently calculate the simplex benchmark. This reduces one explicit claim to finite, reproducible arithmetic under stated geometric identities.

## Recorded findings

| Verification component | Recorded result | Role in the check |
| --- | --- | --- |
| Product construction | Two ten-dimensional simplices; 121 vertices and 22 facets | Defines the finite geometric object. |
| Determinant workload | 231 maximal determinant calculations | Makes the arithmetic check inspectable. |
| Independent arithmetic | Two exact determinant algorithms agree | Avoids floating-point agreement being mistaken for exact equality. |
| Comparison ratio | 5,588,869 / 5,505,024 ≈ 1.01523 | The explicit construction exceeds the stated benchmark by about 1.523%. |

**Yes—the explicit construction survives exact arithmetic.**

At commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`, Theorem 1 takes `K = T₁₀ × T₁₀`, where `T₁₀ = conv(0, e₁, …, e₁₀)`, and claims


`R₂₀(K) / c₂₀ = 22,355,476 / 22,020,096 > 1`



I reconstructed its **121 integer vertices and 22 facets**, calculated facet areas, and evaluated all **231 maximal determinants** defining its projection-body volume. I separately computed the 20-simplex benchmark, without assuming the paper’s product formula.

The exact result agrees:


`R₂₀(K) / R₂₀(T₂₀) = 5,588,869 / 5,505,024 > 1`


an excess of approximately **1.523%**. Two exact determinant algorithms agreed, and a standalone rerun reproduced identical outputs.

The check assumes the standard simplex-volume, orthogonal-product measure, facet-pyramid, Cauchy projection, and zonotope-volume identities. It verifies this construction under those identities—not the entire paper. Source hashes matched both supplied snapshots.

## What the comparison shows

The check supports this construction under its listed identities. It is neither a formal proof of every intermediate identity nor a validation of the entire paper.

## Assumptions and limits

The check covers this finite construction under named mathematical identities, not the whole paper or every proof. The source snapshots and exact calculation files are retained in the package.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
