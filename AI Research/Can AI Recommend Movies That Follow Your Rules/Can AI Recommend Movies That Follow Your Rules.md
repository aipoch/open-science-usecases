# Can AI Recommend Movies That Follow Your Rules

## Research question

How often does a fixed watchlist violate the user’s runtime, genre, or sequel restrictions?

Freezes a ten-film watchlist and audits it against genre, runtime, and sequel restrictions. The archived table records evidence for each recommendation and separates confirmed violations from ambiguous classification.

## Data and comparison design

The record freezes the recommendations before looking up their properties. Verify each film against the same criteria and distinguish a clear violation from an ambiguous genre boundary. Keep runtime and originality evidence alongside the judgment.

## Recorded findings

The fixed watchlist has **0 confirmed rule-breaking films and 0 confirmed rule violations**. Nine are clear passes. *The Vast of Night* is a caution: film sources call it science fiction, but its eerie tone and screening at a horror festival may make it a poor fit for someone avoiding horror altogether. The archived assessment does not count that uncertainty as a pass or as a confirmed violation.

| Original recommendation | Runtime | Verdict and evidence |
|---|---:|---|
| *Arrival* (2016) — a thoughtful first contact story built around language. | 116 min | Pass. [Genre and time](https://www.bbfc.co.uk/release/arrival-q29sbgvjdglvbjpwwc00mzi3nti); [story origin](https://www.paramountpictures.com/movies/arrival). |
| *Ex Machina* (2014) — a tense, compact story about artificial intelligence. | 108 min | Pass. [Genre and time](https://www.bbfc.co.uk/release/ex-machina-q29sbgvjdglvbjpwwc0zodiwndi); [original screenplay](https://www.bafta.org/media-centre/press-releases/nominations-announced-for-the-ee-british-academy-film-awards-in-2016/). |
| *Moon* (2009) — a lonely lunar mystery with a strong central performance. | 97 min | Pass. [Genre and time](https://www.bbfc.co.uk/release/moon-q29sbgvjdglvbjpwwc00ntcymdm); [production history](https://www.sonyclassics.com/moon/moon_presskit.pdf). |
| *Source Code* (2011) — a brisk science fiction puzzle with a ticking clock. | 93 min | Pass. [Genre and time](https://www.bbfc.co.uk/release/source-code-q29sbgvjdglvbjpwwc0zodiymtu); [writer interview](https://scriptshadow.net/interview-with-ben-ripley-writer-of-source-code-2/). |
| *Primer* (2004) — a demanding time travel story that rewards close attention. | 77 min | Pass, with differing genre and minute labels across sources. [Sci-fi listing](https://visitfilms.com/primer); [runtime](https://www.library.ucla.edu/visit/events-exhibitions/timecrimes-primer-08-16-24/). |
| *Gattaca* (1997) — a sharp story about ambition and genetic selection. | 106 min | Pass. [Genre and time](https://www.bbfc.co.uk/release/gattaca-q29sbgvjdglvbjpwwc0zmdyyote); [studio film record](https://www.sonypictures.com/movies/gattaca). |
| *The Vast of Night* (2019) — a small town mystery carried by sound and atmosphere. | 91 min | **Caution:** science-fiction thriller, with horror-adjacent atmosphere. [Festival genre](https://filmadelphia.org/wp-content/uploads/2023/12/PFF28-Program-Guide-1.pdf); [horror festival screening and time](https://www.overlookfilmfest.com/2019-program/). |
| *The Man from Earth* (2007) — a dialogue driven science fiction premise. | 87 min | Pass. The recommended film is the original; *Holocene* came later. [Genre and time](https://sf-encyclopedia.com/entry/jerome_bixbys_the_man_from_earth); [film site](https://manfromearth.com/mfe/). |
| *The Invisible Guest* (2016) — a twisty locked room crime mystery. | 106 min | Pass. This is the Spanish *Contratiempo*, which had a 2017 theatrical release. [Genre](https://www.rottentomatoes.com/m/the_invisible_guest); [runtime and origin](https://www.filmfactoryentertainment.com/films/the-invisible-guest/). |
| *See How They Run* (2022) — a playful whodunit set in London’s theatre world. | 98 min | Pass. [Genre and time](https://www.bbfc.co.uk/release/see-how-they-run-q29sbgvjdglvbjpwwc0xmda1ndu4); [studio story and credits](https://www.searchlightpictures.com/see-how-they-run). |

The notebook preserves the original wording, per-film sources, release-cut differences, sequel and prequel reasoning, verdicts, and reproducible counts. Where a source does not explicitly say “not a sequel,” the notebook labels the standalone judgment as an inference from the film’s origin evidence.

## What the comparison shows

A zero confirmed-violation count is not the same as ten unqualified passes. Personal interpretation of a genre restriction remains relevant.

## Assumptions and limits

A film with an eerie tone remains a caution rather than an automatic pass. Genre judgments and dated source evidence do not guarantee that every viewer will consider the list suitable.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
