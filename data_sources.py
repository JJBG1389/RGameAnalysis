import os
from datetime import datetime, timezone
import requests

try:
    import streamlit as st
except ImportError:
    st = None

TIMEOUT = 12

def _secret(name):
    """Read a credential from Streamlit Cloud secrets first, then the OS environment."""
    if st is not None:
        try:
            value = st.secrets.get(name)
            if value:
                return str(value).strip()
        except Exception:
            pass
    return os.getenv(name, "").strip()
MANUAL_SOURCES = {
    "FRC": {"current": "https://www.firstinspires.org/programs/frc/game-and-season", "archive": "https://www.firstinspires.org/resources/library/frc/archived-games"},
    "FTC": {"current": "https://ftc-resources.firstinspires.org/ftc/game", "archive_template": "https://ftc-resources.firstinspires.org/ftc/archive/{year}/game"},
    "VEX": {"current": "https://www.vexrobotics.com/v5/competition", "manual": "https://www.vexrobotics.com/override-manual"},
}
def _get_json(url, headers=None, params=None):
    r=requests.get(url,headers=headers or {},params=params or {},timeout=TIMEOUT); r.raise_for_status(); return r.json()
def manual_links(program,season):
    if program=="FTC": return {"Official current materials":MANUAL_SOURCES["FTC"]["current"],"Official season archive":MANUAL_SOURCES["FTC"]["archive_template"].format(year=season)}
    if program=="FRC": return {"Official current materials":MANUAL_SOURCES["FRC"]["current"],"Official game archive":MANUAL_SOURCES["FRC"]["archive"]}
    return {"Official current competition page":MANUAL_SOURCES["VEX"]["current"],"Official current manual":MANUAL_SOURCES["VEX"]["manual"]}
def statbotics_team_year(team,year): return _get_json(f"https://api.statbotics.io/v3/team_year/{int(team)}/{int(year)}")
def tba_team_year(team,year):
    key=_secret("TBA_AUTH_KEY")
    if not key:return None,"TBA_AUTH_KEY not configured"
    return _get_json(f"https://www.thebluealliance.com/api/v3/team/frc{int(team)}/events/{int(year)}/statuses",headers={"X-TBA-Auth-Key":key}),None
def ftcscout_team(team): return _get_json(f"https://api.ftcscout.org/rest/v1/teams/{int(team)}")
def first_ftc_results_link(season): return f"https://ftc-events.firstinspires.org/{int(season)-1}/"
def robotevents_team(team):
    token=_secret("ROBOTEVENTS_TOKEN")
    if not token:return None,"ROBOTEVENTS_TOKEN not configured"
    return _get_json("https://www.robotevents.com/api/v2/teams",headers={"Authorization":f"Bearer {token}"},params={"number[]":team}),None
def infer_frc_profile(team,season):
    """Infer FRC tranche from pre-season Statbotics team-year percentiles.

    Statbotics v3 TeamYear exposes flat fields including total_epa_rank,
    total_epa_percentile, and total_team_count. We use the latest available
    pre-season percentile for tranche and the 3-year percentile change for
    trajectory. We never silently default to T4 when data is missing.
    """
    rows=[]
    for year in range(max(2002,int(season)-3),int(season)):
        try:
            row=statbotics_team_year(team,year)
            pct=row.get("total_epa_percentile") if isinstance(row,dict) else None
            rank=row.get("total_epa_rank") if isinstance(row,dict) else None
            count=row.get("total_team_count") if isinstance(row,dict) else None
            if pct is not None:
                pct=float(pct)
                pct=pct*100 if pct<=1 else pct
                rows.append({"year":year,"percentile":pct,"rank":rank,"team_count":count,"raw":row})
        except Exception:
            pass
    if not rows:
        return None

    latest=rows[-1]; pct=latest["percentile"]
    # Quantile bands: top 2%, next 8%, next 15%, next 25%, next 30%, bottom 20%.
    if pct>=98: tranche="T1"
    elif pct>=90: tranche="T2"
    elif pct>=75: tranche="T3"
    elif pct>=50: tranche="T4"
    elif pct>=20: tranche="T5"
    else: tranche="T6"

    if len(rows)>=2 and rows[-1]["percentile"]>=rows[0]["percentile"]+5: trajectory="Rising"
    elif len(rows)>=2 and rows[-1]["percentile"]<=rows[0]["percentile"]-5: trajectory="Declining"
    else: trajectory="Stable"

    evidence=[]
    for r in rows:
        detail=f'{r["year"]}: {r["percentile"]:.1f}th EPA percentile'
        if r["rank"] is not None and r["team_count"] is not None:
            detail+=f' (rank {r["rank"]} of {r["team_count"]})'
        evidence.append(detail)

    return {
        "tranche":tranche,
        "trajectory":trajectory,
        "source":"Statbotics",
        "latest_history_year":latest["year"],
        "percentile":pct,
        "rank":latest["rank"],
        "team_count":latest["team_count"],
        "evidence":evidence,
    }

def live_snapshot(program,team,season):
    out={"program":program,"team":team,"season":int(season),"checked_at":datetime.now(timezone.utc).isoformat(),"manuals":manual_links(program,season),"sources":[],"warnings":[],"profile":None}
    if program=="FRC":
        try:
            out["profile"]=infer_frc_profile(team,season); out["sources"].append("Statbotics live")
        except Exception as exc:out["warnings"].append(f"Statbotics unavailable: {exc}")
        try:
            data,err=tba_team_year(team,season)
            if err:out["warnings"].append(err)
            else:out["tba"]=data; out["sources"].append("The Blue Alliance live")
        except Exception as exc:out["warnings"].append(f"The Blue Alliance unavailable: {exc}")
    elif program=="FTC":
        try:out["ftcscout"]=ftcscout_team(team); out["sources"].append("FTCScout live")
        except Exception as exc:out["warnings"].append(f"FTCScout unavailable: {exc}")
        out["first_events"]=first_ftc_results_link(season); out["sources"].append("FIRST FTC Events link")
    else:
        try:
            data,err=robotevents_team(team)
            if err:out["warnings"].append(err)
            else:out["robotevents"]=data; out["sources"].append("RobotEvents live")
        except Exception as exc:out["warnings"].append(f"RobotEvents unavailable: {exc}")
    return out
