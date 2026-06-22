#!/bin/bash
# Start Redis in background
redis-server --daemonize yes --port 6379 --loglevel warning

# Wait for Redis to be ready
sleep 1

# Start FastAPI backend on port 5000
cd backend
exec uvicorn main:app --host 0.0.0.0 --port 5000 --reload
