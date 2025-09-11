# Benchmarking DuckDB vs Pandas

This submodule uses a Kubernetes job to compare the performance of DuckDB against Pandas with New York Taxi data.

## Setup

I use Minikube as my Kubernetes implementation. To get started, make sure to follow the [installation instructions](https://minikube.sigs.k8s.io/docs/start/) for your OS.

I also use Docker for my container runtime, make sure that's installed as well.

## Run the script

To run the benchmark, you can simply call `./run.sh` which will build the Docker image, get the data and configure a Kubernetes job to run the benchmark script. The benchmark will perform a simple group by over `passenger_count` with aggregation by `fare_amount`. The script will incrementally iterate the number of months of data until it either fails or parses a full year's worth of data. Each iteration will print the results of the calculation for Pandas and DuckDB to compare results as well as display the time taken for the benchmark and memory consumed. This is what the output should look like for one iteration:

```
Running benchmark with 3 months of data

Pandas result:
    passenger_count  fare_amount
0              0.0    16.585719
1              1.0    17.741896
2              2.0    20.253134
3              3.0    20.184723
4              4.0    21.918963
5              5.0    17.730861
6              6.0    17.318611
7              7.0    52.930000
8              8.0    77.122976
9              9.0    45.588235
Pandas took 8.01s and consumed 3124.90 MB of memory

DuckDB result:
     passenger_count  avg(fare_amount)
0                 0         16.585719
1                 1         17.741896
2                 2         20.253134
3                 3         20.184723
4                 4         21.918963
5                 5         17.730861
6                 6         17.318611
7                 7         52.930000
8                 8         77.122976
9                 9         45.588235
10             <NA>         19.072759
DuckDB took 0.46s and consumed 44.46 MB of memory
```

The benchmark may also exit early. This is most likely due to the Pandas benchmark consuming too much memory and being forefully terminated by Minikube. You can rerun the benchmark script with higher VM memory using the --memory flag when starting the Minikube cluster but you will need to delete the cluster before doing so. i.e. 

```
minikube delete;
minikube start --memory=15000mb; # on my instance minikube by default starts with 3900mb
./run.sh
```

After the first run, if you want to rerun the benchmark, you can toggle the --use_cache option to avoid redownloading the dataset i.e. `./run.sh --use_cache`. 

## Analysis of results

Unsuprisingly, DuckDB significantly outperforms Pandas on both execution time and memory usage. On my machine, With a full year's worth of data, DuckDB will take ~0.25s whereas Pandas will take about 36x as long at 9.2s. With Pandas, the memory usage increases approximately linearly starting from ~1.6 GB for a single month to ~12 GB for the full year. DuckDB on the other hand stays fairly flat, at around 50-80 MB regardless of the size of the dataset.

The speed I'm not surprised by, DuckDB has a variety of optimizations to make things run faster. What does surprise me though is that the memory usage stays constant. Not 100% sure, but if I had to guess, it'd be due to the fact that DuckDB uses a columnar data format, whereas Pandas does things by rows. This means that DuckDB can effectively 'stream' the dataset to perform it's calculation without having to load everything into memory whereas Pandas does require everything in memory before being able to proceed.


