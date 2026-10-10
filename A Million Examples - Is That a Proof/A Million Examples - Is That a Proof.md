# A Million Examples - Is That a Proof?

## Research topic and question

If a mathematical claim survives a million tests, why is that still not a proof? This case compares sequential testing, random sampling, and a structured search for an exact counterexample to Euler's conjecture about sums of like powers. It uses the historical fifth-power example attributed to Lander and Parkin as a demonstration, not a new discovery.

## Methods and recorded findings

The sequential and random methods test quadruples in **1 <= a <= b <= c <= d <= 144**, a finite space of **18,671,940** possibilities. A hit requires **a^5 + b^5 + c^5 + d^5 = e^5** with **d < e <= 144**. Python arbitrary-precision integers and exact fifth-power lookups avoid approximate roots.

| Method | Recorded work | Recorded elapsed time | Result |
| --- | --- | ---: | --- |
| Sequential | First 1,000,000 distinct quadruples in ascending lexicographic order | 0.149 s | No counterexample |
| Random | 1,000,000 uniform draws from the quadruple space, with replacement; seed 1966 | 2.033 s | No counterexample |
| Structured pair-sum search | 10,296 pair constructions and 497,640 complement lookups; exhaustive within the bounded solution space | 0.082 s | One sorted witness: (27, 84, 110, 133, 144) |

The structured method stores every pair **1 <= a <= b <= 143** by its fifth-power sum, retaining pairs that share a sum. It enumerates **e**, then **c**, then **d** in ascending order with **1 <= c <= d < e <= 144**, looks up **e^5 - c^5 - d^5**, and retains matches with **b <= c**. Random sampling sorts a uniformly drawn four-element subset of 0..146 and maps coordinate i to t[i] + 1 - i, giving uniform nondecreasing quadruples. Simply sorting four independent integer draws would not give that distribution.

The recorded exact check is **27^5 + 84^5 + 110^5 + 133^5 = 144^5 = 61,917,364,224**. The witness quadruple is at lexicographic position **10,418,944**, beyond the sequential budget. Given the single sorted solution found by the exhaustive bounded search, the probability of at least one hit in a million independent uniform draws is **1 - (1 - 1/18,671,940)^1,000,000**, approximately **5.21%**. This is a sampling-model probability; the recorded seeded run is deterministic, and repeated random draws were not counted as distinct coverage.

## Assumptions and limits

The bound **144 was chosen because the published answer was already known**. The search does not target the four summands, but that informed bound makes the problem tractable; the witness is also used for direct verification and a post-search assertion. Finding it here is not an uninformed discovery.

Times are the archived single-run measurements on Python 3.12.14 and macOS ARM64, not new benchmarks. Random generation and pair-table construction are included; shared power-table setup is excluded. Quadruple tests, pair constructions, and complement lookups are different operations, and the workloads have different coverage. These timings do not establish a universal speedup or quantify timing variability.

A million negative tests leave untested cases. Exhaustive finite computation can establish a bounded claim when coverage and implementation are justified; it cannot establish an unbounded claim without an additional argument. Conversely, one exact counterexample suffices to refute a universal claim.

## Research outputs and provenance

The package preserves the conversation, `euler_fifth_power_searches.py`, `euler_search_report.md`, `euler_search_results.json`, `euler_search_comparison.png`, notebook data, the uploaded source guide, and execution evidence.

The recorded source is L. J. Lander and T. R. Parkin, “[Counterexample to Euler's conjecture on sums of like powers](https://doi.org/10.1090/S0002-9904-1966-11654-3),” *Bulletin of the American Mathematical Society* 72 (1966), p. 1079. The session reports checking citation metadata through Crossref and reading `source-guide.md` and `source-guide.json` from the uploaded ZIP. The original AMS PDF was blocked by the session's network destination check. The guide's claimed visual inspection is supplied provenance, not a PDF inspection performed in the recorded session or during this integration.

The original `.science` package and PNG are imported unchanged from [aipoch/open-science-usecases at a1d1bfcb7d1c7a85d3e4a465060fa87fddc6d284](https://github.com/aipoch/open-science-usecases/tree/a1d1bfcb7d1c7a85d3e4a465060fa87fddc6d284/A%20Million%20Examples%20-%20Is%20That%20a%20Proof). Theresa (@theresayao0614-sudo) contributed the case and poster in [94a33e0](https://github.com/aipoch/open-science-usecases/commit/94a33e00f69f7cc8e482b3a6744e89af38d9d7d6). This introduction summarizes the packaged evidence and its stated limitations.
