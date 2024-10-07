import shutil

import pandas as pd
import mlflow
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import os
import argparse
import joblib

PROJECT_DIR = os.getenv('PROJECT_DIR')
os.chdir(PROJECT_DIR)

def read_data(train_path, test_path):
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    return train, test

def encode_data(df, columns_to_encode, fit=True):
    encoders_base_dir = "models/encoder"
    if fit:
        for i, column in enumerate(columns_to_encode):
            labelencoder = LabelEncoder()
            df[column] = labelencoder.fit_transform(df[column])
            encoder_dir = f'{encoders_base_dir}{i}.pkl'
            joblib.dump(labelencoder, encoder_dir)
    else:
        for i, column in enumerate(columns_to_encode):
            labelencoder = joblib.load(f'{encoders_base_dir}{i}.pkl')
            df[column] = labelencoder.transform(df[column])
    return df

def scale_data(train, test):
    scaler_dir = "models/scaler.pkl"

    scaler = MinMaxScaler()
    X_train, y_train = train.drop('Exam_Score', axis=1), train['Exam_Score']
    X_test, y_test = test.drop('Exam_Score', axis=1), test['Exam_Score']
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    joblib.dump(scaler, scaler_dir)

    return X_train, y_train, X_test, y_test

def fit_model(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def predict_model(model, X_test):
    return model.predict(X_test)


def save_model(model, mse):
    model_dir = "models/linear_regression_model.pkl"

    if os.path.exists(model_dir):
        shutil.rmtree(model_dir)

    with mlflow.start_run():
        mlflow.log_metric("mse", mse)
        mlflow.sklearn.log_model(model, "models/linear_regression_model")

        os.makedirs("models", exist_ok=True)
        mlflow.sklearn.save_model(model, model_dir)

def main(step):
    if step == 'read':
        train, test = read_data('data/processed/train.csv', 'data/processed/test.csv')
        pd.to_pickle(train, 'data/temp/train.pkl')
        pd.to_pickle(test, 'data/temp/test.pkl')

    elif step == 'encode':
        train = pd.read_pickle('data/temp/train.pkl')
        test = pd.read_pickle('data/temp/test.pkl')
        columns_to_encode = ['Parental_Involvement', 'Access_to_Resources', 'Extracurricular_Activities', 'Motivation_Level',
                             'Internet_Access', 'Family_Income', 'Teacher_Quality', 'School_Type', 'Peer_Influence',
                             'Learning_Disabilities', 'Parental_Education_Level', 'Distance_from_Home', 'Gender']
        train = encode_data(train, columns_to_encode, fit=True)
        test = encode_data(test, columns_to_encode, fit=False)
        pd.to_pickle(train, 'data/temp/train_encoded.pkl')
        pd.to_pickle(test, 'data/temp/test_encoded.pkl')

    elif step == 'scale':
        train = pd.read_pickle('data/temp/train_encoded.pkl')
        test = pd.read_pickle('data/temp/test_encoded.pkl')
        X_train, y_train, X_test, y_test = scale_data(train, test)
        pd.to_pickle((X_train, y_train, X_test, y_test), 'data/temp/scaled_data.pkl')

    elif step == 'fit':
        X_train, y_train, _, _ = pd.read_pickle('data/temp/scaled_data.pkl')
        model = fit_model(X_train, y_train)
        pd.to_pickle(model, 'data/temp/model.pkl')

    elif step == 'predict':
        model = pd.read_pickle('data/temp/model.pkl')
        _, _, X_test, y_test = pd.read_pickle('data/temp/scaled_data.pkl')
        y_pred = predict_model(model, X_test)
        mse = mean_squared_error(y_test, y_pred)
        pd.to_pickle(mse, 'data/temp/mse.pkl')

    elif step == 'save':
        model = pd.read_pickle('data/temp/model.pkl')
        mse = pd.read_pickle('data/temp/mse.pkl')
        save_model(model, mse)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--step', type=str, required=True)
    args = parser.parse_args()

    main(args.step)
