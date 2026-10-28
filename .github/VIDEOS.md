# Case videos

An optional `video` references an available resource. See [AGENTS.md](../AGENTS.md#adding-and-updating-videos) for required fields, filenames and URL rules; existing cases need no migration.

## Internal S3 video

Upload only to `s3://{bucket name}/open-science/usecases/{case.name}/{file_name}`, using the stable manifest name and ordinary filename. Keep video files out of Git; catalog path rules do not apply.

Generate the video JSON from the local file:

```sh
python3 .github/scripts/video_resources.py metadata --case example-case /absolute/path/demo.mp4
```

This prints all five fields, including measured `bytes` and `sha256`, without uploading or editing the manifest. Files and parent directories must not be symlinks. Never use example sizes or hashes.

Use local AWS credentials or a named profile; an S3 skill is optional. If credentials are missing, advise the user to prepare them. Install any needed pinned SDK in a task-local virtual environment.

For an authorized upload, replace `bucket name` with the Action's internal-video bucket:

```sh
# Use the actual file and existing manifest case name.
video_bucket='bucket name'
video_file='/absolute/path/demo.mp4'
video_case='example-case'
video_name=$(basename "$video_file")
video_sha=$(shasum -a 256 < "$video_file" | awk '{print $1}')
video_bytes=$(wc -c < "$video_file" | tr -d '[:space:]')
aws s3 cp "$video_file" "s3://$video_bucket/open-science/usecases/$video_case/$video_name" \
  --content-type video/mp4 --metadata "sha256=$video_sha" --only-show-errors
aws s3api head-object --bucket "$video_bucket" \
  --key "open-science/usecases/$video_case/$video_name" \
  --query '{bytes:ContentLength,sha256:Metadata.sha256}' --output json
```

Set Content-Type to match the file. Compare HEAD's `bytes` and `sha256` with `$video_bytes` and `$video_sha`; add the generated JSON to the manifest only when both match. This trusts custom upload metadata, without remote rehashing or ETag/multipart checksum substitution.

For overwrites, regenerate metadata, update the declaration and refresh CDN. Publication refreshes the case prefix only when the internal-video declaration changes; otherwise refresh explicitly. Uploading alone does not publish the shared manifest.

## External direct video

Set `type: "external"`, actual `file_name`, public HTTPS file URL in `file_path`, and measured `bytes`. Get the size from `wc -c < /absolute/path/demo.mp4` or remote HEAD Content-Length. No SHA is required or checked; player pages are not direct files.

HEAD must return 200, `video/*` and matching Content-Length. Bounded HTTPS redirects preserve HEAD; private/special-use addresses, credentials and nonstandard ports are rejected. There is no GET fallback.

## YouTube

```json
{
  "video": {
    "type": "youtube",
    "file_path": "https://www.youtube.com/watch?v=VIDEO_ID",
    "file_name": "Case demonstration"
  }
}
```

Use a real single-video ID and a display name; omit `bytes` and `sha256`. Supported links: `watch?v=`, `youtu.be/`, `shorts/`, `embed/`, `live/`. Playlists alone and other platforms are unsupported.

The probe validates the requested ID against at most 64 KiB of YouTube oEmbed metadata. It confirms metadata availability, not universal playback. Private, unavailable or embedding-disabled videos may fail; rate limits/network errors mean probe failure, not confirmed deletion.

## Checks and publication

[CHECKING.md](CHECKING.md#commands) covers global schema validation, changed-video probes and fork-PR deferrals. Workflow AWS secrets need HEAD access to the fixed video prefix. [PUBLISHING.md](PUBLISHING.md#video-references) covers mandatory publication checks, failure retention and CDN refresh.

Video-only changes trigger no package upload/extraction; removing a reference never deletes its object. Existing resource allowlists, concurrency and conditional-write guarantees remain unchanged.
