FROM python:3.12-slim

WORKDIR /app

RUN pip --no-cache-dir install poetry==1.8.3

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY chatbot chatbot

CMD ["poetry", "run", "main"]
