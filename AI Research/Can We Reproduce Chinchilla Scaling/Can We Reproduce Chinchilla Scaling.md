# Can We Reproduce Chinchilla Scaling

**Creator:** @Xudong07452910

## Research question

Can the public reconstruction of Chinchilla Figure 4 reproduce Epoch AI’s fitted scaling law, and how sensitive are its uncertainty estimates and compute-optimal allocation to optimization settings and five unusually undertrained runs?

This case examines Approach 3: fitting a loss function to model size and training tokens. It reanalyzes existing measurements extracted from a published figure; it does not train new language models or independently reproduce Chinchilla’s downstream performance. The supplied Open-Science session contains a completed analysis, corrected final report, code, result tables and figures.

## Data and comparison design

The captured input is Epoch AI’s `svg_extracted_data.csv`. Its `Model Size`, `Training FLOP` and `loss` columns describe reconstructed parameter counts N, training compute C and final losses. Training tokens are derived using the approximation `D = C / (6N)`.

| Input characteristic | Recorded value | Meaning for the analysis |
| --- | --- | --- |
| Reconstructed observations | 245 | A subset recovered from Figure 4, not the complete original training dataset |
| Missing or duplicate rows | None reported | Basic checks of the captured table |
| Model parameters N | 5.73 × 10⁷ to 1.62 × 10¹⁰ | The observed model-size range |
| Training compute C | 1.4 × 10¹⁸ to 1.3 × 10²² FLOP | The observed compute range |
| Final loss | 2.077 to 5.006 | Digitized outcome values |
| Derived training tokens D | 2.45 × 10⁸ to 3.18 × 10¹¹ | Depends on the approximate FLOP conversion |
| Main fitting sample | 240 observations | Excludes the five highest-loss points |
| Sensitivity sample | All 245 observations | Tests how those five points change the fitted allocation |

The excluded points have approximately 2.0–6.8 billion parameters but only 0.245–0.812 billion derived training tokens. Their D/N ratios are about 0.036–0.404. The main analysis follows the five-point exclusion used in the replication study, while retaining an all-points sensitivity analysis. These runs cannot simply be treated as erroneous or irrelevant: their influence is one of the results being examined.

## Fitting procedure

The assumed loss surface is:

`L(N, D) = E + A / N^α + B / D^β`

Here E is the fitted asymptotic loss term. The two remaining terms represent modeled contributions associated with finite parameter count and finite training data. They are components of an assumed empirical function, not separately measured causes of loss.

The fitting procedure works in logarithmic coordinates for A, B and E. A log-sum-exp calculation produces the predicted log loss, and the objective sums Huber penalties on predicted-minus-observed log loss.

| Method choice | Recorded implementation | Why it matters |
| --- | --- | --- |
| Huber threshold | δ = 0.001 in log-loss space | Controls the quadratic versus linear residual penalty |
| Initializations | 4,500 combinations | Reduces dependence on one starting point |
| Initialization grid | α, β: 0 to 2 in steps of 0.5; log E: −1 to 1 in steps of 0.5; log A, log B: 0 to 25 in steps of 5 | Makes the starting-point search explicit |
| Final optimizer | L-BFGS-B with an analytic gradient | The corrected implementation used for the retained results |
| Final stopping settings | ftol = 10⁻¹⁵; gtol = 10⁻¹²; maxiter = 5,000 | Tightens stopping criteria for the small objective values |
| Earlier implementation | Default stopping settings and numerical gradients | Retained as a comparison, particularly for uncertainty estimation |

The recorded grid search places 33.8% of main-sample starting points within 10⁻⁸ of the best objective. That is evidence of agreement among many starts in this search, rather than a proof of global optimality.

## Recorded findings

### 1. The refit is close to Epoch AI’s main estimates

| Parameter | Hoffmann Approach 3, rounded body values | Epoch AI Table 1, 240 points | Supplied analysis, 240 points | Supplied analysis, all 245 points |
| --- | ---: | ---: | ---: | ---: |
| E | 1.69 | 1.8172 | 1.8172 | 1.8913 |
| A | 406.4 | 482.01 | 477.83 | 495.73 |
| B | 410.7 | 2,085.43 | 2,143.42 | 12,845.61 |
| α | 0.34 | 0.3478 | 0.3473 | 0.3493 |
| β | 0.28 | 0.3658 | 0.3672 | 0.4530 |

The refit reproduces the broad parameter pattern and the improved fit reported by Epoch AI. It is numerically close, rather than identical after rounding: A differs by about 0.9% and B by about 2.8%. Including the five points increases the fitted data exponent and coefficient substantially, demonstrating sensitivity in the derived extrapolation.

### 2. Parameter sets should be compared on the same observations

The following table uses the 240-point main sample throughout. Raw-loss errors and the log-space optimization objective describe different scales.

| Parameter set | Sum of log-space Huber penalties | Raw-loss RMSE | Raw-loss MAE | Mean residual, prediction minus observation |
| --- | ---: | ---: | ---: | ---: |
| Hoffmann rounded Approach 3 | 0.00412 | 0.0526 | 0.0476 | +0.0447 |
| Epoch AI Table 1 | 0.00102 | 0.0218 | 0.0126 | −0.0008 |
| Supplied main-sample refit | 0.00102 | 0.0218 | 0.0126 | −0.0021 |
| Supplied all-points refit, evaluated on the main sample | 0.00116 | 0.0190 | 0.0138 | +0.0010 |

The rounded original parameters have an objective about four times the main refit’s and a positive average residual. The archived residual plots examine that pattern by compute and tokens per parameter.

The all-points fit has a lower raw-loss RMSE on the main sample while a worse Huber objective. This is not a contradiction: minimizing a robust log-space objective is different from minimizing squared error in raw loss. A claim about the “best fit” therefore needs to name its metric.

### 3. Optimizer settings substantially affect the recorded bootstrap spread

The corrected analysis resamples the 240-point dataset with replacement 2,000 times and initializes each fit at the main optimum. It does not repeat the full 4,500-start search for every resample. A default-setting comparison uses the same first 500 resamples.

| Quantity | Main estimate | Bootstrap SE, strict settings | Recorded 95% percentile interval | SE, default-setting comparison |
| --- | ---: | ---: | --- | ---: |
| A | 477.83 | 123.22 | 287.06–733.98 | 0.0582 |
| B | 2,143.42 | 1,242.62 | 1,153.67–5,732.38 | 0.1946 |
| E | 1.8172 | 0.02517 | 1.7724–1.8708 | 0.00476 |
| α | 0.3473 | 0.01517 | 0.3169–0.3727 | 0.000531 |
| β | 0.3672 | 0.01953 | 0.3359–0.4148 | 0.000391 |
| Compute-allocation exponent a | 0.5139 | 0.01903 | 0.4820–0.5553 | 0.000558 |

A separate exercise follows the original paper’s 80%-subsample, 100-repeat design. Its recorded 10th-to-90th-percentile interval for a is 0.4993–0.5251, width 0.0258. The original interval transcribed in the supplied report is 0.454–0.455, width 0.001. These intervals must not be confused with the 95% bootstrap interval above.

Under the default-setting exercise, the subsampling interval width falls to approximately 0.0007. In the recorded 30-resample optimizer diagnostic, tighter L-BFGS-B, BFGS and a small initialization grid agree on lower objectives and a wider spread than the default-setting run.

This demonstrates a mechanism within this implementation: insufficient movement away from the initial optimum can produce artificially small resampling variability. It does not establish what happened in the original authors’ implementation. The recorded comparison also changes gradient handling, so its effect should not be attributed to one tolerance constant alone.

### 4. “About 20 tokens per parameter” is compatible with the main fit, but is not a constant

Under the constraint `C = 6ND`, the assumed surface implies:

`a = β / (α + β)`  
`b = α / (α + β)`  
`G = [αA / (βB)]^(1 / (α + β))`  
`N_opt = G × (C / 6)^a`  
`D_opt = (C / 6)^b / G`  
`D_opt / N_opt = (C / 6)^(b − a) / G²`

The main fit gives a = 0.5139 and b = 0.4861, close to equal growth of model size and training tokens. Its estimated b − a is −0.0278, but the recorded 95% interval is −0.1105 to +0.0360. Approximately 20.9% of bootstrap draws give b > a. The point-estimate decline in tokens per parameter is therefore not a statistically resolved direction throughout the uncertainty distribution.

| Compute budget | Main fit: optimal tokens per parameter | Recorded 95% bootstrap interval | All-points fit: optimal tokens per parameter |
| --- | ---: | --- | ---: |
| 10²¹ FLOP | 21.4 | 15.6–28.3 | 15.5 |
| 5.76 × 10²³ FLOP | 17.9 | 7.8–35.5 | 6.8 |
| 10²⁶ FLOP | 15.5 | 4.5–42.4 | 3.5 |

The conventional value of 20 lies within the main fit’s intervals. However, the Chinchilla-scale compute budget already exceeds the largest observed budget, and 10²⁶ FLOP is nearly four orders of magnitude above it. The wide intervals and the all-points sensitivity make these model-based projections unsuitable as a universal training prescription.

## What the comparison shows

The case illustrates three distinct reproducibility questions: whether the same public observations produce a similar fitted surface; whether uncertainty survives a change in numerical implementation; and whether a derived scaling recommendation is stable outside the observed range.

The retained results support a close reproduction of Epoch AI’s main fit and show that the rounded original parameters describe this reconstructed subset less well under the chosen objective. They also show why a convincing point estimate does not guarantee a trustworthy bootstrap interval. Finally, the near-equal allocation exponents are more stable as a broad interpretation than a precise token-to-parameter ratio at extreme compute budgets.

## Assumptions and limits

- Figure-derived measurements contain coordinate and color-quantization error. They are not the complete original set of training observations, and the available runs may not be a representative statistical sample.
- `C = 6ND` is an approximation. Deviations in FLOP accounting or architectures can alter the conversion from compute to tokens.
- The five-point exclusion materially affects the fitted data term and allocation projections. Both versions belong in the interpretation; neither is automatically the unique correct fit.
- The functional form is assumed. Row-resampling intervals are conditional on the captured dataset and analysis design; they do not encompass model-form uncertainty or the original training experiment’s full variability.
- Bootstrap optimization differs from Epoch AI’s stated BFGS procedure, and only 30 diagnostic resamples were checked against additional optimizer/search settings.
- The main error comparison uses rounded original-paper parameters. The package separately examines more precise exponents transcribed through the replication paper; those source values must not be mixed with the rounded set without labeling.
- This introduction summarizes retained artifacts and checks their reported values. It does not rerun model fitting, bootstrap computation or language-model training, and archived review or integrity records are not independent scientific validation.

## Sources and research materials

| Source | Role |
| --- | --- |
| [Hoffmann et al., Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556) | Original scaling-law study and Approach 3 specification |
| [Besiroglu et al., Chinchilla Scaling: A replication attempt, v2](https://arxiv.org/abs/2404.10102v2) | Published replication, parameter comparison and uncertainty discussion |
| [Epoch AI analysis repository](https://github.com/epoch-research/analyzing-chinchilla) | Public reconstruction and replication code |
| [Figure-derived input CSV](https://raw.githubusercontent.com/epoch-research/analyzing-chinchilla/main/data/svg_extracted_data.csv) | Public location of the input; the saved package retains the captured bytes |

The supplied package retains the final version of `REPORT.md`, the replication bundle, data-check and fitting scripts, parameter and error tables, bootstrap samples and summaries, allocation calculations, and residual/uncertainty figures. Earlier default-setting files remain explicitly identified as historical comparisons. The numerical tables above are drawn from those retained results, rather than from a fresh download of the mutable repository branch.
