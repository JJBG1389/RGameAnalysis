"""Score Model 5.5 archetype/tailoring/week cells against observed outcomes.

The production scorer will ingest program-specific observed percentiles:
FRC: Statbotics team-event EPA / component contribution by event week.
FTC: FTCScout QuickStats/event results.
VEX: RobotEvents event results + Robot Skills percentile.
This module defines the common scoring rubric and synthetic invariants so the
three adapters are judged identically.
"""
def score_cell(predicted_band, predicted_tailor, observed_percentile):
    # Convert observed percentile to 30 ordered capacity cells (T6A..T1E).
    p=max(0,min(99.999,float(observed_percentile)))
    bounds=[(0,32,"T6"),(32,48,"T5"),(48,63,"T4"),(63,75,"T3"),(75,85,"T2"),(85,100,"T1")]
    lo=0;hi=100;t="T6"
    for a,b,name in bounds:
        if a<=p<b:lo,hi,t=a,b,name;break
    q=min(4,int(((p-lo)/max(.001,hi-lo))*5))
    obs_tail="ABCDE"[q]
    order=[f"{tt}{aa}" for tt in ("T6","T5","T4","T3","T2","T1") for aa in "ABCDE"]
    pred=f"{predicted_band}{predicted_tailor}";obs=f"{t}{obs_tail}"
    dist=abs(order.index(pred)-order.index(obs))
    # 100 exact; lose 8 points per adjacent tailoring cell.
    return max(0,100-8*dist),obs,dist

assert score_cell("T1","E",99)[0]==100
assert score_cell("T6","A",1)[0]==100
assert score_cell("T3","C",69)[0]>=92
print("Cross-program observed-performance scoring rubric passed.")
