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
    headers={"X-TBA-Auth-Key":key}; base="https://www.thebluealliance.com/api/v3"
    events=_get_json(f"{base}/team/frc{int(team)}/events/{int(year)}",headers=headers)
    statuses=_get_json(f"{base}/team/frc{int(team)}/events/{int(year)}/statuses",headers=headers)
    return {"events":events,"statuses":statuses},None

def _tba_year_score(data):
    """Return 0..100 event-performance score and evidence from TBA statuses."""
    if not data:return None,[]
    events={e.get("key"):e for e in data.get("events",[]) if isinstance(e,dict)}
    statuses=data.get("statuses",{}) or {}; vals=[]; evidence=[]
    for key,status in statuses.items():
        if not isinstance(status,dict):continue
        ev=events.get(key,{})
        rank=(status.get("qual") or {}).get("ranking",{})
        r=rank.get("rank"); n=rank.get("num_teams")
        qual_score=None
        if r and n and n>1:qual_score=100*(1-(r-1)/(n-1))
        playoff=status.get("playoff") or {}; level=str(playoff.get("level") or "")
        playoff_score={"won":100,"f":90,"sf":80,"qf":70,"ef":60}.get(level.lower(),50 if playoff else 35)
        alliance=status.get("alliance") or {}; pick=alliance.get("pick")
        draft_score=85 if pick==0 else (75 if pick==1 else (65 if pick==2 else 50))
        if qual_score is None:qual_score=50
        score=.45*qual_score+.35*playoff_score+.20*draft_score
        vals.append(score)
        name=ev.get("name",key)
        evidence.append(f'{year if False else ""}{name}: qualification rank {r if r else "n/a"} of {n if n else "n/a"}; playoff {level or "none"}; alliance pick {pick if pick is not None else "n/a"}')
    return (sum(vals)/len(vals) if vals else None),evidence

def _tranche_from_score(score):
    if score>=90:return "T1"
    if score>=80:return "T2"
    if score>=68:return "T3"
    if score>=52:return "T4"
    if score>=35:return "T5"
    return "T6"

def ftcscout_team(team): return _get_json(f"https://api.ftcscout.org/rest/v1/teams/{int(team)}")
def first_ftc_results_link(season): return f"https://ftc-events.firstinspires.org/{int(season)-1}/"
def robotevents_team(team):
    token=_secret("ROBOTEVENTS_TOKEN")
    if not token:return None,"ROBOTEVENTS_TOKEN not configured"
    return _get_json("https://www.robotevents.com/api/v2/teams",headers={"Authorization":f"Bearer {token}"},params={"number[]":team}),None
def infer_frc_profile(team,season):
    """Composite pre-season FRC Team Execution Capacity from Statbotics + TBA."""
    years=range(max(2002,int(season)-3),int(season)); sb=[]; tba_rows=[]; evidence=[]
    for year in years:
        try:
            row=statbotics_team_year(team,year); pct=row.get("total_epa_percentile")
            if pct is not None:
                pct=float(pct);pct=pct*100 if pct<=1 else pct
                sb.append({"year":year,"percentile":pct,"rank":row.get("total_epa_rank"),"team_count":row.get("total_team_count")})
                evidence.append(f'Statbotics {year}: {pct:.1f}th EPA percentile')
        except Exception:pass
        try:
            data,err=tba_team_year(team,year)
            if not err:
                score,ev=_tba_year_score(data)
                if score is not None:tba_rows.append({"year":year,"score":score})
                evidence.extend([f"TBA {year}: {x}" for x in ev])
        except Exception:pass
    if not sb and not tba_rows:return None
    sb_score=sb[-1]["percentile"] if sb else None
    tba_score=tba_rows[-1]["score"] if tba_rows else None
    # 40% EPA strength, 60% translated event execution. When one source is
    # unavailable, use the available source and clearly expose that fact.
    if sb_score is not None and tba_score is not None: composite=.40*sb_score+.60*tba_score;source="Statbotics + The Blue Alliance"
    elif sb_score is not None:composite=sb_score;source="Statbotics only (TBA unavailable)"
    else:composite=tba_score;source="The Blue Alliance only (Statbotics unavailable)"
    tranche=_tranche_from_score(composite)
    history=[]
    for year in years:
        sp=next((x["percentile"] for x in sb if x["year"]==year),None)
        tp=next((x["score"] for x in tba_rows if x["year"]==year),None)
        if sp is not None and tp is not None:history.append((year,.40*sp+.60*tp))
        elif sp is not None:history.append((year,sp))
        elif tp is not None:history.append((year,tp))
    if len(history)>=2 and history[-1][1]>=history[0][1]+5:trajectory="Rising"
    elif len(history)>=2 and history[-1][1]<=history[0][1]-5:trajectory="Declining"
    else:trajectory="Stable"
    return {"tranche":tranche,"trajectory":trajectory,"source":source,"composite":composite,"statbotics_score":sb_score,"tba_score":tba_score,"evidence":evidence,"history":history}

def live_snapshot(program,team,season):
    out={"program":program,"team":team,"season":int(season),"checked_at":datetime.now(timezone.utc).isoformat(),"manuals":manual_links(program,season),"sources":[],"warnings":[],"profile":None}
    if program=="FRC":
        try:
            out["profile"]=infer_frc_profile(team,season)
            if out["profile"]:
                source_name=out["profile"].get("source","")
                if "Statbotics" in source_name:
                    out["sources"].append("Statbotics historical tranche data")
                if "Blue Alliance" in source_name and "TBA unavailable" not in source_name:
                    out["sources"].append("The Blue Alliance historical tranche data")
        except Exception as exc:
            out["warnings"].append(f"FRC tranche classifier unavailable: {exc}")
        try:
            data,err=tba_team_year(team,season)
            if err:
                out["warnings"].append(err)
            else:
                out["tba"]=data
                out["sources"].append("The Blue Alliance live")
        except Exception as exc:
            out["warnings"].append(f"The Blue Alliance unavailable: {exc}")
    elif program=="FTC":
        try:
            out["ftcscout"]=ftcscout_team(team)
            out["sources"].append("FTCScout live")
        except Exception as exc:
            out["warnings"].append(f"FTCScout unavailable: {exc}")
        out["first_events"]=first_ftc_results_link(season)
        out["sources"].append("FIRST FTC Events link")
    else:
        try:
            data,err=robotevents_team(team)
            if err:
                out["warnings"].append(err)
            else:
                out["robotevents"]=data
                out["sources"].append("RobotEvents live")
        except Exception as exc:
            out["warnings"].append(f"RobotEvents unavailable: {exc}")
    return out
