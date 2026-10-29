from backtest_observed import evaluate,aggregate
rows=[
 {"program":"FRC","season":"2025","team":"254","week":"1","observed_percentile":"95"},
 {"program":"FRC","season":"2025","team":"254","week":"6","observed_percentile":"98"},
 {"program":"FTC","season":"2025","team":"11260","week":"3","observed_percentile":"90"},
 {"program":"VEX","season":"2025","team":"1234A","week":"2","observed_percentile":"50"},
]
profiles={
 ("FRC",2025,"254"):{"tranche":"T1","composite":97},
 ("FTC",2025,"11260"):{"tranche":"T1","composite":93},
}
out,skipped=evaluate(rows,profiles)
assert len(out)==3 and len(skipped)==1
assert len(aggregate(out,["program","week"]))==3
assert out[0]["predicted"]==out[1]["predicted"]
assert out[0]["observed"]!=out[1]["observed"]
assert all(0<=r["score"]<=100 for r in out)
print("Observed backtest grouping, week sensitivity and exclusions passed")
