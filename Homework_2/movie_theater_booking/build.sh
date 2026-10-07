#!/usr/bin/env bash
# Build steps for Render. Stops immediately if any step fails.
set -o errexit

pip install -r ../requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py seed
# Creates an admin login from environment variables; ignored if it already exists.
python manage.py createsuperuser --no-input || true
