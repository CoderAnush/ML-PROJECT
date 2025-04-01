import streamlit as st
import numpy as np
import joblib

# Load trained XGBoost model
model = joblib.load("xgboost_model.pkl")

# Team and Venue Lists
teams = [
    "Delhi Daredevils", "Royal Challengers Bangalore", "Lucknow Super Giants",
    "Punjab Kings", "Deccan Chargers", "Chennai Super Kings", "Gujarat Titans",
    "Mumbai Indians", "Rajasthan Royals", "Kolkata Knight Riders",
    "Delhi Capitals", "Royal Challengers Bengaluru", "Sunrisers Hyderabad",
    "Kings XI Punjab"
]

venues = [
    "Ahmedabad", "Bangalore", "Chandigarh", "Chennai", "Delhi", "Dharamsala",
    "Hyderabad", "Indore", "Jaipur", "Kanpur", "Kochi", "Kolkata", "Lucknow",
    "Mohali", "Mumbai", "Nagpur", "Pune", "Raipur", "Rajkot", "Ranchi",
    "Thiruvananthapuram", "Visakhapatnam"
]

# Configure page
st.set_page_config(page_title="IPL Match Winner Predictor", layout="wide")

# Sidebar
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/6/6a/IPL_Logo.svg", width=150)
st.sidebar.title("Quick Access")

# Main Title
st.title("IPL Match Winner Predictor")
st.subheader("Predict the winner of an IPL match based on real-time match data.")

st.markdown("---")

# Columns for team selection
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox("Select Batting Team", teams)
with col2:
    bowling_team = st.selectbox("Select Bowling Team", teams)

# Venue selection
venue = st.selectbox("Select Venue", venues)

st.markdown("---")

# Match situation inputs
st.subheader("Match Conditions")

col3, col4 = st.columns(2)

with col3:
    target = st.number_input("Target Score", min_value=1, step=1)
    current_score = st.number_input("Current Score", min_value=0, step=1)
    
with col4:
    balls_left = st.number_input("Balls Left", min_value=1, max_value=300, step=1)
    wickets_down = st.number_input("Wickets Down", min_value=0, max_value=10, step=1)

st.markdown("---")

# Prediction button
if st.button("Predict Winner", use_container_width=True):
    # Prepare the input data
    input_data = np.array([[target, current_score, balls_left, wickets_down]])

    # Predict the probabilities for both classes (batting team wins or bowling team wins)
    proba = model.predict_proba(input_data)

    # Get the predicted class (0 or 1) and its confidence (probability)
    predicted_class = np.argmax(proba)  # 1 if batting team wins, 0 if bowling team wins
    confidence_score = proba[0][predicted_class] * 100  # Probability in percentage

    # Display the predicted winner and confidence score
    result = "Batting Team Wins" if predicted_class == 1 else "Bowling Team Wins"
    st.markdown(f"<h2 style='text-align: center; color: green;'>{result}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>Confidence: {confidence_score:.2f}%</h3>", unsafe_allow_html=True)

    # Match insights
    st.subheader("Match Insights")
    run_rate = round(current_score / ((300 - balls_left) / 6), 2) if balls_left < 300 else 0
    required_run_rate = round((target - current_score) / (balls_left / 6), 2) if balls_left > 0 else 0
    
    col5, col6 = st.columns(2)
    col5.metric(label="Current Run Rate", value=f"{run_rate} RPO")
    col6.metric(label="Required Run Rate", value=f"{required_run_rate} RPO")

st.markdown("---")
