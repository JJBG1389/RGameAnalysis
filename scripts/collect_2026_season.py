"""Collect raw FTC and VEX 2026 season event data; do not modify model parameters.

Usage:
  python scripts/collect_2026_season.py --program FTC --output-dir collected
  ROBOTEVENTS_TOKEN=... python scripts/collect_2026_season.py --program VEX --output-dir collected

Raw JSON is retained for audit. Collection is bounded and failures are recorded,
not silently interpreted as zero scores.
"""
import argparse,datetime,json,os,time
from pathlib import Path
import requests

FTC_BASE="https://api.ftcscout.org/rest/v1"
VEX_BASE="https://www.robotevents.com/api/v2"

def fetch(session,url,params=None):
    for attempt in range(4):
        response=session.get(url,params=params,timeout=35)
        if response.status_code in (429,500,502,503,504) and attempt<3:
            time.sleep(min(15,2**attempt));continue
        response.raise_for_status()
        return response.json()
    raise RuntimeError("Retries exhausted")

def dump(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False))

def collect_ftc(session,root,limit):
    # FTCScout season keys use the starting year (BIOBUZZ=2026).
    events=fetch(session,f"{FTC_BASE}/events/search/2026",{"hasMatches":"true","end":"2026-11-14","limit":limit})
    if not isinstance(events,list):raise ValueError("Unexpected FTC event search shape")\n    if len(events)>=limit:raise RuntimeError("FTC event search reached the configured limit; dataset may be incomplete. Increase --limit or partition by dates.")
    dump(root/"ftc_events.json",events)
    errors=[];count=0
    for event in events:
        code=event.get("code")
        if not code:continue
        try:
            matches=fetch(session,f"{FTC_BASE}/events/2026/{code}/matches")
            teams=fetch(session,f"{FTC_BASE}/events/2026/{code}/teams")
            dump(root/"ftc"/f"{code}.json",{"event":event,"matches":matches,"teams":teams})
            count+=1
        except (requests.RequestException,ValueError) as exc:
            errors.append({"event":code,"error":str(exc)})
    return {"program":"FTC","events_listed":len(events),"events_saved":count,"errors":errors}

def vex_pages(session,path,params,cap=40):
    records=[];page=1
    while page<=cap:
        data=fetch(session,f"{VEX_BASE}/{path}",{**params,"page":page,"per_page":250})
        if not isinstance(data,dict) or not isinstance(data.get("data"),list):
            raise ValueError(f"Unexpected VEX API response for {path} page {page}")
        records.extend(data["data"])
        meta=data.get("meta") or {}
        last=(meta.get("last_page") or (meta.get("links") or {}).get("last_page"))
        if not data["data"] or (last is not None and page>=int(last)):break
        if len(data["data"])<250:break
        page+=1
    if page>=cap:raise RuntimeError(f"Pagination cap reached: {path}")
    return records

def collect_vex(session,root,limit):
    if not os.environ.get("ROBOTEVENTS_TOKEN"):raise RuntimeError("ROBOTEVENTS_TOKEN missing")
    session.headers.update({"Authorization":"Bearer "+os.environ["ROBOTEVENTS_TOKEN"]})
    # Program 1 is V5RC; 2026-27 Override season ID must be supplied,
    # never guessed from a calendar year.
    season=os.environ.get("VEX_SEASON_ID","204")
    if season!="204":raise RuntimeError("This collector is scoped to V5RC Override (RobotEvents season 204)")
    events=vex_pages(session,"events",{"season[]":season,"program[]":1})\n    events=[e for e in events if str(e.get("start") or "")[:10]<="2026-11-14"][:limit]
    dump(root/"vex_events.json",events)
    errors=[];count=0
    for event in events:
        eid=event.get("id")
        if eid is None:continue
        try:
            teams=vex_pages(session,f"events/{eid}/teams",{})
            skills=vex_pages(session,f"events/{eid}/skills",{})
            # Match results are division-specific.
            divisions=event.get("divisions") or []
            matches={}
            for division in divisions:
                did=division.get("id")
                if did is not None:matches[str(did)]=vex_pages(session,f"events/{eid}/divisions/{did}/matches",{})
            dump(root/"vex"/f"{eid}.json",{"event":event,"teams":teams,"skills":skills,"matches_by_division":matches})
            count+=1
        except (requests.RequestException,ValueError,RuntimeError) as exc:
            errors.append({"event":eid,"error":str(exc)})
    return {"program":"VEX","events_listed":len(events),"events_saved":count,"errors":errors}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--program",choices=("FTC","VEX"),required=True)
    p.add_argument("--output-dir",default="collected")
    p.add_argument("--limit",type=int,default=250)
    args=p.parse_args()
    root=Path(args.output_dir)/datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    with requests.Session() as session:
        session.headers["User-Agent"]="RGameAnalysis research collector/0.1"
        result=collect_ftc(session,root,args.limit) if args.program=="FTC" else collect_vex(session,root,args.limit)
    result["collected_at_utc"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
    result["season"]="2026-27"\n    result["as_of"]="2026-11-14"
    dump(root/f"{args.program.lower()}_manifest.json",result)
    print(json.dumps(result,indent=2))
    if result["errors"]:raise SystemExit(2)

if __name__=="__main__":main()
