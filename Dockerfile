FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY requirements.txt /tmp/

RUN pip install --no-cache-dir -r /tmp/requirements.txt

ADD "https://github.com/unitaryai/detoxify/releases/download/v0.1-alpha/toxic_original-c1212f89.ckpt" "/app/model.ckpt"

COPY main.py /app/
