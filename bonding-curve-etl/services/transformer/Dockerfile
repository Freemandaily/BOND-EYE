FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir apache-airflow
CMD ["/bin/sh", "-c", "echo 'run transformer container' && sleep infinity"]
