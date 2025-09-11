
#!/usr/bin/env bash

USE_CACHE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --use_cache)
        USE_CACHE=true
        ;;
    esac
    shift
done

docker build -t hxyue1/duckdb-vs-pandas:latest .
docker push hxyue1/duckdb-vs-pandas:latest

kubectl delete job duckdb-job --ignore-not-found
if [ "$USE_CACHE" = false ]; then
    kubectl get pvc duckdb-pvc &>/dev/null && \
    kubectl patch pvc duckdb-pvc -p '{"metadata":{"finalizers":null}}' && \
    kubectl delete pvc duckdb-pvc --ignore-not-found
fi
kubectl apply -f pvc.yaml
kubectl apply -f duckdb-job.yaml
while [[ "$(kubectl get pod -l job-name=duckdb-job -o jsonpath='{.items[0].status.phase}')" == "Pending" ]]; do
    echo "Container is booting up please wait"
    sleep 5
done
kubectl logs -f job/duckdb-job

