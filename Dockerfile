FROM python:3.10.1-slim-bullseye

LABEL maintainer="github.com/bbt-t" description="aiogram-telegram bot"

WORKDIR /app

ENV PIP_NO_CACHE_DIR=true \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONDONTWRITEBYTECODE=true

RUN apt update &&  \
    apt upgrade && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean &&  \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./
RUN pip install -U pip poetry && poetry install --no-dev

COPY . .

ENTRYPOINT ["python", "start.py"]

