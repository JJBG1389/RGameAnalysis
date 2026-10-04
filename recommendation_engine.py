TRANCHE_LABELS={"T1":"Championship Elite","T2":"Championship Contender","T3":"Regional Contender","T4":"Emerging Competitor","T5":"Developing","T6":"Foundation"}
TRANCHE_SHARES={"T1":5,"T2":10,"T3":20,"T4":25,"T5":25,"T6":15}
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
    if tranche in ("T1","T2"):
        # Proven teams can usually carry more simultaneous game capability.
        promote=should[:2]
        must=list(dict.fromkeys(must+promote))
        should=list(dict.fromkeys(should[2:]+optional[:1]))
        optional=optional[1:] if len(optional)>1 else optional
    elif tranche=="T4":
        optional=list(dict.fromkeys(should[2:]+optional))
        should=should[:2]
        must=must[:4]
    elif tranche=="T5":
        optional=list(dict.fromkeys(must[3:]+should[1:]+optional))
        must=must[:3]
        should=should[:1]
    elif tranche=="T6":
        # Rookie/foundation: finish a robust minimum competitive robot early.
        optional=list(dict.fromkeys(must[2:]+should+optional))
        must=must[:2]
        should=["Repeatable autonomous contribution"]
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


TRANCHE_SHARES = {
    "T1": "≈2% of teams",
    "T2": "≈8% of teams",
    "T3": "≈15% of teams",
    "T4": "≈25% of teams",
    "T5": "≈30% of teams",
    "T6": "≈20% of teams",
}
# These are policy bands for the model, not measured FIRST/VEX population shares.
# The live classifier will eventually replace them with season/program-specific empirical quantiles.

PERFORMANCE_TARGETS = {
    ("FRC", 2026): {
        "T1": {"auto":"85–115 Fuel points","teleop":"220–300 Fuel points","rate":"Sustain ~3.5–4.5+ scored Fuel/sec during active scoring bursts; refill/reposition with minimal dead time.","cycles":"Treat Fuel as continuous flow rather than discrete cycles; maximize intake-to-shot duty cycle.","avoid":["Treat as lower priority when Tower scoring if disengage/travel/climb opportunity cost exceeds expected Fuel during the same time.","Sequence later unless a turret/aim-independent system unless testing shows a measurable throughput/CPR gain over chassis aiming."]},
        "T2": {"auto":"70–100 Fuel points","teleop":"180–255 Fuel points","rate":"Target ~2.5–3.5 scored Fuel/sec in active shooting windows.","cycles":"High-capacity collection + rapid dump; minimize inactive-Hub dead time by collecting/positioning.","avoid":["Do not sacrifice shooter/intake reliability for an elaborate Tower mechanism.","Avoid secondary mechanisms that reduce hopper capacity or jam resistance."]},
        "T3": {"auto":"55–85 Fuel points","teleop":"140–210 Fuel points","rate":"Target ~1.8–2.8 scored Fuel/sec when shooting.","cycles":"Reliable collect-buffer-shoot loop; prioritize one or two proven shooting locations.","avoid":["Sequence later than championship-level turret complexity before fixed shooting and auto are mature.","Prioritize after Tower points ahead of primary Fuel throughput."]},
        "T4": {"auto":"40–65 Fuel points","teleop":"105–165 Fuel points","rate":"Target ~1.2–2.0 scored Fuel/sec from a repeatable location.","cycles":"Wide intake, simple buffer, repeatable shooter; spend saved complexity on auto and driving.","avoid":["Sequence later unless a high-complexity turret initially.","Sequence later than multiple endgame options; add Tower only if it becomes highly reliable early."]},
        "T5": {"auto":"25–50 Fuel points","teleop":"75–125 Fuel points","rate":"Target ≥0.8–1.3 scored Fuel/sec with very low jam rate.","cycles":"One reliable collection/scoring loop.","avoid":["Lower priority: turret and complex Tower mechanisms.","Add only after a second scoring architecture until the primary loop is reliable."]},
        "T6": {"auto":"10–30 Fuel points","teleop":"40–90 Fuel points","rate":"Target repeatable scoring every match before optimizing rate.","cycles":"Reliable drivetrain + intake + one scoring solution.","avoid":["Sequence after core capability: championship-complexity mechanisms.","Lower priority: optional scoring/endgame functions until the core robot completes full simulated matches."]},
    },
    ("FRC", 2025): {
        "T1":{"auto":"70–85+ points","teleop":"170–230+ points","rate":"Target ~5–7 sec per Coral cycle equivalent in sustained reef work.","cycles":"Multi-Coral auto; rapid L4 cycling with automated reef alignment.","avoid":["Do not spend meaningful match time on low-value Algae if it displaces L4 Coral.","Do not sacrifice triple/deep-cage endgame reliability for marginal secondary scoring."]},
        "T2":{"auto":"50–75 points","teleop":"130–190 points","rate":"Target ~7–9 sec effective Coral cycles.","cycles":"L4-first cycling; automated alignment; reliable Deep Cage.","avoid":["Avoid broad Algae specialization unless alliance strategy demands it.","Add only after scoring degrees of freedom that slow Coral cycles."]},
        "T3":{"auto":"35–60 points","teleop":"90–145 points","rate":"Target ~9–12 sec effective Coral cycles.","cycles":"Fast station acquisition + repeatable L4 placement; simple Algae utility.","avoid":["Sequence later unless an elaborate Algae system ahead of L4 reliability.","Avoid late redesigns for marginal reef reach."]},
        "T4":{"auto":"20–45 points","teleop":"60–105 points","rate":"Target ~12–16 sec effective Coral cycles with ≥95% placement reliability.","cycles":"Prioritize station intake, L4 scoring, auto-align, and one reliable climb.","avoid":["Sequence after core capability: to become equally good at Coral and Algae.","Lower priority: complex secondary manipulators until L4 + auto are mature."]},
        "T5":{"auto":"10–30 points","teleop":"35–70 points","rate":"Target ~16–22 sec reliable Coral cycles.","cycles":"One reliable Coral acquisition/placement loop.","avoid":["Lower priority: specialized Algae scoring.","Avoid complex climb if it prevents a working Coral robot."]},
        "T6":{"auto":"5–20 points","teleop":"20–50 points","rate":"Complete repeatable Coral scoring before cycle optimization.","cycles":"Reliable drivetrain + one Coral level + simple auto.","avoid":["Sequence after core capability: all reef levels plus Algae plus climb.","Choose the simplest repeatable scoring level and finish early."]},
    },
    ("FTC", 2026): {
        "T1":{"auto":"55–85 points","teleop":"180–260 points","rate":"Target rapid Artifact acquisition/indexing and repeatable high-value scoring with minimal setup time.","cycles":"Acquire → index/sort → score → return; automate repetitive aiming and positioning.","avoid":["Treat orientation-independent/turret scoring as a later upgrade unless it clearly improves throughput.","Keep secondary specialization below primary scoring reliability and autonomous development."]},
        "T2":{"auto":"45–70 points","teleop":"145–220 points","rate":"Target fast Artifact cycles with high scoring accuracy and low jam rate.","cycles":"Wide intake → buffered indexing → repeatable scoring; protect autonomous and driver practice.","avoid":["Defer high-complexity orientation independence until the base scorer is mature.","Keep secondary mechanisms from reducing intake/indexing reliability."]},
        "T3":{"auto":"35–60 points","teleop":"110–175 points","rate":"Target repeatable scoring cycles with automated alignment where it saves driver time.","cycles":"Acquire → index → preferred scoring location → reacquire.","avoid":["Treat turret-level complexity as lower priority than reliable intake/indexing/scoring.","Keep broad specialization below one strong primary scoring loop."]},
        "T4":{"auto":"25–45 points","teleop":"80–135 points","rate":"Target a forgiving intake and one repeatable scoring solution before expanding capability.","cycles":"Simple acquisition → controlled indexing → preferred scoring location.","avoid":["Prioritize the primary scorer over complex secondary functions.","Prioritize autonomous reliability and driver practice over marginal mechanism breadth."]},
        "T5":{"auto":"15–35 points","teleop":"50–95 points","rate":"Target reliable scoring every match with a low-jam acquisition/indexing path.","cycles":"One acquisition path and one preferred scoring solution.","avoid":["Treat turret/orientation-independent scoring as a lower priority.","Treat secondary scoring breadth as lower priority until the primary loop is reliable."]},
        "T6":{"auto":"5–25 points","teleop":"25–70 points","rate":"Target a legal, repeatable autonomous contribution and one dependable teleop scoring loop.","cycles":"Drive → acquire → score reliably → repeat.","avoid":["Keep optional mechanisms below drivetrain, intake, scoring, and autonomous reliability.","Favor early completion and practice over broad game coverage."]},
    },
    ("FTC", 2027): {
        "T1":{"auto":"80–120+ points target","teleop":"330–430+ points target","rate":"Target a HIVE TIP approximately every 12–18 sec per alliance robot once recycling is established.","cycles":"Acquire/buffer → launch → TIP → immediately reacquire dump; minimize chassis rotation and empty travel.","avoid":["Do not divert both robots to FLOWERS late; keep at least one elite HIVE recycler active.","Add only after a turret unless it measurably reduces seconds/TIP or improves CPR."]},
        "T2":{"auto":"60–100 points","teleop":"260–360 points","rate":"Target a TIP about every 16–22 sec.","cycles":"Reliable multi-element burst + rapid dump reacquisition.","avoid":["Avoid dedicated FLOWER specialization that materially reduces HIVE throughput.","Do not overcomplicate launcher aiming before shot repeatability is high."]},
        "T3":{"auto":"40–80 points","teleop":"190–290 points","rate":"Target a TIP about every 20–28 sec.","cycles":"Wide intake, buffered storage, repeatable preferred shooting zone.","avoid":["Do not start with a turret.","Sequence later unless a sophisticated FLOWER system until HIVE cycles and auto are mature."]},
        "T4":{"auto":"25–60 points","teleop":"130–220 points","rate":"Target a reliable TIP every ~25–35 sec.","cycles":"Simple wide intake + fixed launcher + chassis auto-aim; maximize repeatability.","avoid":["Sequence later unless a turret for Event 1.","Sequence later than complex FLOWER manipulation unless it is mechanically trivial and already reliable."]},
        "T5":{"auto":"15–40 points","teleop":"80–150 points","rate":"Target 2–4 reliable HIVE TIPS in teleop.","cycles":"One preferred shooting location and forgiving intake.","avoid":["Lower priority: turret and complex FLOWER mechanisms.","Prioritize after long-range shooting before preferred-zone accuracy is ≥90–95%."]},
        "T6":{"auto":"5–25 points","teleop":"40–100 points","rate":"Target at least 1–3 repeatable HIVE TIPS per match.","cycles":"Drive, acquire, score reliably, park.","avoid":["Sequence after core capability: every game function.","Prioritize a legal, reliable HIVE scorer and basic autonomous movement/scoring."]},
    },
}

# Historical FRC target contribution ranges at a mid-season reference point.
# Values are robot-contribution targets, not alliance final scores. They provide
# the correct game-specific scale; competition week then adjusts them.
FRC_REFERENCE_TARGETS = {
    2024: {"auto":(20,35),"teleop":(45,80),"rate":"Target repeatable Note cycles with shot preparation occurring while driving.","cycles":"Floor intake -> Speaker scoring; add Amp/Stage only when it improves alliance value."},
    2023: {"auto":(15,30),"teleop":(35,65),"rate":"Target repeatable grid cycles with automated alignment and low placement miss rate.","cycles":"Loading zone/floor acquisition -> high-value grid placement -> charge-station endgame."},
    2022: {"auto":(12,24),"teleop":(30,60),"rate":"Target fast Cargo acquisition and repeatable Hub shooting with minimal aim/setup time.","cycles":"Acquire Cargo in pairs where practical -> shoot -> reacquire; protect climb time."},
    2020: {"auto":(10,24),"teleop":(30,65),"rate":"Target high-confidence Power Cell bursts and minimize collection-to-shot dead time.","cycles":"Collect -> index -> shoot; add Control Panel only if primary scoring is already mature."},
    2019: {"auto":(9,18),"teleop":(30,55),"rate":"Target fast Hatch/Cargo cycles with alignment assistance.","cycles":"Acquire -> align -> place; prioritize scoring locations that reduce travel and congestion."},
    2018: {"auto":(10,25),"teleop":(35,70),"rate":"Target fast Cube cycles and reliable ownership transitions.","cycles":"Acquire Cube -> score Switch/Scale -> reacquire; preserve endgame climb reliability."},
    2017: {"auto":(15,35),"teleop":(35,75),"rate":"Target repeatable gear/fuel contribution with low station-to-score travel loss.","cycles":"Specialize around the highest-value repeatable scoring loop; protect climb reliability."},
    2016: {"auto":(10,25),"teleop":(30,65),"rate":"Target reliable defense crossing plus high-confidence goal scoring.","cycles":"Cross defenses efficiently -> acquire -> score; avoid low-value mechanism breadth."},
}

TRANCHE_TARGET_FACTOR={"T1":1.45,"T2":1.25,"T3":1.05,"T4":0.85,"T5":0.65,"T6":0.45}

def _week_factor(event_week):
    # Week 1 is the opening-event target. Growth tapers late in the season.
    w=max(1,min(8,int(event_week)))
    return {1:0.78,2:0.86,3:0.94,4:1.00,5:1.07,6:1.13,7:1.18,8:1.22}[w]

def _scale_range(text,factor):
    import re
    nums=re.findall(r"\d+(?:\.\d+)?",str(text))
    if len(nums)<2:return text
    lo=int(round(float(nums[0])*factor)); hi=int(round(float(nums[1])*factor))
    suffix=" Fuel points" if "Fuel" in str(text) else " points"
    plus="+" if "+" in str(text) else ""
    return f"{lo}–{hi}{plus}{suffix}"

def performance_targets(program, season, tranche, event_week=4):
    game=PERFORMANCE_TARGETS.get((program,int(season)),{})
    factor=_week_factor(event_week)
    if tranche in game:
        base=dict(game[tranche])
        base["auto"]=_scale_range(base["auto"],factor)
        base["teleop"]=_scale_range(base["teleop"],factor)
        base["week_note"]=f"Week {event_week} target; week factor {factor:.2f} relative to the mid-season reference."
        return base
    if program=="FRC" and int(season) in FRC_REFERENCE_TARGETS:
        ref=FRC_REFERENCE_TARGETS[int(season)]
        tf=TRANCHE_TARGET_FACTOR.get(tranche,1.0)
        f=tf*factor
        alo,ahi=ref["auto"]; tlo,thi=ref["teleop"]
        return {
            "auto":f"{round(alo*f)}–{round(ahi*f)} points",
            "teleop":f"{round(tlo*f)}–{round(thi*f)} points",
            "rate":ref["rate"],
            "cycles":ref["cycles"],
            "avoid":["Add only after marginal capabilities before the primary scoring loop is reliable.","Prioritize after peak speed before integration and contested testing."],
            "week_note":f"Week {event_week} target scaled for the selected team's hidden history rating."
        }
    return {"auto":"Game-specific numeric target not yet encoded","teleop":"Game-specific numeric target not yet encoded","rate":"Measure top-tier scoring rate from live data before setting a numeric target.","cycles":"Optimize the highest-value repeatable scoring loop.","avoid":["Add only after marginal capabilities before the primary scoring loop is reliable.","Prioritize after peak speed before integration and contested testing."],"week_note":f"Week {event_week}"}


TAILOR_LEVELS=("A","B","C","D","E")
TRANCHE_BOUNDS={"T1":(85,100),"T2":(75,85),"T3":(63,75),"T4":(48,63),"T5":(32,48),"T6":(0,32)}
TAILOR_FACTOR={"A":0.88,"B":0.94,"C":1.00,"D":1.06,"E":1.12}

def tailoring_level(tranche, composite):
    """Map continuous historical capacity to an A-E quintile inside its tranche."""
    if composite is None:return "A"
    lo,hi=TRANCHE_BOUNDS.get(tranche,(0,100))
    width=max(1e-9,hi-lo)
    q=max(0.0,min(0.999999,(float(composite)-lo)/width))
    return TAILOR_LEVELS[min(4,int(q*5))]

def build_lookup_cell(program,season,tranche,tailor,event_week):
    """Canonical Game x Tranche x Tailoring x Week recommendation package."""
    base=performance_targets(program,season,tranche,event_week)
    tf=TAILOR_FACTOR[tailor]
    out=dict(base)
    out["auto"]=_scale_range(base["auto"],tf)
    out["teleop"]=_scale_range(base["teleop"],tf)
    out["features"]=robot_features(program,season,tranche)
    out["tranche"]=tranche;out["tailoring"]=tailor;out["week"]=int(event_week)
    out["lookup_key"]=f"{program}:{int(season)}:{tranche}:{tailor}:W{int(event_week)}"
    return out

def build_game_lookup(program,season):
    return {(t,a,w):build_lookup_cell(program,season,t,a,w)
            for t in ("T1","T2","T3","T4","T5","T6")
            for a in TAILOR_LEVELS for w in range(1,9)}

def lookup_recommendation(program,season,tranche,composite,event_week):
    a=tailoring_level(tranche,composite)
    return build_lookup_cell(program,season,tranche,a,event_week)

def derivation_text(program, season, tranche):
    return (
        f"Derived from Model 5.4 using the selected {program} {season} game structure, "
        "pre-season team execution history, competition-week maturity, autonomous leverage, "
        "scoring throughput and travel/cycle economics, game-piece availability, endgame opportunity cost, "
        "reliability, Contested Performance Retention, and alliance complementarity. "
        "The backend uses a hidden team-capacity band to scale design breadth and risk; it is not a public ranking. "
        "Numeric values are planning targets, not official FIRST benchmarks, and should be replaced by measured "
        "current-season performance as event data accumulates."
    )
