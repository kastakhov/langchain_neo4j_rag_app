#!/bin/bash
set -e

# Run any setup steps or pre-processing tasks here
echo "Starting hospital RAG FastAPI service..."

# Wait for the database to be ready
echo "Waiting for the database to be ready..."
python wait_for_db.py

echo "Waiting for the neoj4 etl loading to be done..."
python wait_for_neoj4_etl.py

# Start the main application
echo "Starting FastAPI service..."
python main.py
