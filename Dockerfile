FROM python:3.9-alpine AS celery-exporter-ng

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY main.py /app/
COPY utils.py /app/
COPY logger.py /app/

ENTRYPOINT python main.py
