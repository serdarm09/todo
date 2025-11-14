#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Changing to app directory..."
cd app

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Build completed!"