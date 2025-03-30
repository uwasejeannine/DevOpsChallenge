#!/bin/bash

# Wait for the database to be ready
echo "Waiting for database..."
until nc -z db 5432; do
  sleep 1
done
echo "Database is up!"

# Apply database migrations
echo "Applying migrations..."
python manage.py migrate

# Start the application
echo "Starting server..."
exec "$@"