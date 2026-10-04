"""Model 5.4 counterfactual sensitivity gate.

Fails if team capacity, game/year, or competition week does not propagate into
materially different numerical/strategic outputs.
"""
import os,sys,re
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from recommendation_engine import performance_targets, robot_features, recommend

def nums(s):
    return tuple(float(x) for x in re.findall(r"\d+(?:\.\d+)?",str(s))[:2])

fail=[]

# WEEK sensitivity: same team-capacity tier/game, different week.
for program,year,tier in [("FRC",2025,"T3"),("FRC",2024,"T3"),("FRC",2023,"T3"),("FTC",2027,"T3")]:
    a=performance_targets(program,year,tier,1)
    b=performance_targets(program,year,tier,6)
    if nums(a["auto"])==nums(b["auto"]): fail.append(f"{program} {year}: auto unchanged W1->W6")
    if nums(a["teleop"])==nums(b["teleop"]): fail.append(f"{program} {year}: teleop unchanged W1->W6")

# TEAM sensitivity: hidden execution capacity must materially change same game/week.
for program,year in [("FRC",2025),("FRC",2024),("FRC",2023),("FTC",2027)]:
    elite=performance_targets(program,year,"T1",3)
    dev=performance_targets(program,year,"T5",3)
    if nums(elite["auto"])==nums(dev["auto"]): fail.append(f"{program} {year}: T1/T5 auto identical")
    if nums(elite["teleop"])==nums(dev["teleop"]): fail.append(f"{program} {year}: T1/T5 teleop identical")

# GAME sensitivity: same hidden capacity/week must not return identical feature sets.
frc_sets=[tuple(robot_features("FRC",y,"T3")["must"]) for y in (2024,2025,2026)]
if len(set(frc_sets))<3: fail.append("FRC 2024/2025/2026 feature sets are not unique")
ftc_sets=[tuple(robot_features("FTC",y,"T3")["must"]) for y in (2025,2026,2027)]
if len(set(ftc_sets))<3: fail.append("FTC 2025/2026/2027 feature sets are not unique")

# Development-stage sensitivity: later week must change the season stage.
r1=recommend("FRC",2025,"6964",1,"T4","Rising","Reliable",72,88,68)
r6=recommend("FRC",2025,"6964",6,"T4","Rising","Contested",92,95,85)
if r1["stage_code"]==r6["stage_code"]: fail.append("recommendation stage unchanged W1->W6")

if fail:
    print("MODEL 5.4 SENSITIVITY FAILURES")
    for x in fail: print("-",x)
    raise SystemExit(1)
print("Model 5.4 counterfactual sensitivity gate passed.")
