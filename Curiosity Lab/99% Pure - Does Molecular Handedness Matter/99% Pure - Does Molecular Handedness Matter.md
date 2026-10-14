# 99% Pure - Does Molecular Handedness Matter

## Research question

Can two equally pure samples contain very different proportions of the desired enantiomer?

Uses hypothetical mixtures to distinguish chemical purity, enantiomer ratios, and enantiomeric excess. The session records hand-checkable examples and a sweep that holds total chemical purity constant.

## Data and comparison design

The design keeps a common 100-mole basis and distinguish target compound from unrelated impurity. Compute chemical purity using the whole mixture, but compute the left:right ratio and enantiomeric excess using only the target compound. Keeping these denominators explicit prevents a purity percentage from being mistaken for stereochemical composition.

## Recorded findings

Ran eight hypothetical examples and a 1,001-point sweep in the notebook. Numerical checks passed.

At **99% chemical purity**:

| Case | L:R within target | ee |
|---|---|---|
| 99% of target molecules are L | 99:1 | 98% L |
| 99% ee favoring L | 99.5:0.5 | 99% L |

Here, chemical purity explicitly counts **both L and R**: `100(L + R) / (L + R + I)`. A single-enantiomer specification may count R as an impurity; the report explains that distinction.

## What the comparison shows

These constructed mixtures explain definitions; they are not measurements of a manufactured batch or evidence about biological activity.

## Assumptions and limits

These are constructed arithmetic examples, not laboratory measurements. The definition of purity counts both handed forms and must be distinguished from a single-enantiomer specification.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
