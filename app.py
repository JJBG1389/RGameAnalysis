import streamlit as st
from recommendation_engine import recommend, worlds_delta, robot_features, worlds_feature_delta, performance_targets, derivation_text, TRANCHE_LABELS, TRAJECTORIES, TRANCHE_SHARES
from data_sources import live_snapshot

st.set_page_config(page_title="RGameAnalysis Team Advisor", page_icon="🤖", layout="wide")
st.title("RGameAnalysis Team Advisor")
st.caption("Model 5.3 · Deploy 2026.10.04.5 · live source adapters · tranche-aware first-event + Worlds planning")

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

TRANCHE_HELP = """
**Team tranche** is Model 5.3's estimate of a team's demonstrated execution capacity entering the selected season.
It is not a permanent ranking or a judgment of the students. The model uses the tranche to recommend an
appropriate level of design risk, complexity, schedule, autonomous development, and practice.

- **T1 — Championship Elite:** consistent championship-level execution; can pursue marginal advantages and higher design risk.
- **T2 — Championship Contender:** regular event-winning/top-alliance performance with credible championship upside.
- **T3 — Regional Contender:** regular playoff/first-pick caliber; occasional event winner.
- **T4 — Emerging Competitor:** playoff-capable and improving, but qualification performance or execution is still inconsistent.
- **T5 — Developing:** sporadic playoff success with meaningful reliability/capability gaps.
- **T6 — Foundation:** rookie/rebuilding or establishing the fundamentals of a reliable competition robot.

The arrow shows trajectory: **↑ Rising**, **→ Stable**, **↓ Declining**. Tranches should be calculated using
information available *before* the selected season so the recommendation does not use hindsight.
"""

with st.sidebar:
    st.header("Team & game")
    program = st.selectbox("Program", ["FRC", "FTC", "VEX"])
    game_labels = [f"{year} — {name}" for year, name in GAME_OPTIONS[program].items()]
    selected_game = st.selectbox("Game / season", game_labels)
    season = int(selected_game.split(" — ", 1)[0])
    game_name = GAME_OPTIONS[program][season]
    team = st.text_input("Team number", "6964" if program == "FRC" else "")
    event_week = st.slider("First event competition week", 1, 8, 1)
    worlds_plan = st.toggle("Team plans to attend World Championship", False, help="Turn this on if the team expects to keep developing for World Championship-level play. The tool gives a first-event plan plus a later list of improvements for Worlds. It does not assume the team should rebuild the robot.")

    st.divider()
    st.subheader("Current maturity")
    primary_gate = st.select_slider("Primary scoring capability", ["Exists","Reliable","Integrated","Contested","Optimized"], value="Integrated", help="How mature is the robot’s MAIN scoring system? Exists = worked once. Reliable = works repeatedly. Integrated = works on the complete robot. Contested = still works with defense, traffic, or imperfect game pieces. Optimized = all of those are true and the team is making it faster. Pick what the robot can prove today, not what you hope it will do.")
    auto_reliability = st.slider("Autonomous reliability (%)", 0, 100, 80, 5, help="How often the FULL autonomous routine works correctly from start to finish. Example: 18 successful runs out of 20 = 90%. A run fails if the robot misses an important action, loses localization, jams, hits something it should not, or does not finish the planned routine.")
    robot_reliability = st.slider("Match reliability (%)", 0, 100, 90, 5, help="How often the robot completes a full match without a major robot problem. Example: 19 good full matches out of 20 = 95%. Count broken mechanisms, electrical problems, software crashes, disconnects, and serious jams. Normal driver misses do not count.")
    cpr = st.slider("Contested performance retention (%)", 0, 100, 75, 5, help="How much normal scoring the robot keeps when the match gets difficult. Compare average scoring in clean practice with scoring under defense, traffic, blocked paths, bad game-piece positions, or partner interference. Example: 80 points under pressure divided by 100 clean points = 80% CPR.")
    refresh = st.button("Refresh live data", use_container_width=True)

@st.cache_data(ttl=900, show_spinner=False)
def get_live(p, t, s):
    return live_snapshot(p, t, s)

if refresh:
    get_live.clear()

if team.strip():
    with st.spinner("Checking live competition sources…"):
        live = get_live(program, team.strip(), season)
else:
    live = {"profile": None, "manuals": {}, "sources": [], "warnings": ["Enter a team number to query live team data."]}

tranche_data = live.get("profile")
tranche = tranche_data.get("tranche") if tranche_data else None
trajectory = tranche_data.get("trajectory") if tranche_data else None

st.caption(f"{program} · {season} {game_name}")

if not tranche:
    st.error("Tranche unavailable — the live historical data did not provide enough information to classify this team. No robot recommendation will be generated from a guessed default.")
    st.markdown("### Data diagnostics")
    if live.get("sources"):
        st.write("**Sources reached:** " + ", ".join(live["sources"]))
    else:
        st.write("**Sources reached:** none")
    if live.get("warnings"):
        for warning in live["warnings"]:
            st.warning(warning)
    else:
        st.warning("No classifier result was returned. Try Refresh live data. If this continues, the historical API response needs to be inspected.")
    st.info("For FRC, automatic tranche classification requires usable pre-season Statbotics and/or The Blue Alliance history. The app will no longer silently assign T4 when that data is missing.")
    st.stop()

tranche_note = f"Auto-classified from {tranche_data['source']} using only seasons before {season}."
result = recommend(program, season, team.strip(), event_week, tranche, trajectory, primary_gate, auto_reliability, robot_reliability, cpr)

c1,c2,c3,c4 = st.columns(4)
c1.metric("Team tranche", f"{result['tranche']} {result['trajectory_symbol']}", help="Calculated from earlier seasons. For FRC, Model 5.3 combines Statbotics EPA strength with The Blue Alliance qualification, alliance-selection, and playoff results. It does not use results from the selected season.")
c2.metric("First-event stage", "Event 1", help="The team is preparing for its first competition. Focus on reliability, autonomous routines, full-match practice, quick pit repairs, and reducing mistakes.")
c3.metric("Reliability", f"{robot_reliability}%", help="How often the robot completes a full match without a major robot-caused problem. Example: 19 successful full matches out of 20 = 95%.")
c4.metric("CPR", f"{cpr}%", help="Contested Performance Retention: scoring under realistic defense/traffic divided by clean-practice scoring. Example: 80 points under pressure divided by 100 clean points = 80% CPR.")
st.caption(tranche_note)

with st.expander("Why was this tranche assigned?"):
    st.write("For FRC, the automatic tranche combines historical Statbotics EPA strength with The Blue Alliance event execution from seasons BEFORE the selected game. Statbotics EPA strength is weighted 75%; TBA qualification ranking, alliance selection, and playoff results are weighted 25%.")
    if tranche_data.get("composite") is not None:
        st.metric("Composite TEC score", f"{tranche_data['composite']:.1f}/100")
    if tranche_data.get("statbotics_score") is not None:
        st.write(f"**Statbotics strength:** {tranche_data['statbotics_score']:.1f}/100")
    if tranche_data.get("tba_score") is not None:
        st.write(f"**TBA event execution:** {tranche_data['tba_score']:.1f}/100")
    for item in tranche_data.get("evidence", []):
        st.markdown(f"- {item}")
    st.caption("TEC bands: T1 >=85; T2 75 to <85; T3 63 to <75; T4 48 to <63; T5 32 to <48; T6 <32.")

features = robot_features(program, season, tranche)
targets = performance_targets(program, season, tranche)

st.subheader("Recommended robot specification")
st.caption(derivation_text(program, season, tranche))

m1, m2 = st.columns(2)
m1.metric("Target autonomous score", targets["auto"], help="Model target derived from game scoring economics, autonomous leverage, team tranche, and historical season-to-championship compression. Not an official benchmark.")
m2.metric("Target teleop score", targets["teleop"], help="Model target derived from sustainable scoring throughput, team tranche, and historical progression. Not an official benchmark.")

st.markdown("### Recommended robot feature set")
f1, f2, f3 = st.columns(3)
with f1:
    st.markdown("#### Must Have")
    st.caption("Core features to protect first.")
    for x in features["must"]:
        st.markdown(f"- **{x}**")
with f2:
    st.markdown("#### Should Have")
    st.caption("Add after core capabilities are reliable and integrated.")
    for x in features["should"]:
        st.markdown(f"- {x}")
with f3:
    st.markdown("#### Only If Mature")
    st.caption("Do not let these delay autonomous, reliability, or driver practice.")
    for x in features["optional"]:
        st.markdown(f"- {x}")

st.markdown("### Match-cycle targets")
st.write("**Scoring loop:** " + targets["cycles"])
st.write("**Throughput target:** " + targets["rate"])

st.markdown("### Do Not Pursue")
st.caption("Game aspects that should not consume meaningful design/build time for this tranche unless new evidence changes the trade.")
for x in targets["avoid"]:
    st.error(x)

st.divider()
st.subheader("Team execution recommendations")
st.markdown(f"### {result['headline']}")
st.write(result["summary"])
l, r = st.columns(2)
with l:
    st.markdown("#### Highest-value work")
    for x in result["priorities"]:
        st.markdown(f"- {x}")
    st.info(result["maturity_action"])
with r:
    st.markdown("#### Do less of")
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
    st.write("Statbotics and FTCScout are queried directly. The Blue Alliance requires TBA_AUTH_KEY. RobotEvents requires ROBOTEVENTS_TOKEN. Missing credentialed sources degrade gracefully.")
