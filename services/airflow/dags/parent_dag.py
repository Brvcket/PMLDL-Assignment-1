from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
import pendulum
from airflow.utils.trigger_rule import TriggerRule

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

start_date = pendulum.now(tz="Europe/Moscow").subtract(minutes=5)
start_date = start_date.replace(second=0, microsecond=0)

dag = DAG(
    'trigger_dags',
    default_args=default_args,
    schedule_interval=timedelta(minutes=5),
    start_date=start_date,
    catchup=False,
)

trigger_data_pipeline = TriggerDagRunOperator(
    task_id='trigger_data_engineering_pipeline',
    trigger_dag_id='data_engineering_pipeline',
    wait_for_completion=True,
    dag=dag
)

trigger_model_pipeline = TriggerDagRunOperator(
    task_id='trigger_model_training_pipeline',
    trigger_dag_id='model_training_pipeline',
    wait_for_completion=True,
    dag=dag
)

# trigger_data_pipeline = DummyOperator(
#     task_id='trigger_data_engineering_pipeline',
#     dag=dag,
# )
#
# trigger_model_pipeline = DummyOperator(
#     task_id='trigger_model_training_pipeline',
#     dag=dag,
# )

trigger_data_pipeline >> trigger_model_pipeline
