FROM python:3.11

WORKDIR /app
#COPY requirements.txt requirements.txt
#RUN pip install -r requirements.txt
RUN pip install streamlit
COPY . /app

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
