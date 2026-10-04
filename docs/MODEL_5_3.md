# Model 5.3 Specification

## Objective

Model 5.3 is a competitive-engineering decision framework. The primary objective is to maximize:

**P(event success | game, robot architecture, team execution capacity, opponents, schedule, reliability)**

rather than theoretical maximum score.

"Event success" can be parameterized as event win, advancement, playoff selection, championship qualification, or another team objective.

## 1. Game model

Extract from the rules:

- scoring actions and point values
- ranking-point / qualification incentives
- autonomous constraints and leverage
- endgame values and timing
- possession limits
- game-piece count, scarcity, recycling, and ownership
- protected zones and defensive constraints
- field geometry, travel paths, choke points, and congestion
- alliance size and interaction
- penalties and strategic externalities

For each action estimate points per second, expected points per attempt, travel burden, resource consumption, opponent denial value, and resulting field state.

## 2. Candidate robot archetypes

Generate multiple functional architectures rather than one assumed optimum. Examples include:

- throughput specialist
- close-range scorer
- long-range scorer
- high-capacity scorer
- hybrid/generalist
- endgame specialist
- control/possession robot
- defensive specialist
- low-complexity specialist
- orientation-independent / turret-style scorer

Architectures are functional requirements, not prescribed mechanisms.

## 3. Reliability distributions

Model performance probabilistically rather than with ideal constants:

- acquisition success
- scoring accuracy
- cycle-time distribution
- jam probability
- mechanism failure
- disabled-match probability
- autonomous success
- endgame success

Expected value alone is insufficient; variance and tail risk affect event-winning probability.

## 4. Contested Performance Retention (CPR)

**CPR = expected contested performance / expected nominal performance**

Contested conditions include defense, traffic, game-piece starvation, blocked preferred routes, disrupted scoring locations, partner interference, and adverse field state.

Use CPR particularly heavily for elimination-play fitness.

## 5. Capability Maturity Gates

Each capability is assigned a maturity state:

1. Exists — demonstrates the task
2. Reliable — repeats successfully
3. Integrated — works with the full robot
4. Contested — retains performance under match disruption
5. Optimized — cycle time / efficiency is improved

Do not optimize immature capabilities merely because their theoretical ceiling is high.

## 6. Team Execution Capacity (TEC)

Classify teams T1–T6 using a rolling multi-year profile. Inputs should include:

- normalized competitive contribution (EPA/OPR-family measures)
- qualification consistency
- playoff advancement
- alliance-selection value
- reliability
- championship/district/state advancement
- year-over-year trajectory
- event strength
- demonstrated autonomous/software capability when measurable

The assignment must use information available before the target season to avoid leakage.

## 7. Season stage

Condition recommendations on:

- G1 Kickoff
- G2 Prototype
- G3 Integration
- G4 Event 1
- G5 Event 2 / qualification
- G6 Championship / late season

The same team may receive different recommendations as uncertainty falls and real performance becomes measurable.

## 8. Development burden and simplicity frontier

For each capability estimate:

- student-hours
- calendar duration
- machining/fabrication burden
- software burden
- weight/volume/power
- integration dependencies
- driver-training burden
- new failure modes
- opportunity cost to autonomous/testing/practice

Use a Pareto frontier: reject architectures dominated by another architecture with similar competitive value and materially lower development burden/risk.

## 9. Technology readiness and schedule

Track mechanism readiness and expected completion date. Late capability completion subtracts from downstream integration, autonomous, reliability testing, and driver practice.

A high-value feature can be rejected if its schedule-adjusted contribution to event success is negative.

## 10. Value of Information (VoI)

When architecture choice depends on uncertain assumptions, compare the expected value of a prototype/test with its cost.

Prefer a short experiment when it can materially change a high-cost decision. Stop testing when the expected information value is lower than the test burden.

## 11. Alliance co-optimization

Optimize alliances rather than assuming the individually strongest robots form the strongest alliance.

Model:

- complementary scoring roles
- field zoning
- traffic
- partner-safe autonomous routines
- game-piece competition
- defense/control roles
- endgame coordination
- draft value

Separate qualification fitness from elimination fitness.

## 12. Red-team / counter-meta loop

For each leading strategy:

1. Optimize Blue.
2. Optimize Red specifically to defeat Blue.
3. Re-optimize Blue against Red.
4. Continue until strategic adaptations produce little marginal gain.

Potential counters include starvation, lane denial, preferred-location denial, forcing long cycles, possession/control, defense, and endgame interference.

## 13. Season evolution / Worlds compression

Model how elite performance changes through the season rather than treating Week 1 performance as the ceiling.

Estimate:

- Week 1
- early season
- late season
- championship
- plausible physical limit

Historical competition data informs compression distributions for analogous game structures.

## 14. Progressive fidelity

Increase model fidelity as evidence becomes available:

**Kickoff:** analytical rules model.

**Prototype:** measured mechanism data.

**Integration:** robot-level reliability/cycle distributions.

**Event 1+:** empirical match/component data.

**Late season:** top-percentile opponent and mature-meta simulation.

Do not retain kickoff assumptions when measurements contradict them.

## 15. Recommended outputs

For each team tranche and season stage, report:

- recommended primary strategy
- functional robot specification
- required autonomous capability
- target acquisition/cycle/scoring performance
- CPR target
- endgame break-even
- alliance role
- counter-strategy vulnerabilities
- capabilities to omit
- maturity gates not yet passed
- highest-value next experiment
- highest-value next development action
- expected development burden
- confidence/uncertainty

The output should explain *why* each capability is recommended and identify what evidence would change the recommendation.
