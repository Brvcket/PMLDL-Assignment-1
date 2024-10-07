FROM python:3.11

WORKDIR /app
#COPY requirements.txt requirements.txt
#RUN pip install -r requirements.txt
RUN pip install pandas uvicorn mlflow pandas joblib fastapi
COPY . /app

ENV PROJECT_DIR /mnt/c/Users/ahmat/PycharmProjects/PMLDL-Assignment-1
#ENV PROJECT_DIR C:\Users\ahmat\PycharmProjects\PMLDL-Assignment-1

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
