# syntax=docker/dockerfile:1.7-labs

FROM python:3.12-bookworm

EXPOSE 8000

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./web .


ENTRYPOINT [ "fastapi", "run", "main.py", "--root-path", "/api" ]