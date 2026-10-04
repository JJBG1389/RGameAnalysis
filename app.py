import streamlit as st
from recommendation_engine import recommend, worlds_delta, robot_features, worlds_feature_delta, performance_targets, derivation_text, TRANCHE_LABELS, TRAJECTORIES, TRANCHE_SHARES
from data_sources import live_snapshot

st.set_page_config(page_title="RGameAnalysis Team Advisor", page_icon="🤖", layout="wide")
st.title("RGameAnalysis Team Advisor")
st.caption("Model 5.4 · Deploy 2026.10.04.22 · live competition data · team-history + week-aware planning")

GAME_OPTIONS = {
    "FRC": {
        2026: "REBUILT", 2025: "REEFSCAPE", 2024: "CRESCENDO", 2023: "CHARGED UP",
        2022: "RAPID REACT", 2020: "INFINITE RECHARGE", 2019: "DESTINATION: DEEP SPACE",
        2018: "FIRST POWER UP", 2017: "FIRST STEAMWORKS", 2016: "FIRST STRONGHOLD",
    },
    "FTC": {
        2027: "BIOBUZZ", 2026: "DECODE", 2025: "INTO THE DEEP", 2024: "CENTERSTAGE",
        2023: "POWERPLAY", 2022: "FREIGHT FRENZY", 2021: "ULTIMATE GOAL",
        2020: "SKYSTONE", 2019: "ROVER RUCKUS", 2018: "RELIC RECOVERY",
    },
    "VEX": {
        2026: "Push Back", 2025: "High Stakes", 2024: "Over Under", 2023: "Spin Up",
        2022: "Tipping Point", 2021: "Change Up", 2020: "Tower Takeover",
        2019: "Turning Point", 2018: "In The Zone", 2017: "Starstruck",
    },
}

with st.sidebar:
    st.header("Team & game")
    program = st.selectbox("Program", ["FRC", "FTC"])
    game_labels = [f"{year} — {name}" for year, name in GAME_OPTIONS[program].items()]
    selected_game = st.selectbox("Game / season", game_labels)
    season = int(selected_game.split(" — ", 1)[0])
    game_name = GAME_OPTIONS[program][season]
    team = st.text_input("Team number", "6964" if program == "FRC" else "")
    event_week = st.slider("Competition week", 1, 8, 1, help="Select the week of the season when this event occurs. Week 1 is the team’s earliest competition period; later weeks allow the model to expect more development and real-match learning.")
    worlds_plan = st.toggle("Team plans to attend World Championship", False, help="Turn this on if the team expects to keep developing for World Championship-level play. The tool gives a first-event plan plus a later list of improvements for Worlds. It does not assume the team should rebuild the robot.")

    st.divider()
    st.subheader("Current readiness")
    st.caption("Model readiness targets change with team history and competition week. Turn this off when you have measured current-robot data.")
    auto_maturity = st.toggle("Use model readiness targets", True, help="On uses historical team execution plus competition week. Off lets you enter measured current-robot values.")
    refresh = st.button("Refresh live data", use_container_width=True)

@st.cache_data(ttl=900, show_spinner=False)
def get_live(p, t, s, cache_version):
    return live_snapshot(p, t, s)

if refresh:
    get_live.clear()

if team.strip():
    with st.spinner("Checking live competition sources…"):
        live = get_live(program, team.strip(), season, "5.4.21")
else:
    live = {"profile": None, "manuals": {}, "sources": [], "warnings": ["Enter a team number to query live team data."]}

tranche_data = live.get("profile")
tranche = tranche_data.get("tranche") if tranche_data else None
trajectory = tranche_data.get("trajectory") if tranche_data else None

_READINESS={"T1":("Contested",92,96,90),"T2":("Integrated",88,94,85),"T3":("Integrated",82,92,78),"T4":("Reliable",72,88,68),"T5":("Reliable",58,82,55),"T6":("Exists",40,72,40)}
primary_gate,auto_reliability,robot_reliability,cpr=_READINESS.get(tranche,("Reliable",60,85,60))
week=max(1,min(8,event_week))
auto_reliability=min(99,auto_reliability+(week-1)*2)
robot_reliability=min(99,robot_reliability+(week-1))
cpr=min(96,cpr+(week-1)*2)
gates=["Exists","Reliable","Integrated","Contested","Optimized"]
advance=(1 if week>=4 else 0)+(1 if week>=7 else 0)
primary_gate=gates[min(4,gates.index(primary_gate)+advance)]
with st.sidebar:
    if auto_maturity:
        st.write(f"**Primary scoring readiness:** {primary_gate}")
        st.write(f"**Autonomous target:** ≥{auto_reliability}%")
        st.write(f"**Match reliability target:** ≥{robot_reliability}%")
        st.write(f"**Contested retention target:** ≥{cpr}%")
        st.caption("Readiness targets—not measurements of the current robot.")
    else:
        primary_gate=st.select_slider("Measured primary scoring capability",gates,value=primary_gate)
        auto_reliability=st.slider("Measured autonomous reliability (%)",0,100,auto_reliability,5)
        robot_reliability=st.slider("Measured match reliability (%)",0,100,robot_reliability,5)
        cpr=st.slider("Measured contested retention (%)",0,100,cpr,5)


team_name = live.get("team_name")
if team_name:
    st.markdown(f"### {program} {team.strip()} — {team_name}")
st.caption(f"{program} · {season} {game_name}")

if not tranche:
    st.error("Team history unavailable — the live competition sources did not provide enough prior-season information to create a reliable recommendation.")
    st.markdown("### Data diagnostics")
    if live.get("sources"):
        st.write("**Sources reached:** " + ", ".join(live["sources"]))
    else:
        st.write("**Sources reached:** none")
    if live.get("warnings"):
        for warning in live["warnings"]:
            st.warning(warning)
    else:
        st.warning("No team-history result was returned. Try Refresh live data. If this continues, one of the historical competition sources may be unavailable or may not contain prior-season results for this team.")
    st.info("Recommendations use only competition history available before the selected season. FRC uses Statbotics + The Blue Alliance; FTC uses FTCScout. When prior history is genuinely unavailable, the app will say so rather than inventing past performance.")
    st.stop()

tranche_note = f"Auto-classified from {tranche_data['source']} using only seasons before {season}."
result = recommend(program, season, team.strip(), event_week, tranche, trajectory, primary_gate, auto_reliability, robot_reliability, cpr)

c1,c2,c3 = st.columns(3)
c1.metric("Competition week", f"Week {event_week}", help="The selected competition week. Later weeks raise expected scoring throughput, autonomous maturity, reliability, and development readiness based on the team's historical execution.")
c2.metric("Reliability", f"{robot_reliability}%", help="How often the robot completes a full match without a major robot-caused problem. Example: 19 successful full matches out of 20 = 95%.")
c3.metric("CPR", f"{cpr}%", help="Contested Performance Retention: scoring under realistic defense/traffic divided by clean-practice scoring. Example: 80 points under pressure divided by 100 clean points = 80% CPR.")

features = robot_features(program, season, tranche)
targets = performance_targets(program, season, tranche, event_week)

st.subheader("Recommended robot specification")
st.caption(derivation_text(program, season, tranche))

m1, m2 = st.columns(2)
m1.metric("Target autonomous score", targets["auto"], help="Recommended autonomous contribution for this game, team history, and competition week. It is a planning target, not an official FIRST benchmark.")
m2.metric("Target teleop score", targets["teleop"], help="Recommended teleop contribution based on this game's scoring economics, the team's historical execution, and the selected competition week. Later weeks intentionally expect greater maturity.")
st.caption(targets.get("week_note",""))

st.markdown("### Recommended robot feature set")
f1, f2, f3 = st.columns(3)
with f1:
    st.markdown("#### Must Have")
    st.caption("Highest-priority capabilities for this team's expected execution level in the selected game.")
    for x in features["must"]:
        st.markdown(f"- **{x}**")
with f2:
    st.markdown("#### Should Have")
    st.caption("High-value capabilities to add as the core robot becomes reliable and integrated.")
    for x in features["should"]:
        st.markdown(f"- {x}")
with f3:
    st.markdown("#### Only If Mature")
    st.caption("Additional capabilities that become attractive when the core robot, autonomous routines, and driver practice are mature.")
    for x in features["optional"]:
        st.markdown(f"- {x}")

st.markdown("### Match-cycle targets")
st.write("**Scoring loop:** " + targets["cycles"])
st.write("**Throughput target:** " + targets["rate"])

st.markdown("### Recommended lower priorities")
st.caption("Capabilities to sequence later in the build unless testing shows they add more match value than the current priorities.")
for x in targets["avoid"]:
    st.info(x)

st.divider()
st.subheader("Team recommendations")
st.markdown(f"### {result['headline']}")
st.write(result["summary"])
l, r = st.columns(2)
with l:
    st.markdown("#### Highest-value work")
    for x in result["priorities"]:
        st.markdown(f"- {x}")
    st.info(result["maturity_action"])
with r:
    st.markdown("#### Lower-priority development")
    for x in result["avoid"]:
        st.markdown(f"- {x}")
    st.success(result["event_target"])

st.markdown("#### Development allocation", help="This chart tells the team how to divide its NEXT block of work. The bars are percentages and add to 100%. Reliability = 25 means spend about one quarter of the next work period finding and fixing robot failures. Autonomous = 25 means spend about one quarter on autonomous. It is a time/resource recommendation, NOT a robot score.")
st.bar_chart(result["allocation"], horizontal=True)

if worlds_plan:
    d = worlds_delta(result, tranche, trajectory, auto_reliability, robot_reliability, cpr)
    wf = worlds_feature_delta(program, season, tranche)
    st.divider()
    st.subheader("World Championship delta plan")
    st.write("Keep the first-event plan above. These are the additional deltas to peak again at Worlds.")
    a,b = st.columns(2)
    with a:
        st.markdown("#### Implement after Event 1")
        for x in d["deltas"]:
            st.markdown(f"- {x}")
    with b:
        st.markdown("#### Worlds targets")
        for x in d["targets"]:
            st.markdown(f"- {x}")
        st.warning(d["guardrail"])
    st.markdown("#### Robot feature deltas for Worlds")
    w1,w2 = st.columns(2)
    with w1:
        st.markdown("**Retain / protect**")
        for x in wf["retain"]:
            st.markdown(f"- {x}")
    with w2:
        st.markdown("**Add or upgrade after Event 1 evidence**")
        for x in wf["add_or_upgrade"]:
            st.markdown(f"- {x}")
    st.info(wf["do_not_sacrifice"])

st.divider()
st.subheader("Live source status")
a,b = st.columns(2)
with a:
    st.markdown("#### Official game/manual sources")
    for label,url in live.get("manuals", {}).items():
        st.markdown(f"- [{label}]({url})")
    if program == "FTC" and live.get("first_events"):
        st.markdown(f"- [FIRST FTC Event Results]({live['first_events']})")
with b:
    st.markdown("#### Competition data")
    for source in live.get("sources", []):
        st.markdown(f"- ✅ {source}")
    for warning in live.get("warnings", []):
        st.markdown(f"- ⚠️ {warning}")

with st.expander("API configuration"):
    st.write("Statbotics and FTCScout are queried directly without local API credentials. The Blue Alliance requires TBA_AUTH_KEY. VEX remains supported by the backend through RobotEvents but is not exposed in the current public UI. Missing optional sources degrade gracefully.")
