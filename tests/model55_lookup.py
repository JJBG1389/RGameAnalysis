import os,sys,re
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from recommendation_engine import build_game_lookup,tailoring_level
GAMES=[("FRC",y) for y in (2016,2017,2018,2019,2020,2022,2023,2024,2025,2026)]+[("FTC",y) for y in range(2018,2028)]+[("VEX",y) for y in range(2017,2027)]
fail=[]
for p,y in GAMES:
    table=build_game_lookup(p,y)
    if len(table)!=240: fail.append(f"{p} {y}: {len(table)} cells, expected 240")
    for t in ("T1","T2","T3","T4","T5","T6"):
        vals=[]
        for a in "ABCDE":
            x=table[(t,a,4)]
            n=re.findall(r"\d+(?:\.\d+)?",x["teleop"])
            if not n: fail.append(f"{p} {y} {t}{a}: no numeric teleop: {x['teleop']!r}")
            else: vals.append(float(n[0]))
            if not x["features"]["must"]: fail.append(f"{p} {y} {t}{a}: no must features")
        if len(vals)==5 and vals!=sorted(vals): fail.append(f"{p} {y} {t}: tailoring not monotonic {vals}")
        w1=table[(t,"C",1)];w8=table[(t,"C",8)]
        n1=re.findall(r"\d+(?:\.\d+)?",w1["teleop"]);n8=re.findall(r"\d+(?:\.\d+)?",w8["teleop"])
        if not n1 or not n8: fail.append(f"{p} {y} {t}: nonnumeric W1/W8 teleop")
        elif float(n8[0])<=float(n1[0]): fail.append(f"{p} {y} {t}: W8 <= W1")
for t,(lo,hi) in {"T1":(85,100),"T2":(75,85),"T3":(63,75),"T4":(48,63),"T5":(32,48),"T6":(0,32)}.items():
    if tailoring_level(t,lo+0.01)!="A":fail.append(f"{t} lower boundary not A")
    if tailoring_level(t,hi-0.01)!="E":fail.append(f"{t} upper boundary not E")
if fail:
    print("MODEL 5.5 LOOKUP FAILURES")
    for x in fail:print("-",x)
    raise SystemExit(1)
print(f"Model 5.5 lookup validation passed across {len(GAMES)} games / {len(GAMES)*240} cells.")
