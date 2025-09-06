
#!/usr/bin/env bash

CLEAN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --clean)
        CLEAN=true
        ;;
    esac
    shift
done

if [ "$CLEAN" = true ]; then
    docker build -t hxyue1/duckdb-vs-pandas:latest .
    docker push hxyue1/duckdb-vs-pandas:latest
    kubectl delete pvc duckdb-pvc --ignore-not-found
fi

kubectl delete job duckdb-job --ignore-not-found
kubectl apply -f pvc.yaml
kubectl apply -f duckdb-job.yaml
kubectl wait --for=condition=Ready pod -l job-name=duckdb-job --timeout=120s
kubectl logs -f job/duckdb-job

