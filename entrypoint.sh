#!/bin/bash

# Exit on any error
set -e

# Load environment variables from .env file
if [ -f .env ]; then
    echo "Loading environment variables from .env file"
    # shellcheck disable=SC2046
    export $(grep -v '^#' .env | xargs)
else
    echo ".env file not found, using existing environment variables"
fi

wait_for_db() {
    echo "Waiting for database to be ready..."

    POSTGRES_HOST=${POSTGRES_HOST:-localhost}
    POSTGRES_PORT=${POSTGRES_PORT:-5432}
    POSTGRES_DB=${POSTGRES_DB:-mydatabase}
    POSTGRES_USER=${POSTGRES_USER:-postgres}

    until PGPASSWORD=${POSTGRES_PASSWORD} psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' >/dev/null 2>&1; do
        echo "Database is unavailable - sleeping"
        sleep 1
    done

    echo "Database is up and running!"
}

# Wait for database
wait_for_db

# Run Alembic migrations
echo "Running database migrations..."
alembic upgrade head

# Start the FastAPI application
echo "Starting FastAPI application..."
exec uvicorn -- factory app.main:create_production_app --host 0.0.0.0 --port "${APP_PORT:-8000}" --reload