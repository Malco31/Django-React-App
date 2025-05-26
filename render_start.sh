#!/bin/bash

# Exit on any error
set -o errexit

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Start the app using Gunicorn and Uvicorn worker
echo "Starting Gunicorn server..."
python -m gunicorn crud.asgi:application -k uvicorn.workers.UvicornWorker