# At 70% should you take it

## Research question

Does a 70% rain forecast tell everyone to make the same decision?

Builds an umbrella decision model around a stated rain probability, exposure time, and the relative inconvenience of carrying an umbrella versus getting wet. The session compares rain-timing assumptions and saves a break-even table and figure.

## Data and comparison design

Write down the cost of carrying protection and the loss from being caught without it. Compare expected losses under the forecast probability rather than choosing a universal probability cutoff. The model separates a calibrated event probability from a person-specific decision threshold.

## Recorded findings

The continuous-rain-block model is now the main model.

For exposure `e` hours and a rain block lasting `d` hours:



`P(wet) ≈ 0.70 × (d + e) / 12`  
`break-even ratio = 1 / P(wet)`



| Trip | `d = 1` h | `d = 2` h | `d = 4` h |
|---|---:|---:|---:|
| 20-minute walk | 12.86× | 7.35× | 3.96× |
| 2-minute trip | 16.59× | 8.43× | 4.25× |

Interpretation: for the 20-minute walk, if a typical rain episode lasts about 2 hours, getting soaked must be roughly **7.35 times worse** than carrying the umbrella for the umbrella to be worth it. For the 2-minute trip, the corresponding threshold is **8.43×**.

I would defend the continuous-block model over the constant-hazard model because rain is temporally clustered rather than arriving independently at every instant. The all-or-none model is a useful limiting case, giving `1 / 0.70 = 1.43×`, but it assumes any outdoor exposure overlaps the day’s rain event. The exact answer depends on typical rain duration `d`; **2 hours is my provisional middle value, and it is explicitly unverified here**. Local climatological rainfall-duration data would be the right way to replace it.

The figure uses **DejaVu Sans**, an open-licensed Bitstream Vera derivative; the SVG source contains no Arial or Helvetica references. The `.science` package contains the table, figure, producing Python script, and handoff note.

At 70%, take it when the soaked-to-umbrella hassle cost ratio exceeds the threshold implied by the exposure time and the typical rain-block duration.

- umbrella_break_even.science — complete export package.

## What the comparison shows

A forecast can be equally informative for two people who rationally choose different actions because their costs differ. The decision calculation does not itself verify forecast calibration.

## Assumptions and limits

The continuous rain-block duration is an explicitly unverified scenario parameter. This illustrates sensitivity to exposure and costs, rather than deriving a personal forecast from the headline rain probability.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
