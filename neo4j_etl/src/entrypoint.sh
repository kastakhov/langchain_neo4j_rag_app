#!/bin/bash
set -e

# Run any setup steps or pre-processing tasks here
echo "Running ETL to move hospital data from csvs to Neo4j..."

# Wait for the database to be ready
echo "Waiting for the database to be ready..."
python wait_for_db.py

# Run the ETL script
echo "Starting local http server..."
python simple_http_server.py &
for i in {1..5}; do
  echo "Waiting for the server to start..."
  sleep 1
done

echo "Starting hospital ETL processing..."
echo '{"status": "running"}' > data/status.json
python hospital_bulk_csv_write.py && \
  echo "Hospital ETL processing complete." && \
  echo '{"status": "loaded"}' > data/status.json && \
  echo "Sleep forever..." && \
  sleep infinity
