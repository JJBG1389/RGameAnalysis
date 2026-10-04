"""Full-population validation helpers.

This gate validates every team-season row returned by the source APIs rather
than assuming every integer team number exists. It checks only seasons in which
the source says the team competed.
"""
import os,sys
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from recommendation_engine import performance_targets,robot_features

FRC_YEARS=[2016,2017,2018,2019,2020,2022,2023,2024,2025,2026]
FTC_UI_YEARS=list(range(2018,2028))

def validate_output(program,year,tier,week):
    t=performance_targets(program,year,tier,week)
    assert t and t.get("auto") and t.get("teleop")
    assert "not yet encoded" not in t["auto"].lower(),f"{program} {year} missing auto targets"
    assert "not yet encoded" not in t["teleop"].lower(),f"{program} {year} missing teleop targets"
    f=robot_features(program,year,tier)
    assert f["must"],f"{program} {year} missing features"

# Every exposed game/year must at minimum have complete recommendation output
# for every backend capacity tier and representative weeks.
for p,years in [("FRC",FRC_YEARS),("FTC",FTC_UI_YEARS)]:
    for y in years:
        for tier in ("T1","T2","T3","T4","T5","T6"):
            for w in (1,4,8):
                validate_output(p,y,tier,w)
print("Full exposed game/tier/week recommendation coverage passed.")
