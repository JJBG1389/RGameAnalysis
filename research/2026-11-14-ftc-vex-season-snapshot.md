# FTC BIOBUZZ and VEX Override: early-season evidence snapshot
Collected: 2026-11-14
Status: Research only. No model calibration changes authorized by this snapshot.

## FTC BIOBUZZ
Official rules: https://ftc-resources.firstinspires.org/ftc/game
Manual: TU09 (2026-11-12).
Latest team update: https://ftc-resources.firstinspires.org/ftc/game/tu-latest
TU09 G411 clarifies strategic denial of access to more than 8 scoring elements; GARDEN is not protected.
TU07 G304 clarifies 4 preloaded POLLEN elements and starting conditions.

Public leaderboard: https://ftc-reference.com/seasons/2026/leaders
Snapshot of selected best single-event OPR estimates (not directly observed solo match scores):
team,auto_opr,teleop_opr,nonpenalty_total_opr
16010,45.4,111.9,157.3
21229,41.8,109.2,151.1
19564,40.2,95.7,135.9
19666,30.0,102.2,132.1

Coverage reference: https://ftc-reference.com/seasons
At collection, site reports approximately 2270 teams and 3909 matches for 2026-27.
Coverage and leaderboard values are dynamic and should be timestamped when fetched.

## VEX V5RC Override
Official manual: https://manuals.vex.com/
Official game overview: https://www.vexrobotics.com/v5/competition
Manual version 2.1 released 2026-10-08.
Key scoring: alliance-colored Pin 5; owned yellow Pin 10; Midfield parking 8 per robot; Autonomous Bonus 12.
World skills: https://events.vex.com/robot-competitions/vex-robotics-competition/standings/skills
Snapshot of selected skills leaders:
team,autonomous_skills,driver_skills,total_skills
8737M,128,128,256
66799T,118,138,256
96Z,108,148,256

## Implications to investigate (not implemented)
1. FTC elite autonomous and teleop planning ranges may be too high relative to observed single-event OPR.
2. FTC scoring and game-control archetypes must respect the TU09 G411 restriction.
3. VEX total Skills can mask different autonomous/driver strengths; consider component-specific tailoring.
4. Compare VEX match scores separately from Robot Skills: the scoring environments are not interchangeable.
5. Derive week-indexed observed distributions from event dates before changing the Model 5.5 week curve.
6. No observed-outcome accuracy score or statistically calibrated change is established by this small, selected sample.

## Data limitations
The above are selected leaders, not a random sample or complete team-event dataset. OPR is an estimate. Skills is a maximum, not typical match contribution. Do not use these values as full-population percentile cutoffs without downloading the underlying records.
