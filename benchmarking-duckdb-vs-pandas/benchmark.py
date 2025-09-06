import argparse
import duckdb
import pandas as pd
import psutil
import os
import time

from multiprocessing import Process, Queue


def benchmark_pandas(data_path):
    start = time.time()
    df = pd.read_parquet(data_path)
    df.groupby("passenger_count")["fare_amount"].mean()
    elapsed = time.time() - start
    rss_mb = psutil.Process().memory_info().rss/(1024*1024)
    print(f"Pandas took {elapsed} and consumed {rss_mb} MB")

def benchmark_duckdb(data_path):
    start = time.time()
    con = duckdb.connect()
    con.execute(f"""
        SELECT passenger_count, AVG(fare_amount)
        FROM '{data_path}'
        GROUP BY passenger_count
    """).fetchdf()
    elapsed = time.time() - start
    rss_mb = psutil.Process().memory_info().rss/(1024*1024)
    print(f"DuckDB took {elapsed} and consumed {rss_mb} MB")

def run(data_dir):
    data_path = os.path.join(data_dir, "yellow_tripdata_2024-01.parquet")
    p1=Process(target=benchmark_pandas, args=(data_path,))
    p2=Process(target=benchmark_duckdb, args=(data_path,))
    p1.start()
    p1.join()
    p2.start()

if __name__ == "__main__":
    data_dir = "data"
    run(data_dir)
