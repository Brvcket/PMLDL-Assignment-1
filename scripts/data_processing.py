import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
import os

PROJECT_DIR = '/mnt/c/Users/ahmat/PycharmProjects/PMLDL-Assignment-1'
os.chdir(PROJECT_DIR)

df = pd.read_csv('data/raw/StudentPerformanceFactors.csv')

df['Attendance'] = df['Attendance'].clip(0, 100)
df['Exam_Score'] = df['Exam_Score'].clip(0, 100)
df['Previous_Scores'] = df['Previous_Scores'].clip(0, 100)
df['Sleep_Hours'] = df['Sleep_Hours'].clip(0, 24)
df['Hours_Studied'] = df['Hours_Studied'].clip(0, 168)
df['Physical_Activity'] = df['Physical_Activity'].clip(0, 168)

df.fillna('most_frequent', inplace=True)

train, test = train_test_split(df, test_size=0.2, random_state=42)

train.to_csv('data/processed/train.csv', index=False)
test.to_csv('data/processed/test.csv', index=False)
