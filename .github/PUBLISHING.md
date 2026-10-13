# Case Publication

Publication reads its baseline from `manifest.json` in the target S3 location and compares it with the manifest in the fixed checkout. The Git push range is not the publication baseline. Only an explicit `NoSuchKey` indicates the first publication; permission errors, network failures, invalid JSON, or an invalid index cause preparation to fail.

## Difference rules

Index updates and resource uploads are evaluated separately. Historical S3 indexes support legacy root-level paths and compare missing cover and introduction `release_url` fields as `""`. Legacy entries without an introduction or without both `catalog` and `catalog_name` are also accepted when reading the old index so they can be upgraded. If either classification field is present, both must satisfy the string, conversion, path, and global collision rules; a partially populated classification is invalid. New indexes must follow [CHECKING.md](CHECKING.md). SHA comparisons ignore hexadecimal letter case.

| Change | Publication behavior |
| --- | --- |
| `path` only | Validate the new source path and update the index; do not upload, extract, or delete resources |
| `title` only | Update the index |
| `catalog` / `catalog_name`, optionally with `path` changes | Validate classification and paths, then update the index; do not upload, extract, or delete resources |
| Add `release_url: ""` | Update the index; this is not a source change |
| URL changes from empty to nonempty, to another URL, or from nonempty to empty | Force preparation and upload of the corresponding resource, overriding deduplication |
| `sha256`, `bytes`, or `file_name` | Add the corresponding resource to the candidate list |
| `name` | Look up the new name in the S3 index; compare incrementally if an entry exists, otherwise treat it as new |
| Removal or reordering | Update the index and retain existing resource objects |
| No relevant resource declaration changes | Do not scan objects with HEAD or repair them; still run FINAL_SYNC |

If a new name has only leftover objects, continue normal preparation: validate target covers and introductions according to candidate deduplication rules, and still prepare, upload, and extract the package. Do not skip a case merely because its prefix exists. Objects under an old name remain after that name leaves the index.

S3 keys always derive from `name` and `file_name`, not the repository `path`:

```text
<AWS_TARGET_FOLDER>/<name>/<file_name>
<AWS_TARGET_FOLDER>/<name>/extracted/...
<AWS_TARGET_FOLDER>/manifest.json
```

Source files are located only through each resource's declared repository-relative `path`. Classified resources use a `<catalog>/` prefix with arbitrary depth and separate subdirectories beneath it; unclassified resources retain arbitrary safe paths and do not require a `usecases/` prefix. Local files and all parent directories must still pass safety checks. Category or path changes update only the index and do not change S3 keys.

## Candidates and deduplication

Only candidate covers and introductions that are not marked for forced upload receive a target S3 `HeadObject` check. Upload is skipped only when both the target `Metadata.sha256` and `ContentLength` match. Missing objects, missing metadata, or SHA or size mismatches trigger preparation and upload. A 403, network failure, or other error causes failure and must not be treated as a missing object; only an explicit 404/NoSuchKey/NotFound from HeadObject indicates absence.

Source changes apply consistently to all three resource types: upload is forced even when target metadata matches. For `.science` packages, extraction and replacement are also selected. Packages do not use metadata deduplication. Metadata from the source download URL is not evidence about the target S3 object.

The plan records candidate reasons, `force_upload`, HEAD evidence, upload or skip decisions, and their reasons. Before execution, HEAD is repeated for every skipped item. If any item no longer matches, the entire batch fails before writes begin and the plan must be regenerated.

## Preparation and extraction

The Action controls entry validation, resource preparation, package extraction, and manifest publication separately. Even when no resources are uploaded, it still publishes the required index and runs `FINAL_SYNC`.

Local sources are read from their `path` in the fixed checkout and copied to a temporary directory for the current run; remote sources are downloaded into that directory. Every selected file must match its declared actual size and SHA. No S3 writes are allowed until all files have been prepared successfully and all selected packages have been extracted successfully. Package upload and extraction reuse the same staged file, so a remote package is downloaded only once. Cover, introduction, title, or path changes do not select package extraction.

A `.science` file is a gzipped tar archive. Extraction preserves the original bytes of `session.json`, `records.json`, the package's `manifest.json`, and `README.md`. Resources in the inventory are restored to their corresponding paths under `extracted/` using `storageKey`, with support for `content-dedupe`. The intermediate `objects/` directory is not published, and historical `$DATA/` data is not rewritten. Clients must resolve `$DATA/<storageKey>` to the corresponding extracted URL and encode each path segment.

Extraction rejects path traversal, absolute paths, symbolic links, hard links, special files, duplicate or cross-platform conflicting paths, unsupported formats or features, missing or undeclared files, incorrect sizes or SHA values, and corrupt or truncated gzip data. Before execution, staged contents are verified again and the complete extraction upload inventory is audited against the verified package without extracting it to disk again. Missing items, extra files, and altered metadata are rejected. Candidates and checkpoints are derived again from the fixed commit, rejecting omitted forced uploads, fabricated skips, or tampered plans.

## Checkpoints and writes

Normally, each added or updated case commits its step's manifest only after completing its own resources. If a shared catalog rename or case replacement would create a catalog collision in an intermediate index, combine dependent consecutive operations into an `UPDATE_CATALOG` checkpoint. Commit only once the complete mapping is valid; the checkpoint's before/after values list the affected cases. All selected group resources must finish before the index is committed, so failures retain a valid baseline for a fresh plan. This does not make multi-resource writes atomic.

The sequence is:

1. Confirm that the S3 baseline has not changed. If the package is selected, clear only `<name>/extracted/`.
2. Upload the case's selected resources and extracted files. Write `sha256` metadata computed from the actual uploaded bytes, then verify the size and metadata with HEAD.
3. Write the root manifest conditionally: use the `If-Match` ETag for an existing object, or `If-None-Match: *` for the first write.
4. Read back the manifest and verify that its raw text matches. Wait for this step's CDN invalidation to finish before proceeding to the next step.
5. Finally, `FINAL_SYNC` writes the manifest's original bytes from the fixed commit as a separate step, reads it back, and invalidates only the manifest's CDN path.

Steps that upload resources invalidate the manifest and the case's `<name>/*` path. Steps without resource uploads, including `FINAL_SYNC`, invalidate only the manifest. Every step still waits for invalidation to finish; the entire publication prefix is no longer invalidated.

`UPDATE_CATALOG` processes resources one case at a time: clear that case's extracted prefix only if its package is selected, then upload and verify all of its selected originals and extracted files before starting the next case. A failure leaves later cases' resources untouched. Removed cases' resources are retained, and the group manifest is committed only after every case succeeds. In name order, invalidate only cases with actual uploads; each request includes the manifest and that case's `<name>/*` and waits for completion. Cases in the group without uploads do not have their resource caches invalidated. Classification/path-only groups invalidate only the index. Operations without catalog collisions retain individual case checkpoints.

Removal, reordering, and index-only steps do not clean up resources. The trailing `/` in the cleanup prefix prevents accidental deletion of similarly named prefixes. Conditional conflicts fail without falling back to unconditional writes. Only an ambiguous transport failure permits a read-back check to determine whether PUT completed. ETag is used for version conditions, not as a content SHA.

The serial workflow lock covers the interval from reading the baseline through final publication. It does not make writes across multiple objects atomic: files may be briefly absent during package replacement, and objects uploaded successfully before a failure remain in place. All publishers must honor the same lock.

## Evidence, failures, and recovery

`publication-plan.json` and its corresponding directory store the baseline, candidates, decisions, complete plan, per-step manifests, file lists, before-and-after entries, `status.json`, `events.jsonl`, and `summary.md`. Actions always save the evidence artifact for 14 days, without uploading staged bodies. Logs also show deduplication evidence; URLs should not contain credentials.

Step status is `waiting`, `uploading`, `completed`, or `failed`, with separate records for manifest commitment, read-back verification, and CDN status. Any validation, preparation, extraction, deletion, upload, read-back, or CDN failure stops processing immediately. FINAL_SYNC is not run after a failure. If the process is terminated, status may remain `uploading`; recovery still uses S3 as the source of truth.

For example, if the first two cases complete and the third uploads but fails to write the index, a new run reads the checkpoint containing the first two cases and processes only the remaining differences. The third case's cover and introduction may be deduplicated using target metadata, but source changes still force upload, and its package is prepared and extracted again. If the index was committed but CDN invalidation failed, the new run's `FINAL_SYNC` only retries invalidation of the manifest; it does not automatically invalidate resource caches for cases that were already committed. Use the failed run's CDN path logs to issue a separate invalidation for each affected case and confirm completion. If the request was accepted but waiting failed, first check the actual status of that invalidation request.

Catalog groups stop invalidating on the first failure, so remaining cases may have no CDN path log even though their resources were uploaded and the index was committed. Obtain all uploaded case prefixes from the failed group's `steps/*/files.json`, check completed invalidation requests, and individually complete the missing case invalidations.

After fixing the cause, start a new `workflow_dispatch` on main; do not use native Re-run jobs. The scripts and Action reject `GITHUB_RUN_ATTEMPT != 1`. Each new run uses a newly fixed SHA, fresh staging, and a fresh S3 baseline. Never reuse an old plan whose extraction has completed to retry extraction. The concurrency queue does not guarantee commit ancestry order; if an older target is published from the queue, dispatch the current main again afterward.

There is no proactive object repair or garbage collection. Unchanged declarations will not reveal manually deleted objects, and reverting declarations does not guarantee repair of object changes left by a failed batch. Arrange explicit resource repair separately when needed.

## usecases migration acceptance

Move directories as a whole, preserving resource contents, filenames, sizes, SHA values, names, and titles. Change only `path` and add empty URL fields. Use the pre-migration index as the fake S3 baseline and prove that the resource candidate/upload, package extraction, and S3 deletion lists are all empty. After the new manifest is written, its read-back must match, and existing resource keys and bytes must remain unchanged.

The classification upgrade only adds `catalog: ""` and `catalog_name: ""` to existing cases, preserving `usecases/`, every resource path, and resource metadata. Historical S3 indexes may omit both fields. This upgrade also changes only the index and selects no resource operations.

## Local validation

```sh
python3 -B -m unittest discover -s .github/tests -v
```

Tests use temporary Git repositories, local HTTP, and fake S3 without accessing production AWS. Coverage includes HEAD without GET, source combinations and switches, incremental candidates, metadata deduplication, preparation integrity, extraction safety, plan tampering, cleanup scope, per-case failure recovery, and index writes for path migrations. Actual Actions permissions, AWS/CDN behavior, and compatibility with production consumers still require separate post-merge verification; passing local tests does not mean live publication has run.
