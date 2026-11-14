# FTC BIOBUZZ observed season data — 2026-11-14

Source: FTCScout event API, captured in GitHub Actions run 43598787800, artifact 14115361868. Analyzed directly from the archived JSON records. All values as of 2026-11-14 UTC.

## Data inventory
- 210 event records collected, 0 collector errors
- 8,050 played alliance-side scoring observations
- 2,903 team-event OPR records from 209 events
- 2,348 distinct team numbers with event OPR
- No claims about full-season coverage beyond the collected FTCScout search response

## Observed nonpenalty alliance scoring distributions
| Metric | P10 | P25 | P50 | P75 | P90 | P95 |
|---|---:|---:|---:|---:|---:|---:|
| Total | 19 | 28 | 43 | 62 | 90 | 113 |
| Autonomous | 3 | 8 | 11 | 23 | 33 | 36 |
| Driver-controlled | 12 | 18 | 31 | 43 | 65 | 85 |

Team-event nonpenalty total OPR percentiles: P10 7.77; P25 12.54; P50 18.73; P75 29.25; P90 45.13; P95 58.93. OPR is estimated individual contribution; alliance scores are not individual-team scores.

## Weekly alliance nonpenalty total
Week index here is a *calendar week from 2026-09-01*, not the competition-week definition in the UI. Do not use as direct W1–W8 calibration until event-week alignment is established.

| Calendar index | Observations | Median | P90 |
|---|---:|---:|---:|
| 3 | 4 | 33 | 37 |
| 4 | 110 | 67 | 149 |
| 5 | 166 | 30 | 71 |
| 6 | 118 | 33 | 72 |
| 7 | 66 | 42 | 75 |
| 8 | 1796 | 38 | 72 |
| 9 | 1674 | 41 | 86 |
| 10 | 3316 | 45 | 92 |
| 11 | 800 | 51 | 128 |

## Decision
**Recommend FTC numerical target recalibration study, not immediate coefficient changes.** Model 5.5 targets must be compared with **team OPR or team-attributed event metrics**, not alliance scores. This snapshot suggests current high-end target assumptions may be excessive, but does not prove which tranche/tailoring cells are miscalibrated. Build frozen preseason profiles for these teams and evaluate by matched event dates and game weeks.

## VEX status
GitHub Actions run 43598787800 confirms ROBOTEVENTS_TOKEN is empty. VEX collection exited with RuntimeError. The artifact labeled vex-override-raw-sample was mistakenly populated by the FTC files left in the shared collected directory; **do not interpret it as VEX data**. Configure the token in GitHub Actions secrets or use a separate public VEX results provider, then run VEX in a clean directory with a required nonempty manifest.

## Provenance
https://github.com/JJBG1389/RGameAnalysis/actions/runs/43598787800
https://github.com/JJBG1389/RGameAnalysis/actions/runs/43598787800/artifacts/14115361868
