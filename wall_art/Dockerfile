FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scrabble.py scrabble_dash.py ./

# Cloud Run sets $PORT; shell form so it's expanded at container start.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 scrabble_dash:server
