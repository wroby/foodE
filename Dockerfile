  FROM python:3.10.6-buster
  COPY foodE /foodE
  COPY requirements.txt /requirements.txt
  RUN pip install -r requirements.txt
  CMD uvicorn foodE.api.fast:app --host 0.0.0.0
