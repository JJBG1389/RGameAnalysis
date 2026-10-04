TRANCHE_LABELS = {
    "T1": "Championship Elite",
    "T2": "Championship Contender",
    "T3": "Regional Contender",
    "T4": "Emerging Competitor",
    "T5": "Developing",
    "T6": "Foundation",
}

TRAJECTORIES = ["Rising", "Stable", "Declining"]
GATES = ["Exists", "Reliable", "Integrated", "Contested", "Optimized"]


def season_stage(event_week: int):
    if event_week <= 1:
        return "G4", "Event 1"
    if event_week <= 5:
        return "G5", "Event 2 / qualification"
    return "G6", "Championship / late season"


def _allocation(tranche, auto, reliability, cpr):
    # Deliberately sums to 100: a simple representation of where the next
    # block of development effort should go.
    if tranche in ("T5", "T6"):
        base = {"Reliability": 35, "Autonomous": 20, "Driver practice": 20, "Primary mechanism": 20, "New features": 5}
    elif tranche == "T4":
        base = {"Reliability": 25, "Autonomous": 25, "Driver practice": 25, "Primary mechanism": 20, "New features": 5}
    elif tranche == "T3":
        base = {"Reliability": 20, "Autonomous": 25, "Driver practice": 20, "Primary mechanism": 20, "New features": 15}
    else:
        base = {"Reliability": 15, "Autonomous": 25, "Driver practice": 15, "Primary mechanism": 20, "New features": 25}

    if reliability < 90:
        shift = min(10, base["New features"])
        base["Reliability"] += shift
        base["New features"] -= shift
    if auto < 80:
        shift = min(5, base["New features"])
        base["Autonomous"] += shift
        base["New features"] -= shift
    if cpr < 70:
        shift = min(5, base["New features"])
        base["Driver practice"] += shift
        base["New features"] -= shift
    return base


def recommend(program, season, team, event_week, tranche, trajectory,
              primary_gate, auto_reliability, robot_reliability, cpr):
    stage_code, stage_name = season_stage(event_week)
    gate_idx = GATES.index(primary_gate)
    next_gate = GATES[min(gate_idx + 1, len(GATES) - 1)]

    priorities = []
    if robot_reliability < 95:
        priorities.append(f"Raise full-match reliability from {robot_reliability}% toward ≥95% before adding marginal mechanisms.")
    if auto_reliability < 90:
        priorities.append(f"Raise autonomous reliability from {auto_reliability}% toward ≥90% and maintain partner-compatible routines.")
    if cpr < 85:
        priorities.append(f"Improve contested performance retention from {cpr}% toward ≥85% through traffic/defense practice and alternate routes.")
    if gate_idx < 3:
        priorities.append(f"Move the primary scoring capability from {primary_gate} → {next_gate}; do not optimize peak speed yet.")
    else:
        priorities.append("Measure cycle distributions and reduce median cycle time without increasing failure variance.")

    if tranche in ("T4", "T5", "T6"):
        priorities.append("Protect driver-practice and software time by freezing low-value mechanical additions early.")
    elif tranche == "T3":
        priorities.append("Add strategic flexibility only after the core scoring loop and autonomous are competition-reliable.")
    else:
        priorities.append("Use remaining capacity on alliance complementarity, counter-meta testing, and physical-limit performance.")

    avoid = [
        "Late redesigns that reset capability maturity.",
        "Optimizing best-case cycle time before reliability and integration.",
    ]
    if tranche in ("T4", "T5", "T6"):
        avoid.append("Adding secondary capabilities whose development burden steals autonomous, testing, or driver time.")
    else:
        avoid.append("Adding complexity without a measurable increase in event-win or playoff contribution.")

    if tranche == "T4":
        headline = f"{program} {team or 'team'} — convert playoff value into qualification consistency"
        target = "Perform like a stable T3: reliable autonomous, low match-to-match variance, and captain/first-pick-caliber contribution."
    elif tranche in ("T5", "T6"):
        headline = f"{program} {team or 'team'} — raise the competitive floor first"
        target = "Finish every match with one repeatable scoring role, a dependable autonomous contribution, and minimal robot-caused failures."
    elif tranche == "T3":
        headline = f"{program} {team or 'team'} — turn regional contention into repeatable event-winning value"
        target = "Become consistently captain/first-pick caliber while preserving reliability under playoff-level disruption."
    else:
        headline = f"{program} {team or 'team'} — optimize championship-level marginal advantage"
        target = "Maximize playoff winning margin against elite opponents through autonomous leverage, complementarity, and counter-meta resilience."

    rationale = (
        f"Model 5.3 conditions the recommendation on {tranche} ({TRANCHE_LABELS[tranche]}), "
        f"a {trajectory.lower()} trajectory, {stage_code} ({stage_name}), capability maturity at "
        f"{primary_gate}, {robot_reliability}% nominal reliability, and {cpr}% CPR. "
        "The model prioritizes moving important capabilities through Exists → Reliable → Integrated → "
        "Contested → Optimized before spending scarce development time on additional features."
    )

    return {
        "tranche": tranche,
        "trajectory_symbol": {"Rising": "↑", "Stable": "→", "Declining": "↓"}[trajectory],
        "stage_code": f"{stage_code} · {stage_name}",
        "headline": headline,
        "summary": "Focus the next development block on the highest-value maturity and reliability gaps rather than maximum theoretical capability.",
        "priorities": priorities[:4],
        "maturity_action": (
            "Primary capability is already Optimized; validate it under stronger opposition and measure whether further work beats another strategic investment."
            if primary_gate == "Optimized"
            else f"Next gate: {primary_gate} → {next_gate}. Require evidence before advancing to optimization."
        ),
        "avoid": avoid,
        "event_target": target,
        "allocation": _allocation(tranche, auto_reliability, robot_reliability, cpr),
        "rationale": rationale,
    }
