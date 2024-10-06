from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os

# PROJECT_DIR = os.getenv('PROJECT_DIR')
PROJECT_DIR = '/mnt/c/Users/ahmat/PycharmProjects/PMLDL-Assignment-1'
os.chdir(PROJECT_DIR)

os.system('pip install pandas')

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('data_engineering_pipeline', default_args=default_args, schedule_interval='*/5 * * * *', start_date=datetime(2024, 10, 6))

task1 = BashOperator(
    task_id='process_data',
    bash_command='python scripts/data_processing.py',
    dag=dag,
    cwd=PROJECT_DIR
)
