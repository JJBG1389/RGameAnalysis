import os,sys,re
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from recommendation_engine import performance_targets

def first_num(s):
    m=re.search(r"\d+",s); return int(m.group()) if m else None

fail=[]
for year in [2016,2017,2018,2019,2020,2022,2023,2024,2025,2026]:
    w1=performance_targets("FRC",year,"T3",1)
    w6=performance_targets("FRC",year,"T3",6)
    print(year,"W1",w1["auto"],w1["teleop"],"W6",w6["auto"],w6["teleop"])
    if "not yet encoded" in w1["auto"] or "not yet encoded" in w1["teleop"]:
        fail.append(f"{year}: numeric targets missing")
    if first_num(w6["auto"]) <= first_num(w1["auto"]):
        fail.append(f"{year}: auto target does not rise from week 1 to week 6")
    if first_num(w6["teleop"]) <= first_num(w1["teleop"]):
        fail.append(f"{year}: teleop target does not rise from week 1 to week 6")

# Team-history tier must still change the target for the same game/week.
for year in [2016,2023,2024,2025,2026]:
    t1=performance_targets("FRC",year,"T1",3)
    t5=performance_targets("FRC",year,"T5",3)
    if first_num(t1["teleop"]) <= first_num(t5["teleop"]):
        fail.append(f"{year}: T1 teleop target not above T5")

if fail:
    print("FAILURES")
    for x in fail: print("-",x)
    raise SystemExit(1)
print("FRC week/history scoring regression passed.")
