FROM python:3.11-slim
WORKDIR /app
COPY src/ ./src/
RUN pip install --no-cache-dir
CMD ["python", "src/worker.py"]
