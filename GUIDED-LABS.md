# Guided 3D labs

The gallery discovers projects in the `3D Lab` catalog. Each project folder includes its introduction, a listing cover, an opening screenshot, and a `lab.json` descriptor for its guided player.

## Published files

| Object under `open-science/usecases/<case.name>/` | Purpose |
| --- | --- |
| `lab.json` | Declares the entry document, opening screenshot, prompt and scene assets. |
| Files named by `entry`, `screenshot`, `prompt` and `assets` | The player resolves these filenames relative to its descriptor. Preserve each file’s exact bytes and MIME type. |
| `introduction.mp4` | The guided film identified by the catalog’s S3 video declaration. Playback uses HTTP byte ranges. |
| The catalog cover, introduction and native archive | The existing case publisher copies these resources and extracts the native session. The viewer reads the published archive for save and import. |

Publish the supplemental objects and films before exposing the cases in the catalog. The standard publisher handles the catalog resources. The descriptor and its scene files need a separate copy to the same public case directory. Use the resource byte counts and SHA-256 values for verification.

## Backend handoff

Start from the five `3D Lab` entries in [the root manifest](manifest.json). The source folders use display names. Build every destination key with the stable `name` from the manifest. The table links each descriptor in Git and its matching film at a pinned revision of the public dataset.

| Source folder and descriptor | Published case directory | Film source |
| --- | --- | --- |
| [Black Hole Observatory](3D%20Lab/Black%20Hole%20Observatory/lab.json) | `black-hole-observatory` | [MP4](https://huggingface.co/datasets/AIPOCH-AI/open-science-usecases/resolve/aa030b4a40a2db71e8c0ef589189ce0720a20b9a/3D%20Lab/Black%20Hole%20Observatory/introduction.mp4) |
| [Mendel Laboratory](3D%20Lab/Mendel%20Laboratory/lab.json) | `mendel-laboratory` | [MP4](https://huggingface.co/datasets/AIPOCH-AI/open-science-usecases/resolve/aa030b4a40a2db71e8c0ef589189ce0720a20b9a/3D%20Lab/Mendel%20Laboratory/introduction.mp4) |
| [Pelican Bicycle Studio](3D%20Lab/Pelican%20Bicycle%20Studio/lab.json) | `pelican-bicycle-studio` | [MP4](https://huggingface.co/datasets/AIPOCH-AI/open-science-usecases/resolve/aa030b4a40a2db71e8c0ef589189ce0720a20b9a/3D%20Lab/Pelican%20Bicycle%20Studio/introduction.mp4) |
| [PTP1B Molecular Laboratory](3D%20Lab/PTP1B%20Molecular%20Laboratory/lab.json) | `ptp1b-molecular-laboratory` | [MP4](https://huggingface.co/datasets/AIPOCH-AI/open-science-usecases/resolve/aa030b4a40a2db71e8c0ef589189ce0720a20b9a/3D%20Lab/PTP1B%20Molecular%20Laboratory/introduction.mp4) |
| [The Riemann Classroom](3D%20Lab/The%20Riemann%20Classroom/lab.json) | `riemann-classroom` | [MP4](https://huggingface.co/datasets/AIPOCH-AI/open-science-usecases/resolve/aa030b4a40a2db71e8c0ef589189ce0720a20b9a/3D%20Lab/The%20Riemann%20Classroom/introduction.mp4) |

For example, copy `3D Lab/Pelican Bicycle Studio/lab.json` to `open-science/usecases/pelican-bicycle-studio/lab.json`. For each resource declared in `entry`, `prompt`, `screenshot` and `assets[]`, read its repository-relative `path` and copy the exact bytes to `open-science/usecases/<case.name>/<file_name>`. The five descriptors and their 47 declared files make 52 supplemental objects. The five MP4s bring the total to 57.

The five `video.type` values are `s3`. Read each film from the pinned dataset link above and publish it at `open-science/usecases/<video.file_path>` with `Content-Type: video/mp4` and the custom `sha256` metadata declared in the root manifest. Each player loads `introduction.mp4` relative to its own `index.html`. The repository excludes MP4 files from Git.

Before exposing the five entries in the public catalog, verify the following from the public static origin.

1. Read each `<case.name>/lab.json`. Check the entry, opening screenshot and every scene resource at its case-relative URL against its declared size and SHA-256.
2. Check each video's S3 HEAD size and custom SHA-256. A browser request for `Range: bytes=0-15` should return HTTP 206 and the expected total in `Content-Range`.
3. Serve HTML as `text/html` and JSON as `application/json`. The website must be able to frame the entry and fetch the native archive across origins. Verify that the guided player starts, the scene opens and the archive can be downloaded from the case page.

## Pelican native archive

The Pelican project uses the single Claude Fable 5.2 session with the Blender-optimized coastal scene. Its GitHub source is the [official release attachment](https://github.com/aipoch/open-science-usecases/releases/download/guided-labs-2026-11-24/Pelican-Open-Science.science). The attachment is 174,290,757 bytes and its SHA-256 is `6806e5719e0f073756d777470958a4152897bdfc95a3703fcb19f0202ac03c6a`.
