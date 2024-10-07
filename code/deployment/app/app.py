import streamlit as st
import requests

st.title("Student Performance Predictor")

FASTAPI_URL = "http://api:8000/predict"

hours_studied = st.number_input('Hours Studied', min_value=0, max_value=168)
attendance = st.number_input('Attendance', min_value=0, max_value=100)
parental_involvement = st.selectbox('Parental Involvement', ['Low', 'Medium', 'High'])
access_to_resources = st.selectbox('Access to Resources', ['Low', 'Medium', 'High'])
extracurricular_activities = st.selectbox('Extracurricular Activities', ['No', 'Yes'])
sleep_hours = st.number_input('Sleep Hours', min_value=0, max_value=24)
previous_scores = st.number_input('Previous Scores', min_value=0, max_value=100)
motivation_level = st.selectbox('Motivation Level', ['Low', 'Medium', 'High'])
internet_access = st.selectbox('Internet Access', ['No', 'Yes'])
tutoring_sessions = st.number_input('Tutoring Sessions', min_value=0, max_value=168)
family_income = st.selectbox('Family Income', ['Low', 'Medium', 'High'])
teacher_quality = st.selectbox('Teacher Quality', ['Low', 'Medium', 'High'])
school_type = st.selectbox('School Type', ['Public', 'Private'])
peer_influence = st.selectbox('Peer Influence', ['Negative', 'Neutral', 'Positive'])
physical_activity = st.number_input('Physical Activity', min_value=0, max_value=168)
learning_disabilities = st.selectbox('Learning Disabilities', ['Yes', 'No'])
parental_education_level = st.selectbox('Parental Education Level', ['College', 'Postgraduate', 'High School'])
distance_from_home = st.selectbox('Distance from Home', ['Near', 'Moderate', 'Far'])
gender = st.selectbox('Gender', ['Male', 'Female'])


if st.button('Predict'):
    features = {
        "Hours_Studied": hours_studied,
        "Attendance": attendance,
        "Parental_Involvement": parental_involvement,
        "Access_to_Resources": access_to_resources,
        "Extracurricular_Activities": extracurricular_activities,
        "Sleep_Hours": sleep_hours,
        "Previous_Scores": previous_scores,
        "Motivation_Level": motivation_level,
        "Internet_Access": internet_access,
        "Tutoring_Sessions": tutoring_sessions,
        "Family_Income": family_income,
        "Teacher_Quality": teacher_quality,
        "School_Type": school_type,
        "Peer_Influence": peer_influence,
        "Physical_Activity": physical_activity,
        "Learning_Disabilities": learning_disabilities,
        "Parental_Education_Level": parental_education_level,
        "Distance_from_Home": distance_from_home,
        "Gender": gender,
    }

    response = requests.post(FASTAPI_URL, json=features)
    st.write(f"Predicted Exam Score: {response.json()['prediction']}")
