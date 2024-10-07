from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import pendulum
import os

PROJECT_DIR = '/mnt/c/Users/ahmat/PycharmProjects/PMLDL-Assignment-1'
os.chdir(PROJECT_DIR)

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

start_date = pendulum.now(tz="Europe/Moscow").subtract(minutes=5)
start_date = start_date.replace(second=0, microsecond=0)

dag = DAG(
    'data_engineering_pipeline',
    default_args=default_args,
    schedule_interval=None,
    start_date=start_date,
    catchup=False,
)

task1 = BashOperator(
    task_id='read_data',
    bash_command='python scripts/data_processing.py --step read',
    dag=dag,
    cwd=PROJECT_DIR
)

task2 = BashOperator(
    task_id='process_data',
    bash_command='python scripts/data_processing.py --step process',
    dag=dag,
    cwd=PROJECT_DIR
)

task3 = BashOperator(
    task_id='split_data',
    bash_command='python scripts/data_processing.py --step split',
    dag=dag,
    cwd=PROJECT_DIR
)

task4 = BashOperator(
    task_id='save_data',
    bash_command='python scripts/data_processing.py --step save',
    dag=dag,
    cwd=PROJECT_DIR
)

task1 >> task2 >> task3 >> task4
