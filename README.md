## Practical Machine Learning and Deep Learning Assignment 1
### Deployment - Student Exam Performance Prediction
This is a homework at Innopolis University to demonstrate basic mlops practices. I chose a simple task - [kaggle dataset](https://www.kaggle.com/datasets/lainguyn123/student-performance-factors) and linear regression from sklearn.

Speaking of mlops, the following were used:
- mlflow for model training and registry
- airflow for child dags - data engineering, model training, deployment
- airflow for parent dag - schedules child dags
- joblib for encoders and scalers registry
- fastapi + uvicorn for backend
- streamlit for frontend
- docker compose for deployment

To start airflow dag, you need to:
1. Configure it with LocalExecutor and PostresSQL/MSSQL (multithreading is needed for parent dag + child dag)
2. Start airflow server
3. Turn on all child dags, then turn on parent dag

After success completion of all dags, you can access frontend through http://localhost:8501/
