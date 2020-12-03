FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY requirements.txt /tmp/

RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN python -c "from detoxify import Detoxify; model = Detoxify('original')"

COPY main.py /app/
