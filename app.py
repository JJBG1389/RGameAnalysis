import streamlit as st
from recommendation_engine import recommend, TRANCHE_LABELS, TRAJECTORIES

st.set_page_config(page_title="RGameAnalysis Team Advisor", page_icon="🤖", layout="wide")

st.title("RGameAnalysis Team Advisor")
st.caption("Model 5.3 · Game × Team Tranche × Season Stage × Trajectory")

with st.sidebar:
    st.header("Team & season")
    program = st.selectbox("Program", ["FRC", "FTC", "VEX"])
    season = st.number_input("Season", min_value=2010, max_value=2035, value=2027, step=1)
    team = st.text_input("Team number", value="6964")
    event_week = st.slider("Next competition week", 1, 8, 1)

    st.divider()
    st.subheader("Team Execution Capacity")
    auto_profile = program == "FRC" and team.strip() == "6964"
    if auto_profile:
        st.info("Known demo profile: FRC 6964 is provisionally T4 ↑ based on the current Model 5.3 working classification.")
        tranche = "T4"
        trajectory = "Rising"
    else:
        st.caption("Until live data adapters are added, select a provisional team profile.")
        tranche = st.selectbox("Team tranche", list(TRANCHE_LABELS))
        trajectory = st.selectbox("Trajectory", TRAJECTORIES)

    st.divider()
    st.subheader("Current maturity")
    primary_gate = st.select_slider(
        "Primary scoring capability",
        options=["Exists", "Reliable", "Integrated", "Contested", "Optimized"],
        value="Integrated",
    )
    auto_reliability = st.slider("Autonomous reliability (%)", 0, 100, 80, 5)
    robot_reliability = st.slider("Match reliability (%)", 0, 100, 90, 5)
    cpr = st.slider("Contested performance retention (%)", 0, 100, 75, 5)

    generate = st.button("Generate recommendation", type="primary", use_container_width=True)

inputs = dict(
    program=program,
    season=int(season),
    team=team.strip(),
    event_week=event_week,
    tranche=tranche,
    trajectory=trajectory,
    primary_gate=primary_gate,
    auto_reliability=auto_reliability,
    robot_reliability=robot_reliability,
    cpr=cpr,
)

result = recommend(**inputs)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Team profile", f"{result['tranche']} {result['trajectory_symbol']}")
c2.metric("Season stage", result["stage_code"])
c3.metric("Reliability", f"{robot_reliability}%")
c4.metric("CPR", f"{cpr}%")

st.subheader(result["headline"])
st.write(result["summary"])

left, right = st.columns(2)
with left:
    st.markdown("### Highest-value work")
    for item in result["priorities"]:
        st.markdown(f"- {item}")

    st.markdown("### Maturity gate")
    st.info(result["maturity_action"])

with right:
    st.markdown("### Do less of")
    for item in result["avoid"]:
        st.markdown(f"- {item}")

    st.markdown("### Event objective")
    st.success(result["event_target"])

st.markdown("### Development allocation")
allocation = result["allocation"]
st.bar_chart(allocation, horizontal=True)

st.markdown("### Why the model chose this")
st.write(result["rationale"])

with st.expander("Model assumptions / limitations"):
    st.write(
        "This V1 runs the Model 5.3 tranche, maturity, reliability, CPR, and season-stage logic locally. "
        "It does not yet fetch live TBA, Statbotics, FTCScout, or RobotEvents data, so teams other than "
        "the included 6964 demo profile require a provisional manual tranche. Percentages shown by the "
        "app are user inputs, not inferred measurements."
    )
