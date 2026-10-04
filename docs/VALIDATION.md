# Validation Methodology

## Principle

Model revisions must be evaluated with rolling-origin historical backtests rather than hindsight-only descriptions.

For target season N:

1. Use only rules and historical information available before season N.
2. Assign team tranches using only pre-season-N history.
3. Generate and freeze predictions.
4. Reveal season N competition data.
5. Compare predictions with actual mature meta and team outcomes.
6. Record errors without retroactively rewriting the frozen prediction.
7. Advance to season N+1.

COVID-disrupted/no-comparable championship seasons should be excluded or separately labeled rather than treated as ordinary championship observations.

## Two separate validation questions

### Meta Prediction Score
Did the model predict the mature competitive equilibrium?

Candidate dimensions:

- primary scoring strategy
- acquisition requirements
- scoring architecture/function
- autonomous leverage
- endgame strategy
- defense/denial
- game-piece economy
- field/traffic behavior
- alliance-role composition
- contested performance
- capabilities correctly identified as unnecessary

### Team Development Score
Did the tranche-specific recommendation improve the type of outcome relevant to that team?

Candidate outcomes:

- normalized EPA/OPR-family improvement
- qualification percentile
- autonomous component improvement
- playoff selection/advancement
- alliance-selection value
- reliability/variance
- championship qualification
- year-over-year tranche movement

## Data sources

### FRC
The Blue Alliance, Statbotics, official FIRST event data, rules archives.

### FTC
Official FIRST event data, FTCScout, rules archives.

### VEX
RobotEvents, Skills standings, rules archives.

### Architecture layer
Technical binders, CAD, team websites, reveal videos, match video, and manually/automatically labeled robot features.

## Anti-leakage requirements

- Team tranche for season N must not use season N outcomes.
- Kickoff predictions must not use Week 1+ data.
- Week-k updates may use data only through week k.
- Championship results must remain hidden until final scoring.
- Rules updates should be timestamped; a prediction may only use updates available at its prediction date.

## Reporting

Do not describe retrospective similarity scores as calibrated probabilities.

Report:

- sample size
- seasons included/excluded
- data completeness
- scoring rubric
- uncertainty
- per-season errors
- per-tranche performance
- comparison with prior model versions

The long-term target is a fully reproducible numerical backtest rather than subjective percentage grades.
