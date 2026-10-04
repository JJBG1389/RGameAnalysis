"""Pre-deploy smoke/regression tests for live tranche classification.

Run:
    python tests/live_smoke_test.py

Credentialed sources:
    TBA_AUTH_KEY          FRC composite classification
    ROBOTEVENTS_TOKEN     VEX live classification (once VEX classifier is enabled)

The test is deliberately diagnostic: it prints source evidence and exits nonzero
when required classification behavior fails.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data_sources import live_snapshot

FRC_CASES = [
    # User-requested sanity cases
    ("254", 2026), ("971", 2026), ("1389", 2026), ("6964", 2026),
    # Broader regression sample intended to exercise different historical tiers
    ("1678", 2026), ("2056", 2026), ("4414", 2026), ("6328", 2026),
    ("3132", 2026), ("3847", 2026), ("4907", 2026), ("7460", 2026),
]

# FTCScout public API connectivity/identity smoke cases. The classifier is not
# yet allowed to invent a tranche until percentile/event normalization is added.
FTC_CASES = ["11260", "19705", "20265", "9879", "12808", "10809"]

# RobotEvents connectivity/identity smoke cases. V5 team numbers are strings.
# Keep a varied set and validate live retrieval before enabling auto-tranche.
VEX_CASES = ["169A", "5225A", "315K", "2011B", "62A", "8059A"]


def check_frc():
    failures=[]; results=[]
    for team,season in FRC_CASES:
        snap=live_snapshot("FRC",team,season); p=snap.get("profile")
        row={"team":team,"tranche":p.get("tranche") if p else None,
             "composite":p.get("composite") if p else None,
             "sb":p.get("statbotics_score") if p else None,
             "tba":p.get("tba_score") if p else None,
             "source":p.get("source") if p else None,
             "warnings":snap.get("warnings",[])}
        results.append(row); print("FRC",row)
        if not p: failures.append(f"FRC {team}: no tranche")
        elif p.get("composite") is None: failures.append(f"FRC {team}: no composite TEC")
        elif "Statbotics" not in p.get("source",""): failures.append(f"FRC {team}: Statbotics missing")
        elif os.getenv("TBA_AUTH_KEY") and "Blue Alliance" not in p.get("source",""):
            failures.append(f"FRC {team}: TBA missing despite configured key")
    # Regression guard for the original bug: requested teams must not all
    # collapse to the same tranche due to a parser/default failure.
    requested=[r["tranche"] for r in results[:4] if r["tranche"]]
    if len(requested)==4 and len(set(requested))==1:
        failures.append("FRC 254/971/1389/6964 all received the same tranche; investigate parser/scoring")
    return failures


def check_ftc():
    failures=[]
    for team in FTC_CASES:
        snap=live_snapshot("FTC",team,2026)
        ok=bool(snap.get("ftcscout"))
        print("FTC",team,"FTCScout",ok,"warnings",snap.get("warnings"))
        if not ok: failures.append(f"FTC {team}: FTCScout lookup failed")
        # Intentional: no auto tranche until normalized FTC classifier exists.
        if snap.get("profile") is not None:
            failures.append(f"FTC {team}: unexpected auto tranche before FTC classifier validation")
    return failures


def check_vex():
    failures=[]
    for team in VEX_CASES:
        snap=live_snapshot("VEX",team,2026)
        if os.getenv("ROBOTEVENTS_TOKEN"):
            ok=bool(snap.get("robotevents"))
            print("VEX",team,"RobotEvents",ok,"warnings",snap.get("warnings"))
            if not ok: failures.append(f"VEX {team}: RobotEvents lookup failed")
        else:
            print("VEX",team,"SKIP live RobotEvents: ROBOTEVENTS_TOKEN not configured")
    return failures


if __name__=="__main__":
    failures=check_frc()+check_ftc()+check_vex()
    if failures:
        print("\nFAILURES")
        for f in failures: print("-",f)
        raise SystemExit(1)
    print("\nAll configured live smoke tests passed.")
