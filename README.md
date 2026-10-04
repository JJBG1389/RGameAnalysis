# RGameAnalysis

RGameAnalysis is a competitive-engineering strategy model for **FRC, FTC, and VEX**. Its goal is not merely to predict match winners. It starts from game rules and team execution capacity to recommend the smallest set of capabilities a team can mature far enough to maximize its probability of competitive success.

**Current baseline: Model 5.3**

## Core idea

The model combines game economics, field geometry, game-piece economy, autonomous leverage, alliance composition, opponent counter-strategy, reliability, development cost, schedule risk, team capability, and empirical competition data.

The working priority hierarchy is:

1. Capability exists
2. Reliability
3. Integration
4. Autonomous capability
5. Contested Performance Retention (CPR)
6. Acquisition
7. Cycle-time compression
8. Alliance complementarity
9. Counter-meta robustness
10. Additional capabilities

A capability should not be optimized before it is reliable and integrated.

## Team tranches

Recommendations are conditioned on Team Execution Capacity (TEC):

- **T1 — Championship Elite**
- **T2 — Championship Contender**
- **T3 — Regional Contender**
- **T4 — Emerging Competitor**
- **T5 — Developing**
- **T6 — Foundation**

Teams also receive a trajectory: rising, stable, or declining.

## Season stages

- **G1 — Kickoff:** rules-only analysis
- **G2 — Prototype:** resolve high-value uncertainties
- **G3 — Integration:** freeze/delete capabilities based on maturity
- **G4 — Event 1:** optimize qualification consistency and advancement
- **G5 — Event 2 / qualification:** use measured deficits to select upgrades
- **G6 — Championship / late season:** optimize playoff role and counter-meta strategy

The model therefore evaluates **Game × Team Tranche × Season Stage × Trajectory**, rather than recommending one universal robot.

## Model 5.3 additions

### Contested Performance Retention

**CPR = contested performance / nominal performance**

CPR measures how much useful performance survives defense, traffic, disruption, scarcity, and opponent interaction. A lower-ceiling robot with high CPR can be preferable to a fragile high-ceiling robot in elimination play.

### Capability Maturity Gates

Capabilities advance through:

1. **Exists**
2. **Reliable**
3. **Integrated**
4. **Contested**
5. **Optimized**

Development resources should normally go toward moving important capabilities through these gates before adding marginal capabilities.

## Data strategy

The model is designed to incorporate:

- The Blue Alliance / Statbotics for FRC
- FIRST / FTCScout for FTC
- RobotEvents / Skills data for VEX
- Rules and scoring manuals
- Alliance selection and playoff data
- Robot architecture information from technical binders, CAD, reveal videos, and match video when available

Historical validation must use rolling-origin testing: train only on information available before the target season, freeze the prediction, then compare it with the mature championship meta.

## Validation policy

Earlier versions used manually assessed retrospective similarity percentages. Those are useful development diagnostics but **must not be presented as calibrated prediction probabilities**.

The project is moving toward reproducible, machine-scored validation using historical match/component data plus robot-architecture labels.

See:

- [Model 5.3 specification](docs/MODEL_5_3.md)
- [Team and season tranches](docs/TRANCHES.md)
- [Validation methodology](docs/VALIDATION.md)
- [Changelog](CHANGELOG.md)

## Near-term roadmap

1. Define a machine-readable game/robot capability schema.
2. Build historical ingestion for FRC, FTC, and VEX.
3. Implement rolling-origin backtests excluding COVID-disrupted championships.
4. Add robot-architecture labels.
5. Estimate tranche transitions year-over-year.
6. Generate kickoff recommendations by T1–T6.
7. Update predictions as real competition data arrives.
8. Report prediction errors explicitly instead of rewriting prior predictions.

The long-term objective is a system that can read a new game at kickoff, predict likely competitive equilibria, recommend appropriate robot architectures for different team capabilities, identify the highest-value experiments, and update those recommendations as the season evolves.
