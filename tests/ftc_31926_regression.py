import os,sys
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from data_sources import infer_ftc_profile

# 31926 has FTCScout DECODE (season-start 2025) data. UI 2027 BIOBUZZ
# must find that history through the ending-year -> starting-year mapping.
p=infer_ftc_profile("31926",2027)
print("31926/2027",p)
assert p is not None, "31926 must return an FTC profile"
assert p.get("history"), "31926 must use actual prior FTCScout QuickStats, not foundation fallback"
years=[y for y,_ in p["history"]]
assert 2025 in years, f"Expected DECODE season-start 2025 in history, got {years}"
assert "no prior-season" not in p.get("source","").lower(), "31926 incorrectly used rookie fallback"
print("FTC 31926 history mapping passed.")
