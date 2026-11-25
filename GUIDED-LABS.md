# Interactive case experiences

A case can offer one browser experience in addition to its introduction and native project. The five guided 3D labs use this contract. A case in any catalog can opt in.

## Case layout

Store the static site in a dedicated `experience/` directory. Its public entry is always `index.html`. Keep internal pages, scripts, textures and other assets at the relative paths used by the HTML. The five labs also include a `lab.json` with player-specific metadata and a screenshot. Other experiences only need their entry and its dependencies.

Add an optional `experience` object to the case in the root manifest. For example, the Mendel case uses the repository path `3D Lab/Mendel Laboratory/experience`. Set `revision` to the full Git tree ID of that directory. To obtain it after staging the assets:

```sh
git add -- '3D Lab/Mendel Laboratory/experience'
staged_tree=$(git write-tree)
git rev-parse "$staged_tree:3D Lab/Mendel Laboratory/experience"
```

Refresh the revision after any change to the directory. CI compares the declared revision to the fixed checkout, including when only a scene file changed.

## Website entry

Show the experience button when the case declares `experience`. Resolve the following path relative to the published manifest:

```text
<case.name>/experience/<experience.revision>/index.html
```

The repository path locates the source. The URL uses the stable case name and the versioned prefix. The Action recursively prepares, uploads and verifies each dependency before committing the case's manifest checkpoint. Prior revisions remain available for previously loaded pages. An experience-only change does not select the native archive for extraction.

## Large page dependencies

To include a file hosted in an allowed upstream repository at a relative URL in the experience, declare it in `experience/.experience-sources.json`. Keys are paths relative to the entry directory. Each value contains a direct `release_url`, the actual `bytes` and the file's `sha256`. Use the same repository URL allowlist as the case resources. Local and remote paths must be distinct. The sources file is publication metadata and is omitted from the published site.

The five labs load `introduction.mp4` by relative URL. Their source declarations pin the original films in the [verified dataset snapshot](https://huggingface.co/datasets/AIPOCH-AI/open-science-usecases/commit/aa030b4a40a2db71e8c0ef589189ce0720a20b9a). The Action verifies each film and serves it beside its HTML, with the video MIME type. Independent case video links continue to follow [the existing video contract](.github/VIDEOS.md).

The Pelican native project remains an [official release attachment](https://github.com/aipoch/open-science-usecases/releases/download/guided-labs-2026-11-24/Pelican-Open-Science.science).
