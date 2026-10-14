# How Often Do Job Posts Ask for Proficiency?

## Research question

How often do exact skill-language expressions occur in one captured job feed?

## Data and method

Use case-insensitive whole-word matching over each posting’s title, excerpt, and description. Count term occurrences separately from the number of postings containing a term; one posting can use the same phrase multiple times.

## Recorded findings

Counts the exact terms "proficient" and "mastery of" across 100 remote job postings from the Jobicy public API. The archived record includes the collected postings, keyword counts, and an analysis script.

The archive counts 12 occurrences of proficient in eight postings and three occurrences of mastery of in three postings among 100 captured Jobicy entries.

## What the findings mean

The result is a dated feed snapshot. It excludes inflections such as proficiency and does not estimate the prevalence of skill requirements across the labor market.

## Interpretation and limits

This is a point-in-time sample from one job feed. Exact-word counts exclude inflections such as "proficiency"; the sample does not represent the entire labor market.

## Package and provenance

The original `.science` export and matching poster are preserved byte-for-byte from Hugging Face snapshot `b0218fea4fc3fc9aa37ac616aba20e619e242c1e`. The package contains the archived conversation, session metadata, and resources listed in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this reorganization.
