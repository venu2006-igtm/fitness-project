import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Smart Fitness Coaching Agent",
    page_icon="🏋️",
    layout="wide"
)

st.title("🏋️ Smart Fitness Coaching Agent")
st.write("Identify exercises, track workouts, and get fitness recommendations.")

# -----------------------------
# Load Model Files
# -----------------------------
if not os.path.exists("fitness_model.pkl"):
    st.error("fitness_model.pkl not found.")
    st.stop()

if not os.path.exists("label_encoder.pkl"):
    st.error("label_encoder.pkl not found.")
    st.stop()

model = joblib.load("fitness_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("User Information")

name = st.sidebar.text_input("Name")

age = st.sidebar.number_input(
    "Age",
    min_value=10,
    max_value=100,
    value=20
)

weight = st.sidebar.number_input(
    "Weight (kg)",
    min_value=20.0,
    max_value=200.0,
    value=60.0
)

height = st.sidebar.number_input(
    "Height (cm)",
    min_value=100.0,
    max_value=250.0,
    value=170.0
)

# -----------------------------
# Exercise Inputs
# -----------------------------
st.header("Enter Exercise Details")

desc = st.text_input("Description")
exercise_type = st.text_input("Type")
body_part = st.text_input("Body Part")
equipment = st.text_input("Equipment")

level = st.selectbox(
    "Level",
    ["Beginner", "Intermediate", "Expert"]
)

rating = st.slider(
    "Rating",
    0.0,
    5.0,
    4.0
)

rating_desc = st.text_input("Rating Description")

duration = st.number_input(
    "Workout Duration (minutes)",
    min_value=1,
    max_value=300,
    value=30
)

# -----------------------------
# Prediction
# -----------------------------
if st.button("Identify Exercise"):

    try:
        # Convert text to simple numeric values
        data = pd.DataFrame({
            "Desc": [hash(desc) % 1000],
            "Type": [hash(exercise_type) % 100],
            "BodyPart": [hash(body_part) % 100],
            "Equipment": [hash(equipment) % 100],
            "Level": [hash(level) % 10],
            "Rating": [rating],
            "RatingDesc": [hash(rating_desc) % 100]
        })

        prediction = model.predict(data)

        exercise = label_encoder.inverse_transform(
            prediction.astype(int)
        )[0]

        st.success(f"Predicted Exercise: {exercise}")

        # Calories
        calories = duration * 5

        st.info(
            f"Estimated Calories Burned: {calories} kcal"
        )

        # Save history
        history = pd.DataFrame([{
            "Date": datetime.now(),
            "Name": name,
            "Exercise": exercise,
            "Duration": duration,
            "Calories": calories
        }])

        if os.path.exists("workout_history.csv"):
            history.to_csv(
                "workout_history.csv",
                mode="a",
                header=False,
                index=False
            )
        else:
            history.to_csv(
                "workout_history.csv",
                index=False
            )

    except Exception as e:
        st.error(f"Prediction Error: {e}")

# -----------------------------
# Workout History
# -----------------------------
st.header("Workout History")

if os.path.exists("workout_history.csv"):

    history = pd.read_csv(
        "megaGymDataset.csv"
    )

    st.dataframe(history)

# -----------------------------
# BMI Calculator
# -----------------------------
st.header("BMI Calculator")

height_m = height / 100

bmi = weight / (height_m ** 2)

st.write(f"Your BMI: {round(bmi,2)}")

# -----------------------------
# Recommendations
# -----------------------------
st.header("Personalized Recommendations")

if bmi < 18.5:
    st.info(
        "You are underweight. Include nutritious food and strength training."
    )

elif bmi < 25:
    st.success(
        "You have a healthy weight. Maintain your current routine."
    )

elif bmi < 30:
    st.warning(
        "You are overweight. Add more cardio and reduce calorie intake."
    )

else:
    st.error(
        "Obesity detected. Increase physical activity and consult a fitness expert."
    )

if duration < 30:
    st.warning(
        "Try exercising for at least 30 minutes every day."
    )
else:
    st.success(
        "Excellent workout duration!"
    )