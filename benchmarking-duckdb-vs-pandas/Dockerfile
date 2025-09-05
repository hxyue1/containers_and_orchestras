FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    gcc \
    && rm -rf /var/lib/apt/lists/* # To save space

RUN pip install --no-cache-dir \
    duckdb \
    pandas \
    pyarrow \
    psutil \

COPY benchmark.py .

CMD ["python", "benchmark.py"]
