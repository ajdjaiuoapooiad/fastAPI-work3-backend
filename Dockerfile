FROM python:3.11-slim-buster


WORKDIR /app


COPY pyproject.toml poetry.lock ./
RUN pip install --upgrade pip && pip install poetry
RUN poetry config virtualenvs.in-project true && poetry install --no-root


COPY app ./app
COPY .env .


CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]

