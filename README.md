## Practical Machine Learning and Deep Learning Assignment 1
### Deployment - Student Exam Performance Prediction
This is a homework at Innopolis University to demonstrate basic mlops practices. I chose a simple task - [kaggle dataset](https://www.kaggle.com/datasets/lainguyn123/student-performance-factors) and linear regression from sklearn.

**Speaking of mlops, the following were used:**
- mlflow for model training and registry
- airflow for child dags - data engineering, model training, deployment
- airflow for parent dag - schedules child dags
- joblib for encoders and scalers registry
- fastapi + uvicorn for backend
- streamlit for frontend
- docker compose for deployment

**To start airflow dag, you need to:**
1. Configure it with LocalExecutor and PostresSQL/MSSQL (multithreading is needed for parent dag + child dag):
   https://airflow.apache.org/docs/apache-airflow/2.10.2/howto/set-up-database.html#choosing-database-backend
   https://airflow.apache.org/docs/apache-airflow/2.10.2/core-concepts/executor/index.html
3. Configure environment variable. Go to project root and write:
   
   ```sh
   export PROJECT_DIR=$PWD
   ```
4. Start airflow server:

   ```sh
   airflow standalone
   ```
6. Turn on all child dags, then turn on parent dag

After success completion of all dags, you can access frontend through http://localhost:8501/
