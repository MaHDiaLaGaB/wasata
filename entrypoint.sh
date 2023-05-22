#!/bin/sh

cd /wasata || exit

# Run Alembic migrations
alembic upgrade head

# Start the application
exec uvicorn app.server:app --host 0.0.0.0 --port 8888