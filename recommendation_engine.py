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
