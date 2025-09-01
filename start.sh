#!/bin/bash

# This script runs every time the container starts.

# Step 1: Run the database initialization script to create/update
# the mlb.duckdb file with the correct, container-relative paths.
echo "Running database initialization..."
python -m db.duckdb_init

# Step 2: Start the Uvicorn server as the main process.
# The --host 0.0.0.0 is crucial for Docker networking.
echo "Starting Uvicorn server..."
exec uvicorn api.main:app --host 0.0.0.0 --port 8080

