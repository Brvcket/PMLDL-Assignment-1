import pandas as pd
from sklearn.model_selection import train_test_split
import os
import argparse

PROJECT_DIR = os.getenv('PROJECT_DIR')
os.chdir(PROJECT_DIR)

def read_data(file_path):
    return pd.read_csv(file_path)

def process_data(df):
    df['Attendance'] = df['Attendance'].clip(0, 100)
    df['Exam_Score'] = df['Exam_Score'].clip(0, 100)
    df['Previous_Scores'] = df['Previous_Scores'].clip(0, 100)
    df['Sleep_Hours'] = df['Sleep_Hours'].clip(0, 24)
    df['Hours_Studied'] = df['Hours_Studied'].clip(0, 168)
    df['Physical_Activity'] = df['Physical_Activity'].clip(0, 168)
    df['Tutoring_Sessions'] = df['Tutoring_Sessions'].clip(0, 168)
    df.fillna('most_frequent', inplace=True)
    return df

def split_data(df):
    return train_test_split(df, test_size=0.2, random_state=42)

def save_data(train, test, train_path, test_path):
    train.to_csv(train_path, index=False)
    test.to_csv(test_path, index=False)

def main(step):
    if step == 'read':
        df = read_data('data/raw/StudentPerformanceFactors.csv')
        df.to_pickle('data/temp/df.pkl')

    elif step == 'process':
        df = pd.read_pickle('data/temp/df.pkl')
        df = process_data(df)
        df.to_pickle('data/temp/df_processed.pkl')

    elif step == 'split':
        df = pd.read_pickle('data/temp/df_processed.pkl')
        train, test = split_data(df)
        pd.to_pickle(train, 'data/temp/train.pkl')
        pd.to_pickle(test, 'data/temp/test.pkl')

    elif step == 'save':
        train = pd.read_pickle('data/temp/train.pkl')
        test = pd.read_pickle('data/temp/test.pkl')
        save_data(train, test, 'data/processed/train.csv', 'data/processed/test.csv')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--step', type=str, required=True)
    args = parser.parse_args()

    main(args.step)
