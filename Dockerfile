FROM python:3.11-slim
LABEL authors="Daniil"
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
