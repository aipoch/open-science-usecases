# COVID-19 Case Counts - Trend or Reporting Noise

## Research question

Which features reflect the broad reported-case wave, and which reflect the reporting calendar?

Compare day-to-day reporting variation with a defensible descriptive reported-case trend for Lombardia during 1 July–31 December 2020. Use official public tables, a compact fixed period, centered seven-day and 21-day smoothers, and explicit uncertainty about the observation process.

## Data and comparison design

The comparison uses centered seven- and 21-day smoothers with the raw daily reports. Summarize weekday departures from the seven-day curve to distinguish recurrent reporting patterns from the slower epidemic trajectory. Centering uses observations on both sides of each date.

| Input or source | Role in this case | Source context |
| --- | --- | --- |
| [Italian Civil Protection pinned repository](https://github.com/pcm-dpc/COVID-19/commit/fc82987b9ebda01fe8e5b59d5667e3e00721edb9) | Official regional CSVs, snapshot dated 2025-01-10 and retrieved 2026-09-29 | Preserve upstream attribution and applicable source terms; this README grants no additional third-party rights |
| [Regional field definitions](https://github.com/pcm-dpc/COVID-19/blob/fc82987b9ebda01fe8e5b59d5667e3e00721edb9/dati-andamento-covid19-italia.md) | Use nuovi_positivi, not net active-case change; preserve notification dates | Preserve upstream attribution and applicable source terms; this README grants no additional third-party rights |

## Recorded findings

| Reporting summary | Recorded result | Interpretation |
| --- | --- | --- |
| Window | Lombardia, July–December 2020 | Historical reported cases. |
| Period total | 385,002 | Reports, not reconstructed infections. |
| Smoothed peak | 10 November for 7- and 21-day centered curves | Retrospective agreement across smoothing widths. |
| Weekday departures | Monday −44.6%; Friday +23.8% | Median deviations from the seven-day curve. |

There are 184 target dates, 204 dates including boundary context, and 385,002 reported cases in the target period. The raw maximum is 11,489 on 7 November 2020. Both centered smoothers peak on 10 November: 8,806.285714 cases/day for seven days and 8,135.142857 for 21 days. Median daily departures from the seven-day smoother are −44.591495% on Mondays and +23.793565% on Fridays; the overall median absolute departure is 20.633769%. These source-count and smoothing calculations were independently checked in the bounded review.

## What the comparison shows

Agreement on the peak date supports a retrospective description of the wave. Large weekday departures explain why individual daily reports can misrepresent its direction.

## Assumptions and limits

The curves describe reported cases, not reconstructed infections. Centered windows use future observations and cannot serve as real-time nowcasts. Testing changes, delays, revisions and shared-window dependence limit interpretation; a later source snapshot does not reconstruct historical real-time data vintages.

## Sources and research materials

The unchanged research package comes from the [upstream archive](https://huggingface.co/datasets/AIPOCH-AI/open-science-cases/tree/4a22011b2b0d08492b55d75798ecb29acbeba32c/cases/case17). It retains the original conversation and included scientific artifacts, including analysis code, results and figures. The poster is an AI-generated thematic illustration, not study evidence. This introduction summarizes archived findings; the analysis was not rerun. Later bounded checks do not certify the entire study or mean the original package was corrected.
