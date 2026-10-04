import streamlit as st
from recommendation_engine import recommend,worlds_delta,TRANCHE_LABELS,TRAJECTORIES
from data_sources import live_snapshot
st.set_page_config(page_title="RGameAnalysis Team Advisor",page_icon="🤖",layout="wide")
st.title("RGameAnalysis Team Advisor");st.caption("Model 5.3 · live source adapters · tranche-aware first-event + Worlds planning")
with st.sidebar:
 st.header("Team & season");program=st.selectbox("Program",["FRC","FTC","VEX"]);season=st.number_input("Season ending year",2010,2035,2027);team=st.text_input("Team number","6964");event_week=st.slider("First event competition week",1,8,1);worlds_plan=st.toggle("Team plans to attend World Championship",False)
 st.divider();st.subheader("Current maturity");primary_gate=st.select_slider("Primary scoring capability",["Exists","Reliable","Integrated","Contested","Optimized"],value="Integrated");auto_reliability=st.slider("Autonomous reliability (%)",0,100,80,5);robot_reliability=st.slider("Match reliability (%)",0,100,90,5);cpr=st.slider("Contested performance retention (%)",0,100,75,5);refresh=st.button("Refresh live data",use_container_width=True)
@st.cache_data(ttl=900,show_spinner=False)
def get_live(p,t,s):return live_snapshot(p,t,s)
if refresh:get_live.clear()
with st.spinner("Checking live competition sources…"):live=get_live(program,team.strip(),int(season))
profile=live.get("profile")
if profile:tranche=profile["tranche"];trajectory=profile["trajectory"];profile_note=f"Auto-classified from {profile['source']} using only seasons before {season}."
else:
 st.sidebar.divider();st.sidebar.subheader("Provisional team profile");st.sidebar.caption("Automatic classification is not yet available from the connected source for this program/team.");tranche=st.sidebar.selectbox("Team tranche",list(TRANCHE_LABELS),index=3);trajectory=st.sidebar.selectbox("Trajectory",TRAJECTORIES,index=0);profile_note="Manual provisional classification."
result=recommend(program,int(season),team.strip(),event_week,tranche,trajectory,primary_gate,auto_reliability,robot_reliability,cpr)
st.caption(profile_note);c1,c2,c3,c4=st.columns(4);c1.metric("Team profile",f"{result['tranche']} {result['trajectory_symbol']}");c2.metric("First-event stage",result["stage_code"]);c3.metric("Reliability",f"{robot_reliability}%");c4.metric("CPR",f"{cpr}%")
st.subheader("First-event recommendation");st.markdown(f"### {result['headline']}");st.write(result["summary"]);l,r=st.columns(2)
with l:
 st.markdown("#### Highest-value work")
 for x in result["priorities"]:st.markdown(f"- {x}")
 st.info(result["maturity_action"])
with r:
 st.markdown("#### Do less of")
 for x in result["avoid"]:st.markdown(f"- {x}")
 st.success(result["event_target"])
st.markdown("#### Development allocation");st.bar_chart(result["allocation"],horizontal=True)
if worlds_plan:
 d=worlds_delta(result,tranche,trajectory,auto_reliability,robot_reliability,cpr);st.divider();st.subheader("World Championship delta plan");st.write("Keep the first-event plan above. These are the additional deltas to peak again at Worlds.");a,b=st.columns(2)
 with a:
  st.markdown("#### Implement after Event 1")
  for x in d["deltas"]:st.markdown(f"- {x}")
 with b:
  st.markdown("#### Worlds targets")
  for x in d["targets"]:st.markdown(f"- {x}")
  st.warning(d["guardrail"])
st.divider();st.subheader("Live source status");a,b=st.columns(2)
with a:
 st.markdown("#### Official game/manual sources")
 for label,url in live["manuals"].items():st.markdown(f"- [{label}]({url})")
 if program=="FTC" and live.get("first_events"):st.markdown(f"- [FIRST FTC Event Results]({live['first_events']})")
with b:
 st.markdown("#### Competition data")
 for source in live["sources"]:st.markdown(f"- ✅ {source}")
 for warning in live["warnings"]:st.markdown(f"- ⚠️ {warning}")
with st.expander("API configuration"):
 st.write("Statbotics and FTCScout are queried directly. The Blue Alliance requires TBA_AUTH_KEY. RobotEvents requires ROBOTEVENTS_TOKEN. Missing credentialed sources degrade gracefully.")
