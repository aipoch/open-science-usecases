# Case upload naming rules

Effective 2026-10-22, every published `.science` filename must use hyphens (`-`) in place of spaces. Apply this to the final filename only, including when a package is remotely hosted. Example: `Can We Reproduce Chinchilla Scaling.science` becomes `Can-We-Reproduce-Chinchilla-Scaling.science`.

- Replace each ASCII space with one hyphen; do not rewrite the case title, stable case `name`, category, parent directories, other punctuation or extension as part of this rule. New uploads must not contain whitespace in the `.science` filename.
- Rename the outer file without unpacking, repacking or editing its internal `session.json`, records, metadata or inventory. Its byte size and SHA-256 must remain identical after renaming.
- Update `case.file_name` and the final filename in `case.path` in `manifest.json`. Keep `file_name` equal to the final path segment. Verify the actual size and SHA-256.
- If `case.release_url` is nonempty, use a working allowed HTTPS source. A Hugging Face URL should pin the revision where the renamed file exists. Preserve external historical release assets that already have whitespace-free filenames; do not rewrite a URL to a nonexistent asset.
- Keep poster and introduction names unchanged unless separately requested. Update repository examples and download instructions that name the renamed package.
- Before upload, check all indexed and locally published `.science` filenames for whitespace, naming collisions, actual size/SHA, source selection and download availability.
- Old URLs remain accessible using historical Git/Hugging Face revisions. Current-branch links using the former filename need the renamed path.

Website publication uses `name` and `file_name` to construct object keys. Changing a package filename therefore schedules that resource for upload/extraction under the repository's existing publication rules. Source-repository updates and a submitted PR are not proof of completed website publication.
