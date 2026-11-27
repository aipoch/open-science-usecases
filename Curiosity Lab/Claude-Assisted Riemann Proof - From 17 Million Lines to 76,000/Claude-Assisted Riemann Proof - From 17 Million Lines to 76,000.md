A claim about a Claude-assisted proof of the Riemann Hypothesis became a second question when much shorter Lean editions appeared: what changed between roughly 17 million lines, 300,000 lines and 76,000 lines—and which verification reports belong to which version? This case is a documentary audit of the original archive, a readable rewrite and a compact rewrite. It organizes source claims, version identities, counting conventions and checker reports; it does not run Lean or independently verify the mathematics.

## Research question

A dramatic reduction in source-code size can make a formal development easier to distribute and inspect. It does not, on its own, show that the mathematical argument became simpler, that every theorem has the same scope, or that an earlier machine check verifies a later rewrite. The case therefore asks three separate questions:

1. What are the reported sizes of the three editions, and are their line-count conventions comparable?
2. Which mathematical statements do the rewrite descriptions identify, and what equivalence claims are actually attributed to sources?
3. What was reportedly compiled, compared, replayed or independently checked for each edition—and what did this session itself check?

The retained report is dated 27 November 2026. Its answers are tied to archived source responses and pinned repository commits, rather than a continuously changing project homepage.

## Data and approach

The session first retained its intake tables and earlier inspection records, then captured primary pages with response hashes, HTTP headers, download-completion times and full Git commit identifiers. These are two generations of evidence: a later capture is not silently substituted for an earlier response or historical checker input.

| Material | Retained identity or scope | Role and boundary |
|---|---|---|
| Original-edition accounts | Lean community joint statement and Michael Rubinstein's overview, captured 27 November | Attribute original verification reports; the original proof archive's hash and toolchain remain unresolved |
| Readable and compact rewrite descriptions | `lsernau/grh-lean` at commit `72fead102f663d5c7a407964a13dc0cf9d977207` | Preserve the root and two edition READMEs; README descriptions are not elaborated theorem declarations |
| Community repository | `leanprover-community/riemann-hypothesis` at `7c4ccbd64d02774b0a5b40a5f923f5b7a18e8abc` | Preserve a separate provenance track whose README identifies its readable-edition ancestor |
| Structured comparisons | Claim table, edition table, theorem-scope table and verification matrix | Make each claim inspectable by source, version and qualification |
| Audit and figures | Source manifest, audit record, plot-validation record and editable Python script | Check documentary consistency and plot mappings; perform no proof checking |

The actual workflow was source reading, exact-excerpt validation, SHA-256 hashing, name-list comparison and documentary link checks. Newly captured pages were saved as raw responses, not as a complete offline mirror of all their links. Repository commits supplied documentary identities; the record does not establish that every reported checker run used those exact commits.

## Recorded findings

### Three sizes, several counting conventions

The headline values describe source-reported approximate code lines. The rewrite READMEs also provide counts that include comments and blank lines. The original counting convention is unspecified, so those categories cannot be treated as one standardized measurement across all three editions.

| Edition | Approximate reported code lines | Other reported counts | Interpretation |
|---|---|---|---|
| Original archive | 17,000,000 | Overview reports 175,187 source files | An attributed archive-scale description, not a recount performed in this session |
| Readable rewrite | 300,000 | About 433,000 nonblank lines including comments; about 477,000 total lines | Different line-count definitions must remain visible |
| Compact rewrite | 76,000 | About 95,000 nonblank lines including comments; about 113,000 total lines | A shorter reported development, without an independently standardized reduction percentage |

The source-reported directory counts are also narrower than project totals: readable lists 495 files under `src/Lib` and 306 under `src/New`; compact lists 573 and 219 respectively. The audit keeps those labels rather than presenting their sums as independently counted repository sizes.

Both rewrite READMEs report Lean v4.35.0 and Mathlib commit `56a005855ea17e0b0958f73ec801ae140b0a1679`. The session did not separately inspect configuration files or rebuild either edition. Its code-size figure uses a logarithmic axis and preserves approximate values; it does not calculate a percentage reduction from incompatible counting conventions.

### The same five names are a documentary observation

The pinned readable, compact and community READMEs list the same five theorem names. That supports a comparison of their published descriptions. It does not establish equality of elaborated Lean statements, definitions or dependencies across versions.

| Listed target | Scope described in the rewrite material | Boundary retained in the audit |
|---|---|---|
| `riemannHypothesis` | Mathlib's RH statement | Name-list agreement is not an independent statement-equivalence check |
| `riemannZeta_eq_zero_re` | An explicit statement about zeta zeros | Do not substitute prose similarity for inspected formal declarations |
| `LFunction_ne_zero_of_half_lt_re` | Dirichlet L-function nonvanishing to the right of real part 1/2, with the principal-character pole exception | The exception belongs to the claimed scope |
| `LFunction_eq_zero_re` | Critical-strip zeros of Dirichlet L-functions | The descriptions do not settle zeros with real part at or below zero |
| `LFunction_eq_zero_re_of_isPrimitive` | Primitive-character specialization | A narrower specialization must remain distinct from a blanket claim about every generalized or extended hypothesis |

The rewrite descriptions specify all moduli `N >= 1` and primitive as well as nonprimitive characters. Separately, the root README says the compact edition has the same five theorems as the readable edition, while the overview claims theorem statements identical to the original. Those are different attributed comparisons. Original declarations were not inspected, so the audit leaves the original five-name mapping unresolved.

### Verification belongs to a version and a procedure

Compilation, theorem comparison, kernel replay, an independent checker and human mathematical review answer different questions. A single “verified” badge would conceal those distinctions. The retained verification matrix separates them for each edition.

| Verification dimension | Original | Readable rewrite | Compact rewrite |
|---|---|---|---|
| Statement comparison | Reported RH match against Mathlib | Reported Comparator acceptance | Reported Comparator acceptance |
| Compilation | Reported pass | Reported pass | Reported pass |
| Lean kernel or replay | Reported original replay | Build/comparator reported; completed full-module replay unspecified | Explicit replay pass reported |
| Independent checker | Reported original exported-proof acceptance | README reports nanoda, con-leche and con-ron acceptance | README reports independent-checker acceptance |
| Axiom audit | Three standard axioms reported | Three standard axioms reported | Three standard axioms reported |
| Human review | Statement vetting reported | No complete mathematical read-through reported | No complete mathematical read-through reported |
| New proof check in this session | None | None | None |

The joint statement's explicit comparison concerns RH against Mathlib; it is not an observed all-five, cross-version comparison. Its original-archive checks cannot automatically be transferred to a rewrite. The rewrite axiom reports name `propext`, `Classical.choice` and `Quot.sound`; this session did not execute an axiom audit itself.

The overview's later compact-specific account reports 794 compiled and replayed modules and paranoid Comparator acceptance. It describes a no-sandbox cluster run and attributes agreeing sandboxed runs to Sutherland. Exact historical checker inputs, logs and operator independence remain unresolved in this case; the report does not erase those qualifications by treating environments as interchangeable.

### Chronology is part of the evidence

| Date reported by a source | Event or claim | What the session can retain |
|---|---|---|
| 20 November | Author announcement of a Claude-assisted proof | An attributed claim from the earlier uploaded PDF extraction; the publisher copy was not newly fetched |
| 21 November | Joint statement and original checker reports | Captured primary accounts with version-specific scope |
| 22 November | A related 265-page v2 exposition described as a working draft | A page-reported description; the PDF was not inspected, and the draft does not prove its condition (M) or thirteen hypotheses outright |
| 25 November | Shortened release and community transition reported | Captured rewrite commit metadata and community ancestry description |
| 26 November | Compact-edition external checks reported | A later, compact-specific report with environment qualifications |
| 27 November | New source snapshots captured and tables consolidated | A documentary capture date, not an invented publication date or checker-run date |

The root README says machine checks only, no mathematician has read the proof through, and no paper accompanies it. A related conditional working draft is not automatically a contradiction to that statement: its relationship, mathematical conditions and review status need to be specified rather than compressed into “a paper exists.”

## What the evidence shows

The useful result is a structured separation of claims that headlines tend to combine. The sources describe substantial shortening and several reported checking procedures. The audit makes it possible to ask which edition, which statement, which procedure and which evidence supports each description.

The archived session records eleven passing documentary checks, including historical-byte preservation, source body/header hashes, claim excerpts, theorem listings, plot mappings and report links. It also records nine unresolved items. Passing those checks means the retained audit materials agree under those tests; it does not turn this session into an independent mathematical verification.

The two figures serve different purposes. The code-size plot compares approximate source reports on a log scale, with counting caveats. The verification-scope plot compares 21 attributed status cells across three editions and seven dimensions. When provenance wording changed, only the affected code-size figure was rerun; the earlier verification image was retained byte-for-byte because its plotted statuses had not changed. The archived record does not reassign that earlier image to later pinned source captures.

## Assumptions and limits

- The original proof archive's exact identity and toolchain remain unresolved. The new rewrite commit identities do not fill that gap.
- Earlier same-day inspections were not byte-snapshotted. Identity between those responses and later captured pages is unestablished.
- README theorem names and descriptions are documentary evidence, not elaborated statement comparison or complete mathematical-scope review.
- Line counts were not independently measured using a common convention; fewer lines do not prove simpler mathematics or a quantified gain in AI reasoning.
- Historical checker-run commits, detailed logs and operator independence are not fully established here. No new Lean build, replay, independent-checker run or axiom audit occurred.
- The related exposition PDF was not inspected, and complete human mathematical review was not established.

During publication preparation, the native export's inventory and content/evidence references were checked for byte-level consistency and the English introduction was prepared for ordinary Markdown rendering. Those distribution checks do not reproduce the research or extend its mathematical conclusions.

## Sources and research materials

Primary sources corresponding to the retained documentary capture:

- [Lean community joint statement](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/).
- [Michael Rubinstein's original and shortened-proof overview](https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/).
- [Pinned rewrite root README](https://github.com/lsernau/grh-lean/blob/72fead102f663d5c7a407964a13dc0cf9d977207/README.md).
- [Pinned readable-edition README](https://github.com/lsernau/grh-lean/blob/72fead102f663d5c7a407964a13dc0cf9d977207/grh/README.md).
- [Pinned compact-edition README](https://github.com/lsernau/grh-lean/blob/72fead102f663d5c7a407964a13dc0cf9d977207/grh-compact/README.md).
- [Pinned community README](https://github.com/leanprover-community/riemann-hypothesis/blob/7c4ccbd64d02774b0a5b40a5f923f5b7a18e8abc/README.md).

The native session retains the consolidated report, four comparison tables, source snapshots and headers, source manifest, audit record, plot-validation record, editable figure script, two figures and historical records. Its consolidated ZIP preserves the internal directory structure for offline inspection. These are documentary research materials, rather than a compiled proof archive or a newly executed proof-verification environment.
