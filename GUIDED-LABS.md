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

## Pelican native archive

The Pelican project uses the single Claude Fable 5.2 session with the Blender-optimized coastal scene. Its GitHub source is the [official release attachment](https://github.com/aipoch/open-science-usecases/releases/download/guided-labs-2026-11-24/Pelican-Open-Science.science). The attachment is 174,290,757 bytes and its SHA-256 is `6806e5719e0f073756d777470958a4152897bdfc95a3703fcb19f0202ac03c6a`.
