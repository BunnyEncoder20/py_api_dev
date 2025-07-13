#!/bin/bash

# Wait until DB is ready (optional)
echo "[Server] ⏳ Waiting for DB to be ready..."
sleep 3

# Run Alembic migrations
echo "[Alembic] ⬆️ Running migrations..."
alembic upgrade head

# Start the server
echo "[Uvicorn] 🚀 Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
