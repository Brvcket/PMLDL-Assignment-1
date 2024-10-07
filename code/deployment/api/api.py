from fastapi import FastAPI
import joblib
import os
import mlflow
import pandas as pd
from pydantic import BaseModel

# PROJECT_DIR = '/mnt/c/Users/ahmat/PycharmProjects/PMLDL-Assignment-1'
PROJECT_DIR = os.getenv('PROJECT_DIR')
os.chdir(PROJECT_DIR)

model_dir = 'models/linear_regression_model.pkl'
model = mlflow.pyfunc.load_model(model_dir)

scaler_dir = "models/scaler.pkl"
scaler = joblib.load(scaler_dir)

encoders_base_dir = "models/encoder"

app = FastAPI()

class Features(BaseModel):
    Attendance: float
    Previous_Scores: float
    Sleep_Hours: float
    Hours_Studied: float
    Physical_Activity: float
    Tutoring_Sessions: float
    Parental_Involvement: str
    Access_to_Resources: str
    Extracurricular_Activities: str
    Motivation_Level: str
    Internet_Access: str
    Family_Income: str
    Teacher_Quality: str
    School_Type: str
    Peer_Influence: str
    Learning_Disabilities: str
    Parental_Education_Level: str
    Distance_from_Home: str
    Gender: str


@app.post("/predict")
def predict(features: Features):

    df = pd.DataFrame([features.dict()])

    column_order = [
        "Hours_Studied", "Attendance", "Parental_Involvement", "Access_to_Resources",
        "Extracurricular_Activities", "Sleep_Hours", "Previous_Scores", "Motivation_Level",
        "Internet_Access", "Tutoring_Sessions", "Family_Income", "Teacher_Quality",
        "School_Type", "Peer_Influence", "Physical_Activity", "Learning_Disabilities",
        "Parental_Education_Level", "Distance_from_Home", "Gender"
    ]

    df = df[column_order]

    df['Attendance'] = df['Attendance'].clip(0, 100)
    df['Previous_Scores'] = df['Previous_Scores'].clip(0, 100)
    df['Sleep_Hours'] = df['Sleep_Hours'].clip(0, 24)
    df['Hours_Studied'] = df['Hours_Studied'].clip(0, 168)
    df['Physical_Activity'] = df['Physical_Activity'].clip(0, 168)
    df['Tutoring_Sessions'] = df['Tutoring_Sessions'].clip(0, 168)

    df = df.fillna('most_frequent')

    columns_to_encode = ['Parental_Involvement', 'Access_to_Resources', 'Extracurricular_Activities',
                         'Motivation_Level', 'Internet_Access', 'Family_Income',
                         'Teacher_Quality', 'School_Type', 'Peer_Influence',
                         'Learning_Disabilities', 'Parental_Education_Level', 'Distance_from_Home', 'Gender']

    print(df)

    print('Encoding...')
    for i, column in enumerate(columns_to_encode):
        labelencoder = joblib.load(f'{encoders_base_dir}{i}.pkl')
        df[column] = labelencoder.fit_transform(df[column])

    print(df)

    print('Scaling...')
    scaled_data = scaler.transform(df)

    print(scaled_data)

    print('Predicting...')
    prediction = model.predict(scaled_data)

    return {"prediction": prediction[0]}
