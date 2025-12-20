FROM python:3.11-slim
WORKDIR /app
COPY src/ ./src/
RUN pip install --no-cache-dir fastapi uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
