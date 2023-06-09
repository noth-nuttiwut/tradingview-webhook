FROM tiangolo/uvicorn-gunicorn:python3.10-slim

LABEL maintainer="Nuttiwut Simsiri <nuttiwutsimsiri@gmail.com>"

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./app /app