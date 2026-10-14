# How Often Do Job Posts Ask for Proficiency?

## Research question

How often do exact skill-language expressions occur in one captured job feed?

Counts the exact terms "proficient" and "mastery of" across 100 remote job postings from the Jobicy public API. The archived record includes the collected postings, keyword counts, and an analysis script.

## Data and comparison design

The analysis uses case-insensitive whole-word matching over each posting’s title, excerpt, and description. Count term occurrences separately from the number of postings containing a term; one posting can use the same phrase multiple times.

## Recorded findings

### Result

Across **100 public job postings** (fetched live from the free Jobicy API), the skill keyword **"proficient"** appears **12 times**, and **"mastery of"** appears **3 times**, for a combined total of **15 occurrences**.

| Keyword | Occurrences | Postings containing it |
|---|---|---|
| "proficient" (exact word) | 12 | 8 |
| "mastery of" | 3 | 3 |
| **Total** | **15** | — |

### Method and data source
- **Source:** Jobicy public API — `https://jobicy.com/api/v2/remote-jobs?count=100` (no auth key required; returned exactly 100 remote job postings with full descriptions).
- **Counting:** case-insensitive whole-word regex — `\bproficient\b` and `\bmastery\s+of\b` — over each posting's title + excerpt + description.

### Caveats worth noting
- I first tried **Remotive** (only 17 jobs live), **Arbeitnow** (HTTP 403), **The Muse** (502), and **USAJobs** (requires an API key). Jobicy was the only open no-auth API that returned a full 100 postings.
- The answer is a **point-in-time snapshot** of Jobicy's live feed; it will shift as postings rotate. Re-running the script will produce a fresh count.
- "Proficient" was counted only as the exact word; "proficiency" and other inflections were not folded in. If you'd like the broader stem (e.g., "proficiency") counted too, that's a one-line change.


## What the comparison shows

The result is a dated feed snapshot. It excludes inflections such as proficiency and does not estimate the prevalence of skill requirements across the labor market.

## Assumptions and limits

This is a point-in-time sample from one job feed. Exact-word counts exclude inflections such as "proficiency"; the sample does not represent the entire labor market.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from Hugging Face snapshot `b0218fea4fc3fc9aa37ac616aba20e619e242c1e`. The package contains the archived conversation, session metadata, and resources listed in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this reorganization.
