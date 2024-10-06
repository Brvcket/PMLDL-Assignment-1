cat $AIRFLOW_HOME/airflow-webserver.pid | xargs kill -9
cat /dev/null >  $AIRFLOW_HOME/airflow-webserver.pid
airflow webserver -p 8080