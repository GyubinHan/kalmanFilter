
FROM python:3.9.12-slim
# 디폴트 폴더 변경
WORKDIR /app

# Pip 패키지 설치
COPY requirements5.txt requirements.txt
COPY kalman10dockerkafka0.py /app/kalman10docker.py
COPY /docker-volume/  /app/logFile
RUN pip install -r requirements.txt
RUN pip install pykalman
RUN pip install kafka-python


CMD ["python","kalman10docker.py"]

