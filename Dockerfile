FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry==2.1.4
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root --no-interaction --no-ansi

COPY . /app/

# entrypoint (у тебя уже создан на шаге 3)
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
