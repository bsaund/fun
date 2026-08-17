FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
CMD ["sh", "-c", "exec gunicorn --bind :${PORT:-8080} --workers 2 main:app"]
