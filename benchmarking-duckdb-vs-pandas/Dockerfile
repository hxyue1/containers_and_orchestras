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
    psutil

WORKDIR /app
COPY benchmark.py get_ny_taxi.sh ./
RUN chmod +x get_ny_taxi.sh

CMD ["/bin/bash", "-c", "./get_ny_taxi.sh && python benchmark.py"]
