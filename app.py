import streamlit as st
import pandas as pd
import joblib

# ---------- Page ----------
st.set_page_config("IPL Win Predictor", "🏏", layout="wide")
st.title("🏏 IPL Win Probability Predictor")

# ---------- Load Model ----------
@st.cache_resource
def load_model():
    return joblib.load("pipe.pkl")

pipe = load_model()

# ---------- Data ----------
teams = [
    'Mumbai Indians','Chennai Super Kings','Royal Challengers Bengaluru',
    'Kolkata Knight Riders','Rajasthan Royals','Sunrisers Hyderabad',
    'Delhi Capitals','Punjab Kings','Gujarat Titans','Lucknow Super Giants'
]

cities = [
    'Bangalore','Chandigarh','Delhi','Mumbai','Kolkata','Jaipur',
    'Hyderabad','Chennai','Ahmedabad','Pune','Lucknow',
    'Guwahati','Mohali','Navi Mumbai'
]

# ---------- Match Setup ----------
c1, c2, c3 = st.columns(3)

# Batting team selection
batting = c1.selectbox("Batting Team", teams, key="batting_team")

# Bowling team selection (exclude selected batting team)
# If previous bowling selection is invalid, reset to first valid option
prev_bowling = st.session_state.get("bowling_team", None)
bowling_options = [team for team in teams if team != batting]
if prev_bowling not in bowling_options:
    st.session_state["bowling_team"] = bowling_options[0]

bowling = c2.selectbox(
    "Bowling Team",
    bowling_options,
    index=bowling_options.index(st.session_state["bowling_team"]),
    key="bowling_team"
)

# City selection
city = c3.selectbox("City", cities)

st.divider()

# ---------- Match Inputs ----------
c4, c5, c6, c7 = st.columns(4)
target = c4.number_input("Target", min_value=1)
score = c5.number_input("Score", min_value=0)
overs = c6.number_input("Overs (e.g. 15.3)", 0.0, 20.0, step=0.1, help="Enter overs as X.Y → X overs and Y balls")
wickets = c7.number_input("Wickets", 0, 10)

# ---------- Prediction ----------
if st.button("Predict", use_container_width=True):

    # ---------- Overs → balls conversion (Safe Parsing) ----------
    overs_split = str(overs).split('.')
    o = int(overs_split[0])
    b = int(overs_split[1]) if len(overs_split) > 1 else 0

    if b > 5:
        st.error("Invalid overs format (decimal must be 0–5)")
        st.stop()

    balls_bowled = o * 6 + b
    balls_left = max(120 - balls_bowled, 0)

    # ---------- Input validation ----------
    if score > target:
        st.error("Score cannot exceed target before match result!")
        st.stop()

    if wickets > 10 or wickets < 0:
        st.error("Wickets must be between 0 and 10!")
        st.stop()

    if score < 0 or target <= 0:
        st.error("Invalid score or target!")
        st.stop()

    if balls_bowled == 0 and score > 0:
        st.error("Score cannot exist without balls bowled!")
        st.stop()

    runs_left = max(target - score, 0)
    wkts_left = 10 - wickets

    # ---------- Real Match Result Checks ----------
    if score >= target:
        st.success(f"{batting} won the match! 🎉")
        st.stop()

    if wickets >= 10:
        st.error(f"{bowling} won! All wickets fallen.")
        st.stop()

    if balls_left == 0 and score < target:
        st.error(f"{bowling} defended successfully!")
        st.stop()

    if balls_left == 0 and score == target:
        st.info("The match is tied!")
        st.stop()

    # ---------- CRR and RRR ----------
    crr = (score * 6) / balls_bowled if balls_bowled > 0 else 0
    rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

    # ---------- DataFrame ----------
    df = pd.DataFrame({
        'batting_team':[batting],
        'bowling_team':[bowling],
        'city':[city],
        'runs_left':[runs_left],
        'balls_left':[balls_left],
        'wickets_left':[wkts_left],
        'target_runs':[target],
        'crr':[crr],
        'rrr':[rrr]
    })

    # ---------- Prediction ----------
    result = pipe.predict_proba(df)[0]
    win = round(result[1] * 100, 2)
    lose = round(result[0] * 100, 2)

    # ---------- Output ----------
    st.subheader("📊 Prediction Result")
    col1, col2 = st.columns(2)

    col1.metric(batting, f"{win}%")
    col1.progress(round(win,1)/100)

    col2.metric(bowling, f"{lose}%")
    col2.progress(round(lose,1)/100)

    # ---------- Match Situation ----------
    st.write(f"""
🏏 **Match Situation**

• Runs Needed: {runs_left}  
• Balls Left: {balls_left}  
• Wickets Left: {wkts_left}  
• Current Run Rate: {round(crr,2)}  
• Required Run Rate: {round(rrr,2)}  
""")

    if win > 75:
        st.success("🔥 Strong Winning Position")
        st.balloons()
    elif win > 55:
        st.info("⚡ Slight Advantage")
    elif win > 45:
        st.warning("🤝 Even Match")
    else:
        st.error("🔄 Tough Situation")

# ---------- Footer ----------
st.divider()
st.caption("Built with Streamlit • IPL Win Probability Model")