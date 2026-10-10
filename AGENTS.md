# Rules for Adding Cases

- Every new case must conform to the current root `manifest.json` structure and `.github/scripts/check_structure.py` requirements. Add exactly one entry to the existing top-level array, with `title`, a unique kebab-case `name`, and the nested resource objects `cover`, `case`, and `introduction`; do not omit required fields or change the schema to accommodate an incomplete case.
- Each resource object must include `file_name`, `bytes`, `sha256`, and `path`; `case` must also include `release_url`. Match the case directory and actual resource filenames, use repository-relative paths, and record the actual file sizes in bytes.
- Every new case must include a nonempty introduction Markdown file named `<case directory name>.md` inside its case directory. Read and verify the introduction's actual content so it accurately describes the case; an empty file, placeholder text, or `README.md` is not a substitute. Register this file in `introduction` using the existing resource-object structure, rather than embedding its Markdown text in `manifest.json`.
- When adding a case directory without a local `.science` package, you must set `case.release_url` in the corresponding entry in the root `manifest.json` to the download URL for that case's `.science` package. The field must not be missing, empty, or whitespace-only.
- Exactly one package source must be provided: a local `.science` file or a nonempty `case.release_url`. If the directory contains the local file, `case.release_url` must be an empty string. Keep `case.path` for both local and remote packages.
- Before completing a case addition, check each new directory and its manifest entry for schema compliance, complete introduction content, correct resource paths and byte sizes, computed SHA-256 values, and exactly one package source. Resolve missing content or metadata before considering the addition complete.

# SHA-256 Metadata

- Before committing added or modified case resources, compute SHA-256 from the actual files on the user's device and update the corresponding `sha256` values in `manifest.json`. For remotely hosted `.science` packages, compute the digest from the local package before uploading it.
- For every new case, compute SHA-256 for all three resources (`cover`, `case`, and the introduction `.md`) after their contents are finalized, before considering the addition complete. Recompute `sha256` and update `bytes` whenever a resource changes; never reuse another file's digest or invent a value.
- Every resource (`cover`, `case`, and `introduction`) in an affected case must have a `sha256` string containing exactly 64 hexadecimal characters (`0-9`, `a-f`, or `A-F`), without whitespace.
- The check action validates SHA-256 presence and format only. It must not download resource bodies or recompute checksums; existing HEAD availability and size checks remain in place.
