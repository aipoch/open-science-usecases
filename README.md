# AIPOCH Open-Science Cases

This repository collects completed Open-Science session exports, covers, and introductions. The root `manifest.json` serves as the case index.

Cases follow upstream's [classification snapshot](https://github.com/aipoch/open-science-usecases/blob/2d19bdbaffa776fb6c75951005ac88e74cc6aac9/categories.json), extended with the Academic Research import and integrated with the catalog fields and directories:

| Stage | Catalog directory | `catalog_name` | Cases | Migration |
| --- | --- | --- | --- | --- |
| 1 | [`AI Research/`](<AI Research/>) | `ai-research` | 46 | 43 existing cases and three creator cases |
| 2 | [`Curiosity Lab/`](<Curiosity Lab/>) | `curiosity-lab` | 48 | 45 existing cases and three creator cases |
| 3 | [`Academic Research/`](<Academic Research/>) | `academic-research` | 30 | 30 approved cases from the verified Hugging Face snapshot |

The manifest contains 124 cases synchronized with the Hugging Face collection: AI Research (46), Curiosity Lab (48), and Academic Research (30). The previously excluded flight case is not in the active index; its legacy files remain untouched under `usecases/`.

`manifest.json` is the authoritative publication index, including catalog fields and resource paths. `categories.json` mirrors the 124 classified cases and records Creator attribution where supplied.

Each entry contains a `title`, a unique kebab-case `name`, the two classification strings, and three resources: `cover`, `case`, and `introduction`. Every resource provides `file_name`, `path`, `bytes`, `sha256`, and `release_url`. An empty URL selects a local file; a nonempty URL selects a remote resource. Fully remote entries do not need local directories but must still retain valid paths. The 13 previously imported packages and 30 Academic Research packages retain their pinned Hugging Face sources; their covers and introductions are stored locally. The Academic Research import uses the [verified snapshot](https://huggingface.co/datasets/AIPOCH-AI/open-science-usecases/tree/b95158d1fb9fec49a5044657aad02fa7145eb64d/Academic%20Research), preserves the original session exports and posters, and includes reviewed introductions without author attribution.

A nonempty `catalog` is the display label and a directory at the repository root. All resource paths start with `<catalog>/` and may use independent subdirectories beneath it. Derive `catalog_name` as ASCII kebab-case, for example `Data Science` becomes `data-science`. Non-ASCII names, empty conversions, and collisions between different catalogs produce errors for the user to resolve. Multiple cases may share a catalog. Both classification fields must be empty or both populated.

```text
Data Science/example/
  cover.png
  session.science
  introduction.md
```

Directories, titles, and names can be chosen independently. S3 always uses `<name>/<file_name>`, with extracted package contents under `<name>/extracted/`. Moving directories does not change S3 resource keys.

Original `.science` session contents remain unchanged. Simulation demonstrations and unresolved conclusions noted in a case remain subject to the source session; inclusion does not guarantee general model performance.

- [Browse cases by catalog](CATEGORIES.md)
- [Adding and updating cases](AGENTS.md)
- [Validation rules and commands](.github/CHECKING.md)
- [Publication, deduplication, and recovery](.github/PUBLISHING.md)

Local tests: `python3 -B -m unittest discover -s .github/tests -v`. Tests use temporary data and fake S3; they do not perform live publication.
