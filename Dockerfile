FROM python:3.10.12-slim


WORKDIR /webhook


COPY ./requirements.txt /webhook/requirements.txt


RUN pip install --upgrade pip


RUN pip install --no-cache-dir --upgrade -r /webhook/requirements.txt


COPY ./app /webhook/app


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
