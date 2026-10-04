import os,sys,re
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from recommendation_engine import build_game_lookup,tailoring_level,lookup_recommendation

GAMES=[("FRC",y) for y in (2016,2017,2018,2019,2020,2022,2023,2024,2025,2026)]+[("FTC",y) for y in range(2018,2028)]+[("VEX",y) for y in range(2017,2027)]
fail=[]
for p,y in GAMES:
    table=build_game_lookup(p,y)
    if len(table)!=240: fail.append(f"{p} {y}: {len(table)} cells, expected 240")
    for t in ("T1","T2","T3","T4","T5","T6"):
        # Tailoring must be monotonic inside a tranche for numeric score targets.
        vals=[]
        for a in "ABCDE":
            x=table[(t,a,4)]
            n=re.findall(r"\d+(?:\.\d+)?",x["teleop"])
            if not n: fail.append(f"{p} {y} {t}{a}: no numeric teleop")
            else: vals.append(float(n[0]))
            if not x["features"]["must"]: fail.append(f"{p} {y} {t}{a}: no must features")
        if vals and vals!=sorted(vals): fail.append(f"{p} {y} {t}: tailoring not monotonic {vals}")
        # Week must progress numerically.
        w1=table[(t,"C",1)];w8=table[(t,"C",8)]
        a1=float(re.findall(r"\d+(?:\.\d+)?",w1["teleop"])[0]);a8=float(re.findall(r"\d+(?:\.\d+)?",w8["teleop"])[0])
        if a8<=a1: fail.append(f"{p} {y} {t}: W8 <= W1")
# Boundary mapping checks.
for t,(lo,hi) in {"T1":(85,100),"T2":(75,85),"T3":(63,75),"T4":(48,63),"T5":(32,48),"T6":(0,32)}.items():
    assert tailoring_level(t,lo+0.01)=="A"
    assert tailoring_level(t,hi-0.01)=="E"
if fail:
    print("\n".join(fail));raise SystemExit(1)
print(f"Model 5.5 lookup validation passed across {len(GAMES)} games / {len(GAMES)*240} cells.")
