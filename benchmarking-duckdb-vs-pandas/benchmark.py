import duckdb
import pandas as pd
import psutil
import time

from multiprocessing import Process, Queue


data_path="data/yellow_tripdata_2024-01.parquet"

def benchmark_pandas():
    start = time.time()
    df = pd.read_parquet(data_path)
    result = df.groupby("passenger_count")["fare_amount"].mean()
    elapsed = time.time() - start
    rss_mb = psutil.Process().memory_info().rss/(1024*1024)
    print(f"Pandas took {elapsed} and consumed {rss_mb} MB")

def benchmark_duckdb():
    start = time.time()
    con = duckdb.connect()
    result = con.execute(f"""
        SELECT passenger_count, AVG(fare_amount)
        FROM '{data_path}'
        GROUP BY passenger_count
    """).fetchdf()
    elapsed = time.time() - start
    rss_mb = psutil.Process().memory_info().rss/(1024*1024)
    print(f"DuckDB took {elapsed} and consumed {rss_mb} MB")

if __name__ == "__main__":
    queue = Queue()
    p1=Process(target=benchmark_pandas)
    p2=Process(target=benchmark_duckdb)
    p1.start()
    p1.join()
    p2.start()