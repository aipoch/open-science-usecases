# Adding and updating cases

- The root `manifest.json` is an array. Add exactly one entry for each new case, containing `title`, a unique kebab-case `name`, `catalog`, `catalog_name`, `cover`, `case`, and `introduction`. Do not change the schema to accommodate missing data.
- `title` is the display title; `name` is the stable identifier and S3 prefix. Neither has to match the directory name. Locate resources by their individual `path` values. Classified resources may use arbitrary subdirectories within their catalog; resources need not share a subdirectory. Unclassified resources retain arbitrary safe relative paths.
- `catalog` and `catalog_name` must both be strings. Two empty strings (`""`) mean unclassified; missing fields, null, whitespace-only values, or filling only one field are invalid. Existing unclassified cases stay under `usecases/` without moving files or changing paths.
- A nonempty `catalog` is both the display label and a classification directory at the repository root. All three resource paths, including remote resources, must start with the literal `<catalog>/`, not `catalog_name`. Spaces, letter case, and punctuation are allowed, but separators, control characters, `.`, `..`, and drive-letter paths are not. Fully remote cases still need no local directory.
- Derive `catalog_name` as ASCII kebab-case: split PascalCase/camelCase and acronym word boundaries, lowercase, collapse consecutive non-alphanumeric characters to `-`, and trim leading/trailing `-`. For example, `Data Science`, `DataScience`, and `Data_Science` all become `data-science`. Reject non-ASCII names or an empty conversion and ask the user to rename the catalog; never translate, transliterate, remove accents, or silently drop unsupported characters. Do not supply an identifier that differs from the conversion.
- Check the entire manifest's catalog mapping. Multiple cases may reuse the same catalog. Different catalogs with the same converted `catalog_name` must produce an error listing both names and the conflicting identifier; never append a number automatically. Case `name` values remain globally unique across catalogs.
- All three resources must contain the five fields below, including fully remote resources. The cover must be an image, the package a `.science` file, and the introduction a `.md` file.

| Field | Meaning |
| --- | --- |
| `file_name` | Actual filename, matching the final segment of `path` |
| `path` | Safe repository-relative path, such as `usecases/physics/example/cover.png` or `covers/cover.png`; required for remote sources as well |
| `bytes` | Actual file size in bytes, as a nonnegative integer |
| `sha256` | Actual file SHA-256, exactly 64 hexadecimal characters with no whitespace |
| `release_url` | An empty string selects the local file; a nonempty value selects an HTTP(S) remote resource |

- Each local source requires an existing regular file at its `path` and existing parent directories. Neither the file nor any parent directory may be a symbolic link. Fully remote entries do not require local directories. A `.science` package must have exactly one source; do not keep a local file at the same path when the package is remote.
- Introductions must be nonempty and accurately describe the case. Read the actual introduction before completing an addition; do not substitute an empty document, placeholder text, or README. Remote introductions must also undergo content review before upload.
- Once the content is final, compute the size and SHA of all three resources from the actual files on the user's device. For remote resources, also compute these values from the local originals before uploading. Do not reuse another file's digest or guess values; recompute them whenever the content changes.

```sh
wc -c < 'usecases/directory/filename'
shasum -a 256 'usecases/directory/filename'
```

# Pre-commit checks

Check fields and types, unique names, catalog conversions and global collisions, resource types, safe paths, filenames, actual sizes, SHA values, and source selection. Classification migrations update catalog fields and paths; preserve resource contents and all other metadata. Follow Conventional Commits.

Run `python3 -B -m unittest discover -s .github/tests -v`. Run the [validation commands](.github/CHECKING.md#commands) against the target being prepared for submission. The check phase does not download bodies or recompute SHA values; it only checks formatting, remote HEAD responses, sizes, and consistency between Git objects and declarations. Actual SHA verification takes place during publication preparation.

See [.github/CHECKING.md](.github/CHECKING.md) for complex source combinations and HEAD behavior. See [.github/PUBLISHING.md](.github/PUBLISHING.md) for S3 baselines, differences, forced uploads, deduplication, staging, extraction, checkpoints, failure recovery, and migration acceptance. Tests must use temporary Git repositories, local HTTP, and fake S3 only. Do not perform live publication without user authorization.
