---
pretty_name: AIPOCH Open-Science Use Cases
size_categories:
  - n<1K
tags:
  - aipoch
  - open-science
  - research-workflows
  - use-cases
---

# AIPOCH Open-Science Use Cases

A collection of Open-Science session exports and their accompanying case posters, published by AIPOCH-AI. The collection covers research questions, data analysis, simulations, and practical AI workflows. Use the posters to browse topics and the available `.science` files to inspect the corresponding sessions in Open-Science.

[Browse all cases](https://huggingface.co/datasets/AIPOCH-AI/open-science-usecases/blob/main/CASES.md) · [Browse repository files](https://huggingface.co/datasets/AIPOCH-AI/open-science-usecases/tree/main) · [File manifest](https://huggingface.co/datasets/AIPOCH-AI/open-science-usecases/blob/main/manifest.json)

## Categories

| Category | Cases | Focus |
|---|---:|---|
| [Curiosity Lab](https://huggingface.co/datasets/AIPOCH-AI/open-science-usecases/tree/main/Curiosity%20Lab) | 48 | Everyday curiosity, natural phenomena, probability, finance, and exploratory science |
| [AI Research](https://huggingface.co/datasets/AIPOCH-AI/open-science-usecases/tree/main/AI%20Research) | 46 | AI capabilities, reliability, behavior, costs, and research progress |
| [Academic Research](https://huggingface.co/datasets/AIPOCH-AI/open-science-usecases/tree/main/Academic%20Research) | 30 | Archived scientific studies across biomedical research, chemistry, environment, and climate |

Categories follow the principal question of each case; they are navigation labels rather than evidence-quality ratings.

## File structure

Each case has its own folder within one of the three category directories:

```text
<Category>/
  <Case title>/
    <Case title>.md
    <Case title>.science
    <Case title>.png
```

- **`.md`**: a case-specific introduction covering the archived study, interpretation and limits, and package provenance.
- **`.science`**: a native Open-Science session export, preserved as supplied.
- **`.png`**: the accompanying poster summarizing the case.
- **`CASES.md`**: a complete case index with absolute links to the introductions.
- **`categories.json`**: category membership and supplied Creator attribution.
- **`manifest.json`**: the case-level publication index. Each case declares `title`, stable `name`, `catalog`, `catalog_name`, and `cover`, `case`, and `introduction` resource objects. Each resource records its filename, repository path, byte size, SHA-256, and `release_url`; an empty URL selects the file stored in this repository.

The latest seven case folders are named after their poster titles. Earlier cases retain their existing names. Some titles contain question marks or Unicode punctuation; adapt local filenames if your operating system requires it.

## How to use

1. Open the [case index](CASES.md) and choose a topic.
2. View the poster, then download the `.science` export where available.
3. Open the export using an Open-Science version that supports the supplied session format. This repository does not specify a minimum compatible application version.
4. Review the source session, assumptions, inputs, and unresolved issues before interpreting or reusing its conclusions. Continuing a workflow may require its original tools, credentials, dependencies, or external data.

To download the collection using the Hugging Face CLI:

```bash
hf download AIPOCH-AI/open-science-usecases --repo-type dataset --local-dir ./open-science-usecases
```

To download one example:

```bash
hf download AIPOCH-AI/open-science-usecases "AI Research/The 100K Cliff/The 100K Cliff.science" --repo-type dataset --local-dir ./open-science-usecases
```

For an exact snapshot, add `--revision <commit-sha>` to the download command. The collection contains application session packages rather than a uniform table of examples; use the native exports to inspect the cases.

## Intended use and limitations

The materials support browsing workflow examples, inspecting recorded sessions, and exploring case-specific methods. Posters are summaries and should be read alongside the available source sessions.

Synthetic demonstrations, estimates, and unresolved findings remain identified in the source materials. Publication of an export does not establish that its conclusions are correct, that the workflow will reproduce in another environment, or that its model performance generalizes. No common evaluation protocol or independently validated aggregate performance score is provided for this collection.

Case selection is curated rather than a representative sample of research tasks. Dates, external services, models, tools, and data sources may differ between cases. Review case-specific provenance and any third-party reuse conditions before reuse.

## License

No repository-wide license has been declared in this snapshot. Public availability should not be interpreted as a grant of unrestricted reuse rights. Check with the publisher and review the rights associated with any third-party material before redistribution.

