FROM python:3.12.4-slim-bookworm as base

ENV PYTHONUNBUFFERED 1

COPY ./requirements /requirements

RUN apt-get update && apt-get -y install \
  poppler-utils \
  gnupg \
  build-essential \
  libpq-dev \
  gcc \
  rustc \
  libpng-dev \
  zlib1g-dev \
  libjpeg-dev \
  libxmlsec1-dev \
  libxml2-dev \
  pkg-config \
  --no-install-recommends \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get clean

RUN pip3 install --upgrade pip==24.0

COPY ./environments/.env /.env

FROM base AS APP
ARG ENVIRONMENT

RUN pip3 install -r ./requirements/$ENVIRONMENT.txt

COPY ./app /app

RUN groupadd -r django \
  && useradd -r -g django django \
  && chown -R django:django /app

WORKDIR /app
EXPOSE 8080
EXPOSE 8180
EXPOSE 8280
