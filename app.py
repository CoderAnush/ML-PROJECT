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

# Streamlit UI
st.title("🏏 Cricket Match Winner Predictor")

# Dropdowns for Batting and Bowling Teams
batting_team = st.selectbox("Select Batting Team", teams)
bowling_team = st.selectbox("Select Bowling Team", teams)

# Dropdown for Venue
venue = st.selectbox("Select Venue", venues)

# Numeric Inputs
target = st.number_input("Enter Target Score", min_value=1)
current_score = st.number_input("Enter Current Score", min_value=0)
balls_left = st.number_input("Enter Balls Left", min_value=1, max_value=300)
wickets_down = st.number_input("Enter Wickets Down", min_value=0, max_value=10)

# Predict Button
if st.button("Predict Winner"):
    input_data = np.array([[target, current_score, balls_left, wickets_down]])  # Modify based on actual model input features
    prediction = model.predict(input_data)
    
    # Display Prediction
    result = "Batting Team Wins" if prediction[0] == 1 else "Bowling Team Wins"
    st.success(f"🏆 Predicted Winner: **{result}**")
