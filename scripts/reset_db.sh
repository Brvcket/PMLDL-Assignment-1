airflow db reset
airflow db init
airflow users create \
--role Admin \
--username admin \
--email admin@example.org \
--firstname admin \
--lastname admin \
--password admin
mkdir -p $AIRFLOW_HOME/logs $AIRFLOW_HOME/dags
echo > $AIRFLOW_HOME/logs/scheduler.log
echo > $AIRFLOW_HOME/logs/triggerer.log
echo > $AIRFLOW_HOME/logs/webserver.log
echo *.log >> $AIRFLOW_HOME/logs/.gitignore
airflow scheduler --daemon --log-file services/airflow/logs/scheduler.log
airflow webserver --daemon --log-file services/airflow/logs/webserver.log
airflow triggerer --daemon --log-file services/airflow/logs/triggerer.log