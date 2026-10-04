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


## Run the Team Advisor locally

The repository includes a Streamlit V1 front end.

```bash
git clone https://github.com/JJBG1389/RGameAnalysis.git
cd RGameAnalysis
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

Then install and run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Streamlit will print a local URL, normally `http://localhost:8501`.

### V1 behavior

- FRC 6964 has a built-in provisional **T4 ↑** demo profile.
- Other teams can be assigned a provisional tranche and trajectory manually.
- Users can enter program, season, team, next event week, primary capability maturity, autonomous reliability, match reliability, and CPR.
- The app generates priorities, maturity-gate guidance, work to avoid, an event objective, and a recommended development-effort allocation.
- Live TBA/Statbotics/FTCScout/RobotEvents ingestion is a planned next step.


## Live data and manual connections

The Team Advisor now includes live adapters / official links for the sources used in Model 5.3:

- **FRC:** Statbotics (public live API), The Blue Alliance API v3, and official FIRST current/archive game materials.
- **FTC:** FTCScout public API, official FIRST FTC Event Results, and official current/archive Competition Manual materials.
- **VEX V5:** RobotEvents API v2 plus official VEX competition/manual pages.

### Optional API credentials

Statbotics and FTCScout do not require local credentials for the calls used by V1.

For full FRC data, create a TBA Read API key and set:

```powershell
$env:TBA_AUTH_KEY="your-key"
```

For VEX RobotEvents, create an API token and set:

```powershell
$env:ROBOTEVENTS_TOKEN="your-token"
```

Set these variables in the same PowerShell session before running `streamlit run app.py`. Do not commit API keys to this repository.

### World Championship planning

The UI includes a **Team plans to attend World Championship** toggle.

- **Off:** the advisor generates the first-event plan.
- **On:** the advisor keeps the first-event plan and adds a separate **World Championship delta plan**: upgrades, maturity targets, autonomous expansion, CPR/reliability targets, and a guardrail against destabilizing a proven robot with late features.

The Worlds output is intentionally expressed as deltas from the first-event configuration rather than as a second independent robot design.
