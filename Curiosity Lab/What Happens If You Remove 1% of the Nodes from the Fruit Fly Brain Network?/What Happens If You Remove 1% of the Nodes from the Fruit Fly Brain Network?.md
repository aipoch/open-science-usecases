# What Happens If You Remove 1% of the Nodes from the Fruit Fly Brain Network?

## Research question

Is losing a random neuron structurally equivalent to losing a highly connected hub?

Compares random node deletion with hub-targeted deletion in a 5,000-neuron high-strength subgraph from the FlyWire v783 archive. The archived analysis uses 100 repetitions per strategy with 50 nodes removed per repetition, and records connectivity metrics and reproducibility artifacts.

## Data and comparison design

Hold the 5,000-node high-strength subgraph fixed, delete 50 nodes per repetition, and compare random removal with hub-targeted removal over 100 repetitions per strategy. Track edges, weak and strong components, reciprocity, and matched-source efficiency separately.

## Recorded findings

| Removal design | Recorded structural interpretation | Boundary |
| --- | --- | --- |
| Random removal | Relatively little disruption in the saved discussion | Depends on the graph and metric definitions. |
| Hub-targeted removal | Greater disruption than random deletion | Tests concentration of structural connectivity. |
| Measured object | A connectome graph | A disconnected graph is not a directly measured behavioral deficit. |
| Figure consistency | Poster–table comparison remains flagged | Numerical conclusions are not strengthened while that issue remains. |

The session describes greater disruption under hub removal. This draft keeps the structural interpretation qualitative because the current introduction already flags poster–table consistency for checking.

Random deletion and hub-targeted deletion answer different robustness questions. The first distributes damage across nodes; the second concentrates it on structurally important nodes. A graph statistic can reveal sensitivity to that targeting without identifying a fly’s resulting behavior. Because the current evidence also flags poster–table consistency, this draft retains the qualitative contrast and the analytical design rather than promoting unchecked numerical effect sizes.

## What the comparison shows

This connectivity-defined subgraph is not the whole brain, and graph resilience does not establish behavioral resilience.

## Assumptions and limits

This is a structural graph analysis of a connectivity-defined subgraph, not a whole-brain simulation or a demonstration of behavioral effects. Anatomical annotations were unavailable for the selected archive. Numerical summaries in the poster and session should be checked against the underlying metric tables before citation.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from Hugging Face snapshot `b0218fea4fc3fc9aa37ac616aba20e619e242c1e`. The package contains the archived conversation, session metadata, and resources listed in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this reorganization.
