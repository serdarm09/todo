#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Collect static files
cd app
python manage.py collectstatic --noinput

# Make migrations (if needed)
python manage.py makemigrations --noinput
python manage.py migrate --noinput