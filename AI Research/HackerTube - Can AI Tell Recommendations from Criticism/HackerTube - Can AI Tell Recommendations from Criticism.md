# HackerTube: Can AI Tell Recommendations from Criticism?

## The question

A video link inside a discussion is easy to extract. Deciding whether the writer recommends that video is harder: the comment may merely cite it, endorse one item in a list, or criticize a different claim in the surrounding thread. Can an AI-assisted workflow keep those distinctions visible while building a useful watchlist?

Inspired by HackerTube, this case audits a small, frozen sample of Hacker News comments about astronomy videos. It follows the evidence from original HTML links through per-video stance judgments, topic checks and a final five-video shortlist. The output is a traceable curation exercise, **not a measured accuracy score for HackerTube or an independently tested AI classifier**.

## Define the sample before counting recommendations

The supplied collection used the Algolia query `astronomy youtube.com`, restricted to comments, with 40 relevance-ranked hits requested. Comments containing specific YouTube video IDs were retained mechanically. The recorded retrieval time is November 3, 2026, at 05:26:08 UTC; selected comments span December 2009 to October 2026. The complete original 40-hit response is not included, so this is a keyword-selected convenience sample rather than representative sampling of Hacker News.

| Unit | Count | What it means |
|---|---:|---|
| Selected comments | 23 | Distinct source comments with retained video mentions |
| Comment–video relationships | 38 | A particular comment mentioning a particular 11-character video ID |
| Unique videos | 36 | Deduplicated destinations, retaining all supporting relationships |
| Final selected videos | 5 | A short, varied list supported by the recorded evidence |
| Supporting relationships for the shortlist | 6 | Two comments support the same beginner-guide video |
| Remaining videos | 31 | Preserved with omission reasons, rather than declared inferior |

Two video IDs occur in two comments each; the other 34 occur once. Adding comments, edges and video nodes would mix units. Treating repeated mentions as votes would also overstate what the sample establishes.

## Recover the links and preserve their context

The workflow reconciles links from both HTML `href` attributes and visible-text URLs against the supplied mapping. It recovers all 38 relationships without extras or omissions, including one link present only as visible text. Deduplication normalizes the destination video ID while preserving the comment that supplied it.

| Evidence layer | Use in the case | Remaining boundary |
|---|---|---|
| Official HN Firebase comment HTML | Authoritative wording for a selected source comment | A link remains a mention until its stance is interpreted |
| Up to three nearest parent items | Identify what praise, disagreement or criticism targets | Three parent chains are truncated |
| Separately fetched root story | Establish the broader discussion topic | It does not restore missing intermediate comments |
| Convenience plain text and search snapshots | Aid inspection and reconciliation | They do not override the official source HTML |
| Supplied oEmbed responses | Attribute video titles and authors when available | No transcript, full description, duration or playback evidence |

Each comment–video pair receives its own decision. Praise of a channel does not automatically praise every linked video, and a comment containing several links can treat them differently. Negative wording about a parent's claim must not be transferred to a video the writer actually endorses.

## Separate stance from astronomy relevance

The case uses four possible stance labels—recommend, critical, neutral/reference and unclear—and a separate yes/no/unclear topic-fit judgment. Recommendation can follow direct praise or appreciative inclusion in a list. A factual citation alone does not establish endorsement.

| Recorded stance | Astronomy fit: yes | No | Unclear | Total relationships |
|---|---:|---:|---:|---:|
| Recommend | 19 | 4 | 2 | 25 |
| Neutral/reference | 2 | 9 | 2 | 13 |
| Critical | 0 | 0 | 0 | 0 |
| Unclear | 0 | 0 | 0 | 0 |
| **Total** | **21** | **13** | **4** | **38** |

The zero critical count is a finding about these saved decisions. It is not evidence that an AI can reliably detect criticism, because this sample supplies no labeled critical examples to test that capability. Likewise, 25 recommendation relationships do not mean 25 unique recommended videos.

Four video-topic decisions remain unclear. A suggestive title, a connection to an astronomy course, a science-media outtake or an underlying physics demonstration was not enough to establish astronomy focus. Those gaps were not resolved from memory.

## Audit why each shortlisted video qualifies

All five provisional choices survived review against original wording and the available context. Three supporting relationships directly praise or recommend an individual video, while three endorse it within a favorable resource list. The final ordering suggests a varied viewing route; it does not rank measured video quality.

| Order and supplied title | Supplied author | Supported reason and source |
|---|---|---|
| 1. Getting Started in Amateur Astronomy - for COMPLETE BEGINNERS. Telescopes? Books? Binos? Part 1 | Ed Ting | Beginner observing resource, separately included in favorable advice lists in [source 42387446](https://news.ycombinator.com/item?id=42387446) and [source 49536680](https://news.ycombinator.com/item?id=49536680) |
| 2. Joseph Fraunhofer Biography: The Father of Modern Astronomy [CC] | Kathy Loves Physics | Individual biography praised in [source 31451807](https://news.ycombinator.com/item?id=31451807) |
| 3. How Starlink is changing Astronomy | Verse | Explicit recommendation for a discussion of benefits and drawbacks in [source 26458700](https://news.ycombinator.com/item?id=26458700); the comment's title differs but its video ID matches |
| 4. Pluto on the Horizon: Anticipating our First Encounter with the Double Planet | SVAstronomyLectures | Explicit recommendation in [source 9071833](https://news.ycombinator.com/item?id=9071833); historical pre-encounter material, not verified current coverage |
| 5. Basics of Statistics for Astro Imaging | The Astro Imaging Channel | Included among enjoyed imaging resources in [source 47936513](https://news.ycombinator.com/item?id=47936513); immediate criticism target is available, but ancestry remains truncated |

Titles and author names are attributed to the supplied successful metadata responses. The explanations describe the comments, not video contents inspected in this session. The native case retains the actual video destinations and a clickable watchlist.

The later full-table audit clarifies four of 38 explanations and leaves 34 unchanged. It removes a redundant extract, limits technical-treatment praise to the channel where appropriate, and removes two unsupported identifications or characterizations. No stance label, topic label or selection changes. Because the same assistant reviews its own evidence, this is a revision record rather than independent confirmation of semantic correctness.

## Metadata success is a different check from availability

| Recorded oEmbed response | Videos | Interpretation |
|---|---:|---|
| HTTP 200 | 33 | Title and author metadata were supplied |
| HTTP 403 | 1 | Metadata request failed; deletion is not established |
| HTTP 404 | 2 | Metadata request failed; deletion is not established |
| **Total** | **36** | One recorded request outcome per unique video |
| Playback tested | 0 | Availability, regional access and playability remain untested |
| Video content viewed | 0 | Accuracy and educational quality remain unassessed |

The final two rows describe the same set of videos and must not be added to the request totals. Failed metadata rows keep their titles, authors and thumbnail URLs blank. A successful response can supply a thumbnail URL without proving that the thumbnail image was fetched or inspected.

## What the workflow demonstrates

| Tempting shortcut | Evidence-aware alternative |
|---|---|
| Every extracted link is a recommendation | Record a separate stance for each source–video relationship |
| Negative language means the video is criticized | Identify the target of the criticism using available context |
| Repeated mentions establish superior quality | Keep both source edges without turning them into votes |
| A relevant-looking title settles topic fit | Retain unclear judgments when evidence is insufficient |
| Successful metadata proves a good, playable video | Separate naming, playback, content and quality checks |
| A reproducible chart proves the judgments correct | Distinguish deterministic rendering from semantic review |

The strongest result is the audit trail: a reader can trace a five-video list back to six source relationships and inspect why each was retained. No conclusion about whole-site HackerTube accuracy, another model's performance or general criticism recognition follows from this small, non-blind exercise.

## Saved materials and verification scope

The session preserves original inputs, per-pair judgments, the source network, six explanatory figures, selection and omission tables, metadata outcomes, a revision log and quotation accounting. Its final `astronomy_evidence_audit_verified.zip` includes `rebuild_audit.py`, a report, input and decision tables, rebuilt outputs, verification records and a clickable watchlist. Earlier provisional versions remain available as history.

The archived fresh-process check reports successful regeneration from an empty output directory without old images: numerical summaries, mappings and the watchlist matched, and 37 local-link occurrences had no broken targets. Four PNG files differed byte-for-byte from earlier renderings; the record does not promise identical image files across exploratory and final runs. External links and playback were not tested.

The rebuild script reads frozen decisions, makes no network calls and invokes no model. It verifies and renders saved judgments; it does not independently infer stance or guarantee identical decisions from a future model run. Extract the entire inner ZIP to use the report's local links. The published introduction uses standard Markdown tables and text, with no math-rendering dependency.

## Sources and provenance

The archived brief cites [Karpathy's HackerTube post](https://karpathy.bearblog.dev/hacker-tube/) and [its Hacker News discussion](https://news.ycombinator.com/item?id=50319510) as background. Whole-site figures in that background are not measurements made by this case. The individual source comments linked above support the shortlist's recorded reasoning.

This document summarizes the supplied AIPOCH Open-Science session, not a new research run. The original native package is preserved byte-for-byte; only its external publication filename is normalized to hyphens. The generated photographic-sticker cover is illustrative. Transfer checks and an actual native import test establish package integrity and compatibility, not the truth of every saved semantic judgment.
