FROM python:3.11-slim

WORKDIR /app

# System deps (lightweight)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and models
COPY app.py ./app.py
COPY models ./models

ENV PORT=8080
CMD exec gunicorn --bind :$PORT --workers 2 --threads 4 app:app