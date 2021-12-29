FROM python:3.10.1

WORKDIR /app

ENV PIP_NO_CACHE_DIR=false \
    POETRY_VIRTUALENVS_CREATE=false

RUN pip install -U poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev
COPY . .

CMD ["python", "start.py"]

