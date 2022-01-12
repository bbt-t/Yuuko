FROM python:3.10.1-slim-bullseye

WORKDIR /app

ENV PIP_NO_CACHE_DIR=true \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONDONTWRITEBYTECODE=true

RUN apt update &&  \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean &&  \
    rm -rf /var/lib/apt/lists/*

RUN pip install -U pip poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

COPY . .

ENTRYPOINT ["python", "start.py"]

