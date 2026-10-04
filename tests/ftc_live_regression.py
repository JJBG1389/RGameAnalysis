"""Live FTC classifier regression tests. Requires public FTCScout only."""
import os,sys
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from data_sources import infer_ftc_profile

# Championship winners should calibrate as elite entering the following season.
ELITE = [
    ("19066", 2025), ("11212", 2025), ("18763", 2025),  # 2024 world winners
    ("11260", 2026), ("20870", 2026), ("19746", 2026),  # 2025 world winners
    ("30030", 2027), ("21087", 2027), ("11228", 2027),  # 2026 world winners
]

# Broader field sanity sample: intended to make sure the classifier does not
# collapse everyone into one bucket. Exact tiers are not hard-coded because
# team strength changes by season.
FIELD = [
    ("23435", 2027), ("12857", 2027), ("16930", 2027),
    ("25872", 2027), ("23954", 2027), ("14503", 2027),
    ("30784", 2027), ("18140", 2027), ("25943", 2027),
]

fail=[]
elite_rows=[]
for team,season in ELITE:
    p=infer_ftc_profile(team,season)
    print("ELITE",team,season,p)
    if not p:
        fail.append(f"{team}/{season}: no FTC profile")
    elif p["tranche"]!="T1":
        fail.append(f"{team}/{season}: expected T1, got {p['tranche']} ({p['composite']:.1f})")
    else:
        elite_rows.append(p)

field_tiers=[]
for team,season in FIELD:
    p=infer_ftc_profile(team,season)
    print("FIELD",team,season,p)
    if p: field_tiers.append(p["tranche"])

if len(field_tiers)<5:
    fail.append("Too few broader-field FTC teams returned usable profiles")
if len(set(field_tiers))<2:
    fail.append(f"Broader FTC field collapsed into too few tiers: {sorted(set(field_tiers))}")

if fail:
    print("\nFAILURES")
    for x in fail: print("-",x)
    raise SystemExit(1)
print("\nFTC live regression passed.")
