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
    'deployment_pipeline',
    default_args=default_args,
    schedule_interval=None,
    start_date=start_date,
    catchup=False,
)

task1 = BashOperator(
    task_id='docker_compose_build_and_up',
    bash_command='docker compose -f docker-compose.yaml up --build -d',
    dag=dag,
    cwd=f'{PROJECT_DIR}/code/deployment'
)

task1