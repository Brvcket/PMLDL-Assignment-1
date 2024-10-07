import pandas as pd
import mlflow
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import os

train = pd.read_csv('data/processed/train.csv')
test = pd.read_csv('data/processed/test.csv')

columns_to_encode = ['Parental_Involvement', 'Access_to_Resources', 'Extracurricular_Activities', 'Motivation_Level',
                     'Internet_Access', 'Family_Income', 'Teacher_Quality', 'School_Type', 'Peer_Influence',
                     'Learning_Disabilities', 'Parental_Education_Level', 'Distance_from_Home', 'Gender']

labelencoder = LabelEncoder()
for column in columns_to_encode:
    train[column] = labelencoder.fit_transform(train[column])
    test[column] = labelencoder.transform(test[column])

scaler = MinMaxScaler()
X_train, y_train = train.drop('Exam_Score', axis=1), train['Exam_Score']
X_test, y_test = test.drop('Exam_Score', axis=1), test['Exam_Score']
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

with mlflow.start_run():
    mlflow.log_metric("mse", mse)

    model_path = "models/linear_regression_model"
    mlflow.sklearn.log_model(model, model_path)

    os.makedirs("models", exist_ok=True)
    mlflow.sklearn.save_model(model, "models/linear_regression_model.pkl")
