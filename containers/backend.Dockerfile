FROM python:3.10-slim

RUN pip install --no-cache-dir poetry

WORKDIR /app
COPY ./backend/poetry.lock ./backend/pyproject.toml ./
# Export dependencies from Poetry to requirements.txt
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./backend /app
EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=.
