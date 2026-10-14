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

The plan records candidate reasons, `force_upload`, HEAD evidence, upload or skip decisions, and their reasons. Before execution, HEAD is repeated for every skipped item. If any item no longer matches, its case or dependent catalog group fails before writes begin; unrelated cases continue.

## Preparation and extraction

The Action controls entry validation, resource preparation, package extraction, and manifest publication separately. Even when no resources are uploaded, it still publishes the required index and runs `FINAL_SYNC`.

Local sources are read from their `path` in the fixed checkout and copied to a temporary directory for the current run; remote sources are downloaded into that directory. Every selected file must match its declared actual size and SHA. Each independent case is checked, prepared, extracted and verified before any writes to that case. A failure in one case does not prevent other cases from publishing. A dependent catalog group must prepare and verify all of its resources before any writes to the group. Package upload and extraction reuse the same staged file, so a remote package is downloaded only once. Cover, introduction, title, or path changes do not select package extraction.

A `.science` file is a gzipped tar archive. Extraction preserves the original bytes of `session.json`, `records.json`, the package's `manifest.json`, and `README.md`. Resources in the inventory are restored to their corresponding paths under `extracted/` using `storageKey`, with support for `content-dedupe`. The intermediate `objects/` directory is not published, and historical `$DATA/` data is not rewritten. Clients must resolve `$DATA/<storageKey>` to the corresponding extracted URL and encode each path segment.

Extraction rejects path traversal, absolute paths, symbolic links, hard links, special files, duplicate or cross-platform conflicting paths, unsupported formats or features, missing or undeclared files, incorrect sizes or SHA values, and corrupt or truncated gzip data. Before execution, staged contents are verified again and the complete extraction upload inventory is audited against the verified package without extracting it to disk again. Missing items, extra files, and altered metadata are rejected. Candidates and checkpoints are derived again from the fixed commit, rejecting omitted forced uploads, fabricated skips, or tampered plans.

## Checkpoints and writes

Normally, each added or updated case commits its step's manifest only after completing its own resources. If a shared catalog rename or case replacement would create a catalog collision in an intermediate index, combine dependent operations, including nonconsecutive ones, into an `UPDATE_CATALOG` checkpoint. Unrelated operations remain independent. Commit only once the complete mapping is valid; the checkpoint's before/after values list the affected cases. All selected group resources must finish before the index is committed, so failures retain a valid baseline for a fresh plan. This does not make multi-resource writes atomic.

The default execution has **4 case workers and 8 file workers per case**, up to 32 simultaneous resource transfers. Repository Actions variables `CASE_UPLOAD_WORKERS` and `FILE_UPLOAD_WORKERS` (or the corresponding `--case-workers` / `--file-workers` CLI options) control these limits. Valid values are 1–16 case workers and 1–32 file workers, with a product of at most 64. These are starting values, not a measured production optimum. Compare throughput, CPU, memory and retries before raising them.

Workers share one Boto3 S3 client/connection pool. Each file task uploads with its own SHA metadata and verifies the resulting size and metadata with HEAD. Managed multipart uploads retain large-file support; nested SDK transfer threads are disabled, so the file-worker limit also bounds in-flight transfer requests. Install the pinned SDK with `python3 -m pip install -r .github/scripts/requirements.txt`. Global index reads/writes and CDN operations continue to use the AWS CLI.

The sequence is:

1. Validate the fixed target and the shared S3 baseline before starting workers.
2. Each worker checks source availability, prepares and verifies resources, extracts its packages, and audits the extracted inventory before modifying its case. If a package is selected, clear only that case's `<name>/extracted/` prefix.
3. Upload and HEAD-verify files concurrently within the case. Bound both active tasks and the submission window. On failure, stop submitting files, cancel queued work and wait for in-flight requests; already-started requests can still finish.
4. The single coordinator processes ready cases, checks that the S3 baseline has not changed, and conditionally commits a new index derived from the **last accepted index plus that successful operation**. It uses `If-Match` or `If-None-Match: *`, reads back the exact bytes and waits for the checkpoint's CDN invalidation. Workers never write the shared manifest. Ready cases may commit in completion order.
5. Case-local source, preparation, extraction, upload or HEAD failures are recorded and independent cases continue. A failed addition is excluded from the index; a failed update retains its old entry. Structural/plan validation errors and shared-index conflicts or unknown commit outcomes stop the run; no further cases are scheduled and in-flight work is drained.
6. If every case operation's manifest was verified, reordering and FINAL_SYNC restore the fixed target's exact bytes. Otherwise these steps are explicitly skipped so they cannot accidentally publish failed cases. After processing independent cases, any failure still makes the job fail.

`UPDATE_CATALOG` remains a dependent commit unit: the global catalog mapping can make individual case changes invalid (for example `Data Science` to `DataScience`, both mapping to `data-science`). Its resources are prepared together, then uploaded one case at a time, with bounded file concurrency. A failure prevents that group's index commit and leaves later cases in the group untouched; **unrelated groups continue**. This preserves the existing classification contract without changing the public manifest schema.

Steps that upload resources invalidate the manifest and the case's `<name>/*` path. Other steps invalidate only the manifest. Each request waits for completion. For catalog groups, all uploaded case paths are attempted and individually recorded, even if one invalidation fails. A CDN failure after a verified manifest commit does not roll back that commit or block unrelated cases; it is reported as committed/verified with CDN failed. The final job still fails.

Removal, reordering, and index-only steps do not clean up resources. The trailing `/` in the cleanup prefix prevents accidental deletion of similarly named prefixes. Conditional conflicts fail without falling back to unconditional writes. Only an ambiguous transport failure permits a read-back check to determine whether PUT completed. ETag is used for version conditions, not as a content SHA.

The serial workflow lock covers the interval from reading the baseline through final publication. It does not make writes across multiple objects atomic: files may be briefly absent during package replacement, and objects uploaded successfully before a failure remain in place. All publishers must honor the same lock.

## Evidence, failures, and recovery

`publication-plan.json` and its corresponding directory store the baseline, candidates, decisions, complete plan, per-step manifests, file lists, before-and-after entries, `status.json`, `events.jsonl`, and `summary.md`. Actions always save the evidence artifact for 14 days, without uploading staged bodies. Full deduplication evidence is in each step's `resource-decisions.json`; URLs should not contain credentials. `applied-manifest.json` records the actual commit body, which can differ from the planned manifest after case failures or out-of-order completion.

Step status is `waiting`, `preparing`, `uploading`, `ready`, `completed`, `failed`, or `skipped`, with separate records for manifest commitment, read-back verification, and CDN status. Case-local failures do not stop unrelated cases. Global validation and shared-manifest failures stop the run. FINAL_SYNC runs only when every case operation has a verified manifest commit; it may run after a case CDN failure. If the process is terminated, status may remain `uploading`; recovery still uses S3 as the source of truth.

For example, if the first two cases complete and the third uploads but fails to write the index, a new run reads the checkpoint containing the first two cases and processes only the remaining differences. The third case's cover and introduction may be deduplicated using target metadata, but source changes still force upload, and its package is prepared and extracted again. If the index was committed but CDN invalidation failed, the new run's `FINAL_SYNC` only retries invalidation of the manifest; it does not automatically invalidate resource caches for cases that were already committed. Use the failed run's CDN path logs to issue a separate invalidation for each affected case and confirm completion. If the request was accepted but waiting failed, first check the actual status of that invalidation request.

After fixing the cause, start a new `workflow_dispatch` on main with `dry_run: false`; do not use native Re-run jobs. The scripts and Action reject `GITHUB_RUN_ATTEMPT != 1`. Each new run uses a newly fixed SHA, fresh staging, and a fresh S3 baseline. Never reuse an old plan whose extraction has completed to retry extraction. The concurrency queue does not guarantee commit ancestry order; if an older target is published from the queue, dispatch the current main again afterward.

There is no proactive object repair or garbage collection. Unchanged declarations will not reveal manually deleted objects, and reverting declarations does not guarantee repair of object changes left by a failed batch. Arrange explicit resource repair separately when needed.

## usecases migration acceptance

Move directories as a whole, preserving resource contents, filenames, sizes, SHA values, names, and titles. Change only `path` and add empty URL fields. Use the pre-migration index as the fake S3 baseline and prove that the resource candidate/upload, package extraction, and S3 deletion lists are all empty. After the new manifest is written, its read-back must match, and existing resource keys and bytes must remain unchanged.

The classification upgrade only adds `catalog: ""` and `catalog_name: ""` to existing cases, preserving `usecases/`, every resource path, and resource metadata. Historical S3 indexes may omit both fields. This upgrade also changes only the index and selects no resource operations.

## Local validation

```sh
python3 -B -m unittest discover -s .github/tests -v
```

Actions console output contains counts, case/phase transitions, failures and progress approximately every 10 seconds. Full file events are appended to `events.jsonl`. A lock serializes journal/snapshot writes; full `status.json` snapshots are written at boundaries, failures and approximately every 5 seconds during file activity. On abrupt termination a snapshot may lag the journal. The job summary shows verified files/bytes, elapsed time, manifest acceptance/read-back and CDN outcomes. No per-file success JSON or repeated complete inventories are printed to the console.

The manually dispatched workflow defaults to `dry_run: true`, runs the actual publisher's tests with local HTTP/fake S3, and has no production AWS credentials. PR CI runs the same publication test suite. Explicitly choose `dry_run: false` only for an authorized publication on main.

Historical baseline readers remain unchanged. Public manifest fields, stable object keys and package bytes do not change; no data migration or reupload is needed. Existing case updates still overwrite stable keys, so a failed case may be partially replaced even while its previous index entry is retained. This change isolates other cases; it does not add rollback or versioned resource storage. Old run plans/staging are not resumable, and diagnostic status values/console format have expanded.

Tests use temporary Git repositories, local HTTP, and fake S3 without accessing production AWS. Coverage includes HEAD without GET, source combinations and switches, incremental candidates, metadata deduplication, preparation integrity, extraction safety, plan tampering, cleanup scope, per-case failure recovery, and index writes for path migrations. Actual Actions permissions, AWS/CDN behavior, and compatibility with production consumers still require separate post-merge verification; passing local tests does not mean live publication has run.
