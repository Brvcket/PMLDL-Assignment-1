from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os

PROJECT_DIR = '/mnt/c/Users/ahmat/PycharmProjects/PMLDL-Assignment-1'
os.chdir(PROJECT_DIR)

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('model_training_pipeline', default_args=default_args, schedule_interval='*/5 * * * *', start_date=datetime(2024, 10, 6))

task1 = BashOperator(
    task_id='train_model',
    bash_command='python scripts/train_model.py',
    dag=dag,
    cwd=PROJECT_DIR
)
