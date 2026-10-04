"""Ten-year FTC powerhouse regression/backtest.

For each requested team, evaluate each UI season using only prior FTCScout data.
This is a leakage-safe historical capacity test, not a test of that season's
event outcome. Missing seasons are reported, not fabricated.
"""
import os,sys
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from data_sources import infer_ftc_profile

TEAMS={
"18215":"Couch Potatoes","14270":"Quantum Robotics","20464":"I.F. Robotics",
"9879":"Root Negative One","16750":"TechnicBots","3888":"Greased Lightning",
"11256":"Duct Tape","14481":"Don't Blink","10644":"CyBugs",
"14353":"The N.E.R.D.-bots!","23373":"Viking Warriors","11260":"Up-A-Creek Robotics",
"22509":"Overdrive",
}
# UI ending years. 2021 retained for FTC because Ultimate Goal had official
# competition data, but missing API history is allowed and reported.
YEARS=list(range(2018,2028))
rows=[];fail=[]
for team,name in TEAMS.items():
    usable=0; upper=0
    for year in YEARS:
        p=infer_ftc_profile(team,year)
        if not p:
            rows.append((team,name,year,"NO_DATA",None))
            continue
        usable+=1
        tier=p["tranche"]; score=p.get("composite")
        if tier in ("T1","T2"): upper+=1
        rows.append((team,name,year,tier,score))
    # Established powerhouse sample should have some usable historical record.
    if usable==0: fail.append(f"{team} {name}: no usable history in 10-year window")
    print(team,name,"usable",usable,"upper",upper)
    for r in rows[-10:]: print(" ",r[2],r[3],None if r[4] is None else round(r[4],1))

# Sanity: test must cover multiple historical years and not collapse every
# usable output into one tier.
tiers={r[3] for r in rows if r[3]!="NO_DATA"}
if len(tiers)<3: fail.append(f"historical outputs collapsed into only {sorted(tiers)}")
if fail:
    print("FAILURES")
    for x in fail: print("-",x)
    raise SystemExit(1)
print("FTC 10-year powerhouse regression passed.")
