# Case videos

`video` is optional. Its `type` selects the interpretation of `file_path` and the checks; `file_name` is always required. Existing cases do not need migration. The video is a reference to an already available resource, not a fourth automatically uploaded publication source.

## Internal S3 video

The only destination is `s3://statics-aipochcom-prod/open-science/usecases/{case.name}/{file_name}`. Use the manifest's stable case name. Ordinary filenames are retained. Files are not added to Git, and internal video paths do not follow the catalog directory rules for the other resources.

Measure the actual file and generate a complete video object:

```sh
python3 .github/scripts/video_resources.py metadata --case example-case /absolute/path/demo.mp4
```

The command reads the file and prints JSON containing `type`, `file_path`, `file_name`, actual `bytes`, and actual `sha256`. It does not upload, change manifest.json, or print credentials. Files and parent directories cannot be symlinks. Do not copy illustrative sizes or hashes into the manifest.

Use existing local AWS credentials (a named AWS profile is also supported); an S3 skill is optional. If credentials are unavailable, tell the user and recommend preparing them. Install the repository's pinned SDK in a task-local virtual environment if needed, not in a shared Python environment.

After the upload has been authorized, the equivalent AWS CLI operations are:

```sh
# Set these to the real file, existing case name and measured metadata.
video_file='/absolute/path/demo.mp4'
video_case='example-case'
video_name=$(basename "$video_file")
video_sha=$(shasum -a 256 < "$video_file" | awk '{print $1}')
video_bytes=$(wc -c < "$video_file" | tr -d '[:space:]')
aws s3 cp "$video_file" "s3://statics-aipochcom-prod/open-science/usecases/$video_case/$video_name" \
  --content-type video/mp4 --metadata "sha256=$video_sha" --only-show-errors
aws s3api head-object --bucket statics-aipochcom-prod \
  --key "open-science/usecases/$video_case/$video_name" \
  --query '{bytes:ContentLength,sha256:Metadata.sha256}' --output json
```

Choose the correct Content-Type for non-MP4 files. Compare **both** returned values with the local measurements; only record the generated video object after they match. Never replace a failed upload or missing metadata with a successful declaration. Do not use ETag or S3 multipart checksum fields as the file SHA. The check verifies stored declarations, not an independent re-hash of S3 content.

When overwriting the same key, regenerate metadata, update the video declaration and refresh its CDN cache. A subsequent publication with a changed internal video declaration refreshes the case prefix. If the declaration is unchanged, arrange any needed cache refresh explicitly. Uploading a video does not publish the shared manifest.

## External direct video

Use `type: "external"`, an actual video `file_name`, a complete public HTTPS video URL in `file_path`, and the file's measured `bytes`. Obtain the size from the local original with `wc -c < /absolute/path/demo.mp4`, or the actual remote HEAD Content-Length, and have the check confirm it. No SHA is required or checked. Do not use a web player page as a direct file URL.

HEAD must return HTTP 200, `video/*` Content-Type and the declared Content-Length. HTTPS redirects preserve HEAD and are bounded; private/special-use network targets, credentials and nonstandard ports are rejected. Servers without suitable HEAD responses fail without a GET fallback.

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

Replace `VIDEO_ID` with the real single-video ID. `file_name` is a user-provided display name, not a claim about a downloadable filename. `bytes` and `sha256` are not needed. Do not include them in new YouTube declarations. `watch?v=`, `youtu.be/`, `shorts/`, `embed/` and `live/` links are supported; playlists alone and other platforms are not.

The check requests up to 64 KiB of YouTube oEmbed metadata and verifies a video response identifying the requested ID. This confirms metadata availability at check time, not playback in every country or browser. Private, unavailable or embedding-disabled videos may not be probeable. Rate limits and network failures are reported as failed probes rather than as success or definitive deletion.

## Checks and publication

Run the commands in [CHECKING.md](CHECKING.md). All video schemas are checked globally, while remote probes select changed video declarations. Untrusted fork PRs explicitly defer S3 probes, with a step-summary notice; trusted publication never permits this skip. Repository AWS secrets must be referenced by the workflow and have permission to HEAD the fixed video bucket/prefix.

Video changes never cause `.science` uploads or extraction by themselves. Failed video checks keep the previous case declaration, and removing a video declaration does not delete its object. Existing resource source allowlists and publication concurrency/conditional-write guarantees remain unchanged.
