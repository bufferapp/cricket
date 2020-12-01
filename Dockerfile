FROM tiangolo/uvicorn-gunicorn-fastapi:latest

RUN pip install --no-cache-dir hatesonar oauth2client google-api-python-client

ENV MAX_WORKERS=2

COPY main.py /app/
