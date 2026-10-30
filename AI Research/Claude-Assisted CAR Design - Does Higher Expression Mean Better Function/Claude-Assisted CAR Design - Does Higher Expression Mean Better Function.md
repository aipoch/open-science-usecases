# Claude-Assisted CAR Design: Does Higher Expression Mean Better Function?

## The question

A receptor can become easier to express without improving every functional endpoint. This case examines that distinction in a Claude-assisted chimeric antigen receptor (CAR) design study: when a redesigned intracellular domain produces more surface receptors, does it also produce stronger cytokine responses, more tumor-cell killing, or longer activity?

The archived investigation focuses on Figure 2a–g and the relevant Results and Methods of Generate Biomedicines' *Refactored intracellular domains enhance CAR expression and function*. It then maps broader public claims to the later designs and experiments that actually support them.

**The central finding is context dependence.** In the reported BCMA system, brs–ζ1–40 has 13-fold greater surface receptor density and twice the peak IFN-γ of BBζ, while killing potency is described as similar. Its expression and cytokine advantages do not transfer to the tested CD19 system. More receptor expression is therefore an engineering observation, not a sufficient surrogate for better killing.

## What was compared

BBζ is the 154-amino-acid reference intracellular domain. brs–ζ1–40 is a 54-aa design. The Figure 2 candidate **krgr–ζ1–4-1bb** and the later 45-aa lead **krgr–ζ1–40** are different constructs; swapping their names would also swap the evidence supporting the headline.

| Feature | BCMA experiment | CD19 experiment |
|---|---|---|
| Binder | bb2121 scFv | FMC63 scFv |
| Antigen | BCMA | CD19 |
| Target cells | H929 myeloma | NALM6 leukemia |
| Effectors | Primary human T cells | Primary human T cells |
| Delivery | mRNA | mRNA |
| Expression / IFN-γ / killing | Figure 2a / 2b / 2c | Figure 2d / 2e / 2f |
| Co-culture replication | Two wells per condition | One well per condition |
| Target-free IFN-γ in the focal panels | Figure 2g | No corresponding panel in Figure 2a–g |

The functional assays use 24-hour co-cultures and eight twofold effector-to-target (E:T) ratios, approximately 0.16:1–20:1. E:T counts **CAR-positive T cells**, rather than all T cells. Equal mRNA mass does not imply equal receptor density or equal numbers of transcript molecules. Binder, antigen, and target-cell context change together between systems, preventing attribution of cross-system differences to the binder alone.

## Three endpoints that must stay separate

| Readout | How the report describes it | What it does not establish |
|---|---|---|
| Surface expression | Anti-FLAG staining and calibration estimate CAR molecules per CAR-positive cell. | The percentage of positive cells, activity per receptor, or therapeutic efficacy |
| Peak IFN-γ | The maximum supernatant concentration across the E:T titration after 24 hours | A comparison at one fixed E:T, stronger killing, or a clinical benefit |
| Killing | Residual luciferase target signal, normalized separately for each construct and replicate | A direct absolute count of viable targets or formal equivalence between designs |

For Figure 2 killing, the recorded normalization is:

```text
Normalized target signal at E:T x (%)
    = 100 × L(x) / L(lowest E:T)
```

The denominator already contains T cells and may already involve killing. A 50% normalized signal means half the luminescence of that construct's lowest-E:T reference, rather than necessarily half of the initial targets remaining alive. Distinct denominators also complicate absolute comparisons between constructs. The session did not extract a numerical Figure 2 killing IC₅₀.

## Reported results, design by design

Every comparison below uses BBζ **within the same experimental system**. Ratios are author-reported; the session did not independently derive them from absolute raw measurements.

| Design and system | Surface expression | Peak IFN-γ | Killing |
|---|---|---|---|
| brs–ζ1–40, BCMA | **13×** BBζ | **2×** BBζ | Described as similar potency |
| brs–ζ1–40, CD19 | Slightly lower; ratio unavailable | Lower; ratio unavailable | Described as similar potency |
| krgr–ζ1–4-1bb, BCMA | Higher; ratio unavailable | Exact comparison unresolved | Exact comparison unresolved |
| krgr–ζ1–4-1bb, CD19 | **2.5×** BBζ | **3.4×** BBζ | Among the most potent; superiority over BBζ unresolved |

Similar potency in this report is not a formal equivalence result. A missing exact comparison is not evidence that the endpoint was unmeasured or that the result was null. The archived evidence matrix keeps these states distinct.

The case's recorded Python checks used an original 21-row evidence snapshot covering three focal designs and seven panels. The final evidence CSV contains 23 rows, with an added target-free exception and a negative-control record. The saved validation result applies to its 21-row analysis snapshot, rather than silently validating those later additions.

## What the no-target control shows

| Figure 2g observation | Appropriate interpretation |
|---|---|
| brs–ζ1–40, BBζ, and krgr–ζ1–4-1bb: IFN-γ below **9.8 pg/mL** | Below the assay's detection limit in the tested BCMA target-free condition |
| brs–ζ1–4-1bb–ζ3 | A reported detectable exception; exact concentration unavailable |
| Negative control | Exact value, detection status, and control identity unresolved in the extracted record |
| CD19 target-free response | Not established by these focal panels |

Below-limit values are left-censored bounds, not zero measurements. They support “no detectable antigen-independent IFN-γ under the tested 24-hour conditions.” They do not show absence of every form of tonic signaling, exhaustion, or long-term safety risk. The report explicitly says exhaustion was not measured.

## Why the public headline needs a design-and-assay map

The public Generate summary describes a shorter design with greater expression, improved killing, and longer activity. The archived review maps these claims primarily to the later **krgr–ζ1–40** lead and Figures 3–4, rather than assigning all of them to Figure 2's brs–ζ1–40.

| Claim | Evidence identified in the archived review | Qualification |
|---|---|---|
| About 70% shorter | 45 aa versus 154 aa: **70.8% shorter**, calculated as `100 × (1 − 45/154)` | Intracellular domain length, not the whole CAR or mRNA |
| Roughly ten times the receptors | Reported 8.4× at the highest mRNA dose and 12× on day 1 in separate experiments | Context-dependent surface abundance, not a universal multiplier |
| Improved killing | Reported 2-fold lower IC₅₀ E:T in Figure 3d; 1.3-fold lower in a later lentiviral experiment | Assay-specific results with different delivery and normalization contexts |
| Longer activity | Reported detectable IFN-γ and sustained killing through day 13 in later time-course challenges | Does not demonstrate slower decay, exhaustion avoidance, or clinical persistence |
| Broader payload potential | Later multi-CAR expression work includes HER2 and MUC16 binders | Does not establish solid-tumor efficacy or simultaneous four-CAR expression in every cell |

The later lead combines an anchor from one candidate with another scaffold after experimental feedback. Scientists set objectives and selected and refined candidates; models supported proposals and rationales; experiments established expression and function. These contributions should not be collapsed into an unaided single-model discovery. Demonstrating superiority over an equally resourced expert or alternative-model workflow would require an appropriate design baseline.

## What would resolve the mechanism

| Follow-up comparison | What it would help answer |
|---|---|
| Change receptor density within an unchanged intracellular domain | Whether abundance contributes to a within-design dose–response relationship |
| Compare designs at overlapping surface-density distributions | Whether functional differences remain after abundance is controlled |
| Use common target-only controls and direct target-survival measurements | Whether relative luminescence normalization obscures absolute killing differences |
| Pair designs across donors and independent preparations | How biological variation affects superiority or equivalence claims |
| Measure basal signaling and function over time | Whether cytokine nondetection extends to broader signaling and persistence properties |

These are proposed comparisons, not experiments performed by this case. Dividing the 2-fold cytokine gain by the 13-fold expression gain would not estimate a validated per-receptor efficiency: one readout is a well-level peak and the other a cell-level abundance summary, with nonlinear responses and differing peak E:T ratios still possible.

## Materials, limits, and provenance

The native archive retains the conversation, the final `CAR_expression_function_evidence_report.md`, eight explanatory figures, the evidence CSV, design-by-system matrix, plotted fold values, validation snapshot, analysis code, and headline-to-experiment mapping. The original Figure 2 image was unavailable to the session through its figure cache; it used caption, Results, and Methods text and did not digitize the original curves. Later findings were contextualized from prose rather than independently remeasured.

The primary source is Bai and colleagues, [*Refactored intracellular domains enhance CAR expression and function*](https://generatebiomedicines.com/publications/refactored-intracellular-domains-enhance-car-expression-and-function/). The contextual public source is Anthropic's [*Early progress on accelerating drug development with Claude*](https://www.anthropic.com/research/early-progress-drug-development).

This introduction summarizes the supplied AIPOCH Open-Science session. The native package's original bytes and evidence records are preserved; only its external filename uses hyphens instead of spaces. Preparing this page did not repeat cell experiments, independently validate clinical benefit, or establish a causal effect of model assistance.
