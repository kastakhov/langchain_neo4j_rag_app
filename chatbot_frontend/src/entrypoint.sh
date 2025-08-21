#!/bin/bash
set -e

# Run any setup steps or pre-processing tasks here
echo "Starting hospital chatbot frontend..."

echo "Waiting for the backend to be ready..."
python wait_for_backend.py

# Run the ETL script
echo "Starting Streamlit frontend..."
streamlit run Chatbot.py --server.fileWatcherType none --browser.gatherUsageStats false
