from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os
import pendulum

PROJECT_DIR = '/mnt/c/Users/ahmat/PycharmProjects/PMLDL-Assignment-1'
os.chdir(PROJECT_DIR)

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

start_date = pendulum.now(tz="Europe/Moscow").subtract(minutes=5)
start_date = start_date.replace(second=0, microsecond=0)

dag = DAG('model_training_pipeline', default_args=default_args, schedule_interval=timedelta(minutes=5),
          start_date=start_date)

task1 = BashOperator(
    task_id='read_data',
    bash_command='python scripts/train_model.py --step read',
    dag=dag,
    cwd=PROJECT_DIR
)

task2 = BashOperator(
    task_id='encode_data',
    bash_command='python scripts/train_model.py --step encode',
    dag=dag,
    cwd=PROJECT_DIR
)

task3 = BashOperator(
    task_id='scale_data',
    bash_command='python scripts/train_model.py --step scale',
    dag=dag,
    cwd=PROJECT_DIR
)

task4 = BashOperator(
    task_id='model_fit',
    bash_command='python scripts/train_model.py --step fit',
    dag=dag,
    cwd=PROJECT_DIR
)

task5 = BashOperator(
    task_id='model_predict',
    bash_command='python scripts/train_model.py --step predict',
    dag=dag,
    cwd=PROJECT_DIR
)

task6 = BashOperator(
    task_id='save_model',
    bash_command='python scripts/train_model.py --step save',
    dag=dag,
    cwd=PROJECT_DIR
)

task1 >> task2 >> task3 >> task4 >> task5 >> task6
