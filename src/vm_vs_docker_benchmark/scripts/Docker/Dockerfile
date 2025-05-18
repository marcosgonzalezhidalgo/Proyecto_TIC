FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    sysbench curl procps \
    && pip install psutil \
    && rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app

CMD ["python", "docker_benchmark.py"]
