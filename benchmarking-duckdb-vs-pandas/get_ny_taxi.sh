
#!/usr/bin/env bash
set -euo pipefail

BASE_URL="https://d37ci6vzurychx.cloudfront.net/trip-data"
YEAR="2024"
MONTH_NUMBERS=(01 02 03 04 05 06 07 08 09 10 11 12)
TAXI_TYPES=("yellow" "green")
DATA_DIR="./data"

mkdir -p "${DATA_DIR}"

echo -e "\nStarting downloads:\n"
for MONTH_NUMBER in "${MONTH_NUMBERS[@]}"; do
    for TAXI_TYPE in "${TAXI_TYPES[@]}"; do
        FILENAME="${TAXI_TYPE}_tripdata_${YEAR}-${MONTH_NUMBER}.parquet"
        URL="${BASE_URL}/${FILENAME}"
        OUTPUT_PATH="${DATA_DIR}/${FILENAME}"

        if [[ -f "${OUTPUT_PATH}" ]]; then
            echo "Skipping existing file ${FILENAME}"
            continue
        fi
        
        curl -fsL -# "${URL}" -o "${OUTPUT_PATH}" && echo "${FILENAME} downloaded"
        done
    done
echo -e "\nAll files downloaded\n"


