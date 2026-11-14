"""Leakage-safe observed-result backtest with explicit missing-data accounting.

Input CSV columns:
program,season,team,week,observed_percentile
The observed percentile must be computed from same-program, same-game,
same-week competition results, not the pre-season classifier inputs.
"""
import argparse,csv,json,collections
from pathlib import Path
from recommendation_engine import tailoring_level,TRANCHE_BOUNDS

def band(p):
    p=float(p)
    for t,(lo,hi) in TRANCHE_BOUNDS.items():
        if lo<=p<hi or (p==100 and hi==100):return t
    raise ValueError("Percentile outside 0..100")

def grade(pred,actual):
    order=[t+a for t in ("T6","T5","T4","T3","T2","T1") for a in "ABCDE"]
    distance=abs(order.index(pred)-order.index(actual))
    return max(0,100-8*distance),distance

def evaluate(rows,profiles):
    out=[];skipped=[]
    for row in rows:
        try:
            program=row["program"];season=int(row["season"]);week=int(row["week"])
            team=str(row["team"]);p=float(row["observed_percentile"])
            assert 1<=week<=8 and 0<=p<=100
            key=(program,season,team)
            prior=profiles.get(key)
            if prior is None or prior.get("composite") is None:
                skipped.append({"key":key,"reason":"missing pre-season history"});continue
            pred_t=prior["tranche"];pred_a=tailoring_level(pred_t,prior["composite"])
            actual_t=band(p);actual_a=tailoring_level(actual_t,p)
            score,distance=grade(pred_t+pred_a,actual_t+actual_a)
            out.append({"program":program,"season":season,"team":team,"week":week,"predicted":pred_t+pred_a,"observed":actual_t+actual_a,"score":score,"distance":distance})
        except (ValueError,TypeError,KeyError,AssertionError) as exc:
            skipped.append({"row":row,"reason":str(exc)})
    return out,skipped

def aggregate(out,dimensions):
    groups=collections.defaultdict(list)
    for row in out:
        groups[tuple(row[d] for d in dimensions)].append(row["score"])
    return [{"group":dict(zip(dimensions,key)),"n":len(vals),"mean_score":round(sum(vals)/len(vals),2)} for key,vals in sorted(groups.items())]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--observations",required=True)
    ap.add_argument("--profiles",required=True,help="Frozen, pre-season profile JSON list")
    ap.add_argument("--output",default="backtest_results.json")
    args=ap.parse_args()
    with open(args.observations,newline="") as f:rows=list(csv.DictReader(f))
    with open(args.profiles) as f:raw=json.load(f)
    profiles={(x["program"],int(x["season"]),str(x["team"])):x for x in raw}
    out,skipped=evaluate(rows,profiles)
    result={"evaluated":len(out),"excluded":len(skipped),"coverage":round(len(out)/len(rows),4) if rows else 0,
      "by_program":aggregate(out,["program"]),"by_game":aggregate(out,["program","season"]),
      "by_week":aggregate(out,["program","week"]),"by_predicted_cell":aggregate(out,["program","predicted"]),
      "by_program_week_cell":aggregate(out,["program","week","predicted"]),
      "exclusions":skipped}
    Path(args.output).write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!="exclusions"},indent=2))
    if not out:raise SystemExit("No valid historical observations; cannot claim accuracy")

if __name__=="__main__":main()
