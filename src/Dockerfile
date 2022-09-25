FROM python:3.10-slim-buster

RUN apt-get update &&  \
    apt-get --no-install-recommends -y install curl netcat gcc postgresql &&  \
    apt-get clean

WORKDIR /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --without dev ; fi"

COPY . ./
ENV PYTHONPATH=./
