  FROM python:3.10.6-buster
  COPY ./foodE /foodE
  COPY ./api /api
  COPY ./requirements.txt requirements.txt
  COPY ./google_key.json google_key.json
  RUN apt-get update
  RUN apt-get install gcc -y
  RUN pip install --no-cache-dir --upgrade -r requirements.txt
  CMD uvicorn api.fast:app --host 0.0.0.0 --port 8000
