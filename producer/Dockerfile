FROM python:3.8.3-alpine3.11 AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

RUN apk update && apk add gcc python3-dev musl-dev libffi-dev bash

RUN pip install --upgrade pip
RUN pip install dumb-init==1.2.2

ADD producer/requirements/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
RUN rm -f /app/requirements.txt

ADD producer /app/producer/
ADD producer_run.py /app/producer_run.py
ADD .env /app/.env

WORKDIR /app

FROM base as test
ADD producer/requirements/requirements-test.txt /app/requirements-test.txt
RUN pip install -r /app/requirements-test.txt
RUN rm -f /app/requirements-test.txt

FROM base as production
ENTRYPOINT ["/usr/local/bin/dumb-init", "--"]
