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
| `release_url` | An empty string selects the local file; a nonempty value must use one of the two HTTPS repository prefixes listed below |

- The `release_url` allowlist applies to all three resources and currently contains exactly `https://github.com/aipoch/open-science-usecases/` (the upstream main repository, not a fork) and `https://huggingface.co/datasets/AIPOCH-AI/open-science-usecases/`. Use a direct resource URL under one of these prefixes. Other hosts, repositories, HTTP URLs, lookalike prefixes, credentials, alternate ports, and literal or encoded path traversal are forbidden. The allowlist applies to the declared URL; normal download redirects to the providers' storage/CDN hosts remain supported.

- Each local source requires an existing regular file at its `path` and existing parent directories. Neither the file nor any parent directory may be a symbolic link. Fully remote entries do not require local directories. A `.science` package must have exactly one source; do not keep a local file at the same path when the package is remote.
- Introductions must be nonempty and accurately describe the case. Read the actual introduction before completing an addition; do not substitute an empty document, placeholder text, or README. Remote introductions must also undergo content review before upload.
- In case Markdown files, use complete absolute HTTP(S) URLs for links and image sources, including reference-style links and HTML attributes. Do not use relative paths, root-relative paths, protocol-relative URLs, or local filesystem paths. Do not list or embed links to the `.science` package or the case cover; those resources are already declared in `manifest.json`.
- Once the content is final, compute the size and SHA of all three resources from the actual files on the user's device. For remote resources, also compute these values from the local originals before uploading. Do not reuse another file's digest or guess values; recompute them whenever the content changes.

```sh
wc -c < 'usecases/directory/filename'
shasum -a 256 'usecases/directory/filename'
```

- Every published `.science` filename must replace spaces with hyphens (`-`), including the final segment of remote download URLs. Do not rename case titles, stable IDs, parent directories or package internals for this rule. Follow [UPLOADING.md](UPLOADING.md); run `python3 .github/scripts/check_package_names.py` before submission.

# Adding and updating videos

Each case may have one `video` object; omit it when unavailable, never use null or placeholders. Existing resource rules remain unchanged. Require `type` (`s3`, `external` or `youtube` only), `file_path` and `file_name`; do not add `media_platform`, `internal_path` or `external_url`.

| `type` | `file_path` | `file_name` | Required integrity fields | Action check |
| --- | --- | --- | --- | --- |
| `s3` | `{case.name}/{file_name}` under the fixed S3 prefix below | Actual filename matching the final segment | Positive integer `bytes`; 64 hexadecimal digits in `sha256` | HEAD size and custom `Metadata.sha256` match |
| `external` | Public HTTPS video-file URL | Actual filename; download routes need not end with it | Positive integer `bytes`; no SHA requirement | HEAD: 200, `video/*`, matching Content-Length |
| `youtube` | Supported single-video HTTPS URL | User-provided display name; extension optional | Neither bytes nor SHA | Platform metadata identifies the requested video |

- Upload internal videos only to `s3://statics-aipochcom-prod/open-science/usecases/{case.name}/{file_name}`. Use the manifest's kebab-case `name`, not title, catalog or local directory. Reject traversal, encoded segments, subdirectories and resource-name collisions. Keep filenames without adding hashes.
- Filenames/display names must be nonempty, without separators or control characters. S3/external extensions: `.mp4`, `.webm`, `.mov`, `.m4v`, `.avi`, `.mkv`, `.ogv`, `.mpeg`, `.mpg`.
- Generate internal video metadata from the actual local file: `python3 .github/scripts/video_resources.py metadata --case <manifest-name> /absolute/path/to/video.mp4`. Never guess size/SHA; recompute after content changes.
- Upload through available local S3 credentials and a CLI/SDK; an S3 skill is optional. If credentials are unavailable, tell the user to prepare them. Never print/commit credentials or claim an unsuccessful upload succeeded.
- Set the correct Content-Type and custom `sha256=<local-SHA-256>` metadata. HEAD the uploaded object and match size/SHA before recording it in the manifest. Do not substitute ETag/multipart checksums or download S3 content to rehash.
- Overwrites require updated size/SHA, metadata and CDN refresh. A video upload does not authorize shared-index publication or other-object deletion; removing its declaration never deletes the object.
- External URLs require public HTTPS without credentials or fragments; checks never download video bodies or validate SHA. YouTube accepts `watch?v=`, `youtu.be/`, `shorts/`, `embed/` and `live/`; an HTML page's HTTP 200 alone is insufficient.

See [VIDEOS.md](.github/VIDEOS.md) for upload commands and examples.

# Pre-commit checks

Check fields and types, unique names, catalog conversions and global collisions, resource types, safe paths, filenames, actual sizes, SHA values, source selection, and the release URL allowlist across the entire manifest. Review case Markdown for absolute URLs and the absence of package and cover links. Classification migrations update catalog fields and paths; preserve resource contents and all other metadata. Follow Conventional Commits.

Run `python3 -B -m unittest discover -s .github/tests -v` with Python 3.11+ and the [validation commands](.github/CHECKING.md#commands) against the submission target. Checks neither fetch resource bodies nor recompute SHA: YouTube uses bounded metadata; S3 videos compare custom SHA metadata. Publication preparation verifies actual file SHA only for the existing three resources.

See [.github/CHECKING.md](.github/CHECKING.md) for complex source combinations and HEAD behavior. See [.github/PUBLISHING.md](.github/PUBLISHING.md) for S3 baselines, differences, forced uploads, deduplication, staging, extraction, checkpoints, failure recovery, and migration acceptance. Tests must use temporary Git repositories, local HTTP, and fake S3 only. Do not perform live publication without user authorization.
