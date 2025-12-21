#!/bin/bash
set -e

echo "Installing frontend dependencies..."
cd /app/frontend
npm install

echo "Building frontend..."
npm run build

echo "Installing backend dependencies..."
cd /app
uv sync


echo "Running migrations..."
cd /app/backend
uv run alembic upgrade head

echo "Starting server..."
cd /app
exec uv run python main.py

echo "Press Ctrl+C to exit log."