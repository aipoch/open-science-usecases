# Case Validation

Resource validation selects added or modified entries that still exist in the root `manifest.json`. Resource-only changes, removed entries, reordering, and JSON formatting changes do not trigger scans of other cases' resources. Catalog fields and mappings are checked across the entire target manifest, including unchanged entries, so incremental checks cannot miss collisions with existing catalogs. Fully remote entries are also selected and need no local directory. Each `name` must be unique across the entire index; titles and directory names can be chosen independently.

## Field rules

The top level is an array. Each entry contains `title`, `name`, `catalog`, `catalog_name`, `cover`, `case`, and `introduction`. Both classification fields must be strings; two empty strings (`""`) mean unclassified. Missing fields, null, whitespace-only values, and filling only one field are invalid.

A nonempty `catalog` is the display label and a single classification directory name. Derive `catalog_name` by converting `catalog` to ASCII kebab-case as specified in [AGENTS.md](../AGENTS.md). Mismatched conversions, non-ASCII characters, empty conversions, and different catalogs with the same converted identifier are rejected without automatic translation, transliteration, or numbering. Reusing the same catalog is allowed. All resource paths, including remote sources, must start with the literal `<catalog>/`; arbitrary depth and separate resource directories are allowed beneath it. Catalog names cannot contain traversal, separators, control characters, or drive-letter paths.

All three resources share the same structure:

| Field | Requirement |
| --- | --- |
| `file_name` | Actual filename, equal to the final segment of `path` |
| `path` | Safe repository-relative path; classified resources start with `<catalog>/` and may use arbitrary subdirectories; unclassified prefixes are unrestricted; required for remote sources as well |
| `bytes` | Nonnegative integer byte count; booleans and strings are not accepted |
| `sha256` | 64 hexadecimal characters with no whitespace; comparisons are case-insensitive |
| `release_url` | `""` selects a local source; a nonempty value must be a valid HTTP(S) download URL and cannot contain only whitespace |

The cover must have an image extension, the package must be a `.science` file, and the introduction must be a `.md` file. Duplicate JSON fields, missing or unknown fields, absolute paths, backslashes, control characters, empty path segments, and `.` / `..` segments are rejected. Windows drive-letter paths are also rejected. New manifests must explicitly provide all three `release_url` fields. Historical S3 baselines allow legacy root-level paths and treat missing cover and introduction URLs as empty strings during comparison.

For example, the `Data Science` catalog may contain `Data Science/covers/cover.png`, `Data Science/packages/session.science`, and `Data Science/docs/zh/intro.md` in one entry. Unclassified root-level files may use their filenames directly as paths. `usecases/` is simply how the existing unclassified cases are organized.

## Sources and checks

| cover | case | introduction | Local checks | Remote checks |
| --- | --- | --- | --- | --- |
| Local | Local | Local | Directories and all three files | None |
| Remote | Local | Local | Directories, package, introduction | Cover HEAD |
| Local | Remote | Local | Directories, cover, introduction; no local package at the package path | Package HEAD |
| Local | Local | Remote | Directories, cover, package | Introduction HEAD |
| Remote | Remote | Local | Directories, introduction; no local package at the package path | Cover and package HEAD |
| Remote | Local | Remote | Directories, package | Cover and introduction HEAD |
| Local | Remote | Remote | Directories, cover; no local package at the package path | Package and introduction HEAD |
| Remote | Remote | Remote | Skip directory and file checks | HEAD for each of the three resources |

For each local resource, use its own `path` to check parent directories, regular-file status, filename and path consistency, and actual size. Neither the file nor any parent directory may be a symbolic link. "Directories" in the table means each resource's parent directories, not a shared directory inferred from the cover or case name. A `.science` package must have exactly one source: do not retain a local package at the same path when using a remote source. Fully remote entries use only their three URLs as sources and skip local checks as shown above.

Remote HEAD requests must return HTTP 200 with a valid integer `Content-Length` matching the declared size. Redirects with status 301/302/303/307/308 continue to use HEAD. Unreachable resources, timeouts, unsupported HEAD requests, and missing or incorrect sizes all fail validation; there is no GET fallback. Each connection has a 15-second timeout.

The check phase does not download bodies or recompute SHA values. Git declaration checks use the Git object IDs of committed regular files and fail if resource contents change without a corresponding SHA declaration update. This does not prove that the SHA matches the actual contents. Actual size and SHA verification takes place during publication preparation.

## Commands

Run from the repository root. The checkout must match the commit being checked, and the manifest must have no uncommitted changes:

```sh
CASES_JSON="$(python3 .github/scripts/check_structure.py directories --base <BASE_SHA>)" \
  python3 .github/scripts/check_structure.py manifest
python3 .github/scripts/check_structure.py declarations --base <BASE_SHA> --after <HEAD_SHA>
python3 -B -m unittest discover -s .github/tests -v
```

PR checks use the range from the merge base to the fixed PR head. New branches may pass `--new-branch-base`; an all-zero base without a new-branch baseline checks every entry. Publication uses `manifest --plan <PLAN_FILE>` to check entries that differ from the S3 baseline. See [PUBLISHING.md](PUBLISHING.md) for safe publication, staging, and failure recovery.
