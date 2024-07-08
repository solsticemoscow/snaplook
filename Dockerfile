FROM python:3.11-slim

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN ln -snf /usr/share/zoneinfo/Europe/Moscow /etc/localtime

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y gcc \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev libgl1 libglib2.0-0 \
  # cleaning up unused files
  && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /code/requirements.txt

RUN pip3 install --no-cache-dir --upgrade --default-timeout=10 -r /code/requirements.txt


COPY ./app/ /code/app



