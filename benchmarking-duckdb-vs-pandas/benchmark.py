import argparse
import duckdb
import pandas as pd
import psutil
import os
import time

from multiprocessing import Process, Queue


def benchmark_pandas(data_paths):
    start = time.time()
    all_dfs = []
    for data_path in data_paths:
        df_temp = pd.read_parquet(data_path)
        all_dfs.append(df_temp)
    df = pd.concat(all_dfs)

    res = df.groupby("passenger_count")["fare_amount"].mean()
    res = res.reset_index()
    res.columns = ["passenger_count", "fare_amount"]


    elapsed = time.time() - start
    rss_mb = psutil.Process().memory_info().rss/(1024*1024)
    print(f"Pandas result:\n {res}")
    print(f"Pandas took {elapsed:.2f}s and consumed {rss_mb:.2f} MB of memory\n", flush=True)

def benchmark_duckdb(data_paths):
    start = time.time()

    query_string = f"""SELECT passenger_count, AVG(fare_amount)
    FROM read_parquet({data_paths})
    GROUP BY passenger_count
    ORDER BY passenger_count"""

    con = duckdb.connect()
    res = con.execute(query_string).fetchdf()
    con.close()

    elapsed = time.time() - start
    rss_mb = psutil.Process().memory_info().rss/(1024*1024)

    print(f"DuckDB result:\n {res}")
    print(f"DuckDB took {elapsed:.2f}s and consumed {rss_mb:.2f} MB of memory\n", flush=True)

def run(data_dir):
    data_paths = []
    # should be range(1,13, but for some reason if I go above 11, the pandas output doesn't print
    for month in range(1,11):
        for taxi_type in ["yellow", "green"]:
            month_str = str(month).zfill(2)
            data_paths.append(os.path.join(data_dir, f"{taxi_type}_tripdata_2024-{month_str}.parquet"))

    print("Group by + Aggregation: Pandas vs DuckDB\n", flush=True)
    p1=Process(target=benchmark_pandas, args=(data_paths,))
    p2=Process(target=benchmark_duckdb, args=(data_paths,))
    p1.start()
    p1.join()
    p2.start()

if __name__ == "__main__":
    data_dir = "data"
    run(data_dir)
