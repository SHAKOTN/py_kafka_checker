FROM python:3.8.3-alpine3.11 AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev bash

RUN pip install --upgrade pip
RUN pip install dumb-init==1.2.2

ADD consumer/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
RUN rm -f /app/requirements.txt

ADD consumer /app/consumer/

WORKDIR /app

FROM base as local

FROM base as test

FROM base as production
ENTRYPOINT ["/usr/local/bin/dumb-init", "--"]
