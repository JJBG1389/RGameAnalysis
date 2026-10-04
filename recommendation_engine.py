TRANCHE_LABELS={"T1":"Championship Elite","T2":"Championship Contender","T3":"Regional Contender","T4":"Emerging Competitor","T5":"Developing","T6":"Foundation"}
TRAJECTORIES=["Rising","Stable","Declining"]; GATES=["Exists","Reliable","Integrated","Contested","Optimized"]
def season_stage(w):
    if w<=1:return "G4","Event 1"
    if w<=5:return "G5","Event 2 / qualification"
    return "G6","Championship / late season"
def _allocation(t,a,r,c):
    if t in ("T5","T6"):b={"Reliability":35,"Autonomous":20,"Driver practice":20,"Primary mechanism":20,"New features":5}
    elif t=="T4":b={"Reliability":25,"Autonomous":25,"Driver practice":25,"Primary mechanism":20,"New features":5}
    elif t=="T3":b={"Reliability":20,"Autonomous":25,"Driver practice":20,"Primary mechanism":20,"New features":15}
    else:b={"Reliability":15,"Autonomous":25,"Driver practice":15,"Primary mechanism":20,"New features":25}
    for cond,key,n in [(r<90,"Reliability",10),(a<80,"Autonomous",5),(c<70,"Driver practice",5)]:
        if cond:
            s=min(n,b["New features"]);b[key]+=s;b["New features"]-=s
    return b
def recommend(program,season,team,event_week,tranche,trajectory,primary_gate,auto_reliability,robot_reliability,cpr):
    sc,sn=season_stage(event_week);gi=GATES.index(primary_gate);ng=GATES[min(gi+1,4)];p=[]
    if robot_reliability<95:p.append(f"Raise full-match reliability from {robot_reliability}% toward ≥95% before adding marginal mechanisms.")
    if auto_reliability<90:p.append(f"Raise autonomous reliability from {auto_reliability}% toward ≥90% and maintain partner-compatible routines.")
    if cpr<85:p.append(f"Improve CPR from {cpr}% toward ≥85% through traffic/defense practice and alternate routes.")
    p.append(f"Move the primary capability from {primary_gate} → {ng}; do not optimize peak speed yet." if gi<3 else "Reduce median cycle time without increasing failure variance.")
    p.append("Protect driver-practice and software time by freezing low-value mechanical additions early." if tranche in ("T4","T5","T6") else "Use remaining capacity on strategic flexibility, alliance complementarity, and counter-meta testing.")
    avoid=["Late redesigns that reset capability maturity.","Optimizing best-case cycle time before reliability and integration."]
    if tranche=="T4":headline=f"{program} {team or 'team'} — convert playoff value into qualification consistency";target="Perform like a stable T3: reliable autonomous, low variance, and captain/first-pick-caliber contribution."
    elif tranche in ("T5","T6"):headline=f"{program} {team or 'team'} — raise the competitive floor first";target="Finish every match with one repeatable scoring role, dependable autonomous contribution, and minimal robot-caused failures."
    elif tranche=="T3":headline=f"{program} {team or 'team'} — turn regional contention into repeatable event-winning value";target="Become consistently captain/first-pick caliber while preserving reliability under playoff-level disruption."
    else:headline=f"{program} {team or 'team'} — optimize championship-level marginal advantage";target="Maximize playoff winning margin through autonomous leverage, complementarity, and counter-meta resilience."
    return {"tranche":tranche,"trajectory_symbol":{"Rising":"↑","Stable":"→","Declining":"↓"}[trajectory],"stage_code":f"{sc} · {sn}","headline":headline,"summary":"Focus the next development block on the highest-value maturity and reliability gaps rather than maximum theoretical capability.","priorities":p[:4],"maturity_action":("Primary capability is Optimized; validate it under stronger opposition." if primary_gate=="Optimized" else f"Next gate: {primary_gate} → {ng}. Require evidence before optimizing."),"avoid":avoid,"event_target":target,"allocation":_allocation(tranche,auto_reliability,robot_reliability,cpr)}
def worlds_delta(first,tranche,trajectory,auto_reliability,robot_reliability,cpr):
    deltas=["Re-measure the mature game meta after Event 1 and compare your actual component contribution with top-percentile teams.","Add or expand autonomous routines only where they create uncontested scoring, partner compatibility, or starting-position flexibility.","Practice against stronger defense/traffic and redesign only the failure modes that materially reduce contested performance.","Tune cycle time after reliability and CPR targets are met; preserve the first-event robot's proven core."]
    if tranche in ("T1","T2","T3"):deltas.append("Add a championship-specific counter-meta or alliance-complementarity capability only if its measured value exceeds integration risk.")
    else:deltas.append("Prefer a narrow, proven upgrade path over a championship-scale rebuild; protect practice and reliability.")
    return {"deltas":deltas,"targets":["≥98% match reliability","≥95% autonomous reliability","≥90% CPR against playoff-level disruption","Multiple partner-compatible autonomous options","Measured playoff role that complements likely alliance partners"],"guardrail":"Do not sacrifice a proven scoring loop for a late Worlds feature unless testing shows a clear increase in playoff winning margin."}


GAME_FEATURES = {
    ("FRC", 2026): {
        "must": ["Fast, wide floor Fuel intake", "High-throughput Fuel storage/indexing", "Repeatable high-rate Hub shooter", "Vision + odometry localization", "Multiple autonomous Fuel-scoring routines"],
        "should": ["Score from multiple field locations", "Automated aiming/shooter sequencing", "Anti-jam sensing/recovery", "Architecture that retains scoring under traffic/defense"],
        "optional": ["Tower capability only if measured endgame value exceeds continued Fuel scoring", "Advanced aim-independent/turret solution only after fixed scoring is mature"],
    },
    ("FRC", 2025): {
        "must": ["Fast Coral acquisition", "Reliable L1-L4 Coral placement with L4 emphasis", "AprilTag/odometry reef alignment", "Multi-Coral autonomous capability", "Reliable drivetrain positioning around the Reef"],
        "should": ["Deep Cage climb", "Automated Coral scoring sequence", "Useful Algae handling without compromising Coral throughput", "Partner-safe autonomous paths"],
        "optional": ["Expanded Algae specialization", "Additional scoring geometry only after L4 cycles are mature"],
    },
    ("FRC", 2024): {
        "must": ["Fast floor Note intake", "Reliable Speaker scoring", "Vision-assisted aiming/localization", "Multi-Note autonomous", "Fast drivetrain transitions between acquisition and scoring"],
        "should": ["AMP capability", "Reliable Stage endgame", "Automated shot preparation while driving", "Defense-resistant acquisition"],
        "optional": ["Trap scoring", "Complex shooting flexibility beyond proven high-value locations"],
    },
    ("FTC", 2027): {
        "must": ["Wide tolerant floor intake", "Buffered multi-element storage", "Highly repeatable HIVE launcher", "Odometry + AprilTag localization", "Reliable multi-TIP autonomous"],
        "should": ["Automatic chassis aiming", "Fast HIVE recycling geometry", "Simple NECTAR/FLOWER capability if it does not compromise HIVE throughput", "Automatic indexing and jam recovery"],
        "optional": ["Turreted launcher after fixed/chassis aiming is mature", "Sophisticated FLOWER specialization"],
    },
    ("FTC", 2026): {
        "must": ["Wide Artifact intake", "Fast internal indexing/storage", "Repeatable high-rate scoring mechanism", "Vision/odometry localization", "Strong autonomous scoring"],
        "should": ["Automatic Artifact classification/sorting", "Flexible scoring orientation", "Automated aiming", "Fast return/base execution"],
        "optional": ["Turret or other orientation-independent scorer after base shooter is mature"],
    },
    ("FTC", 2025): {
        "must": ["Fast ground Sample intake", "Reliable high-value scoring", "Strong autonomous", "Odometry/vision alignment", "Low-cycle-time extension/lift"],
        "should": ["Alliance-complementary Sample/Specimen capability", "Reliable ascent when opportunity cost is favorable", "Automated scoring positions"],
        "optional": ["Full hybrid capability if specialization is already mature"],
    },
    ("VEX", 2026): {
        "must": ["Fast primary game-object acquisition", "Reliable high-throughput scoring", "Compact maneuverable drivetrain", "Autonomous scoring routine", "Mechanism designed for repeated cycles"],
        "should": ["Game-object control/denial capability", "Multiple autonomous starting strategies", "Defense-resistant scoring routes"],
        "optional": ["Secondary scoring functions only after primary throughput is mature"],
    },
}

def robot_features(program, season, tranche):
    base = GAME_FEATURES.get((program, int(season)))
    if not base:
        base = {
            "must": ["Reliable drivetrain", "One high-value primary scoring mechanism", "Repeatable autonomous contribution", "Tolerant game-piece acquisition"],
            "should": ["Automated alignment/localization where useful", "Simple high-value endgame", "Partner-compatible autonomous options"],
            "optional": ["Secondary scoring capability", "High-complexity mechanism for marginal scoring flexibility"],
        }
    must=list(base["must"]); should=list(base["should"]); optional=list(base["optional"])
    if tranche in ("T5","T6"):
        # Lower-TEC teams should protect completion and practice time.
        optional = should[2:] + optional
        should = should[:2]
    elif tranche=="T4" and len(should)>3:
        optional = should[3:] + optional
        should = should[:3]
    return {"must":must,"should":should,"optional":optional}

def worlds_feature_delta(program, season, tranche):
    base = robot_features(program, season, tranche)
    return {
        "retain": base["must"][:],
        "add_or_upgrade": [
            "Increase autonomous breadth and starting-position flexibility.",
            "Increase scoring/acquisition tolerance under championship-level traffic and defense.",
            "Add alliance-complementary capability only when measured playoff value exceeds integration risk.",
            "Reduce cycle-time variance and automate repetitive driver actions.",
        ] + (base["optional"][:1] if tranche in ("T1","T2","T3") and base["optional"] else []),
        "do_not_sacrifice": "Do not destabilize the proven primary scoring loop, autonomous reliability, or driver practice to add a late championship feature.",
    }
