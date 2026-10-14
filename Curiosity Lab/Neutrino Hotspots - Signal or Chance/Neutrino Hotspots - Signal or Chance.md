# Neutrino Hotspots - Signal or Chance

## Research question

How surprising is the strongest-looking sky patch after searching many patches?

Scans a reproducible neutrino-event sample and compares its strongest spatial cluster with randomized skies. The archive records fixed scan choices, preserved declinations, null checks, and a global comparison across searched locations.

## Data and comparison design

The record freezes the spatial grid and radii, record the maximum statistic, and compare it with maxima from right-ascension-randomized skies that preserve declinations. This accounts for the whole search rather than attaching a local probability to a selected winner.

## Recorded findings

| Scan quantity | Recorded result | Interpretation |
| --- | --- | --- |
| Strongest 3° patch | 18 events | The maximum was selected after scanning the sky. |
| Expected local count | 6.04 | A local excess before accounting for the search. |
| Equally strong randomized maxima | 753 of 1,999 skies | Compares maxima with maxima, not one fixed patch. |
| Global p-value | 0.377 | The selected hotspot is compatible with chance under this null. |

**Yes—the strongest patch is compatible with chance.** In the reproducible 5,000-event sample, the winning 3° circle at RA 210°, Dec 0° contains **18 events**, versus **6.04 expected**.

Of **1,999 randomized skies**, 753 produced an equally strong or stronger maximum. The **global p-value is 0.377**, accounting for every location and radius searched; its 95% Monte Carlo interval is 0.355–0.398.

The grid and radii were fixed before scanning. Randomizations preserved every declination. RA uniformity and its relationships with declination and time showed no clear discrepancy, supporting this null for a season-long analysis. These checks cannot exclude subtle instrumental effects. This unweighted subsample test also ignores event energies and angular uncertainties, so it cannot rule out astrophysical sources.

The events were observed **3 May 2021–23 May 2022**. The supplied provenance dates the **README publication to 5 October 2026**; that is not the observing period or an independently verified version-wide publication date.

## What the comparison shows

A visually striking patch can be compatible with the searched null. The subsample analysis does not rule out astrophysical sources.

## Assumptions and limits

The simplified unweighted sample analysis ignores some event information and cannot exclude astrophysical sources. The observing period and the supplied release-provenance date are distinct.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
