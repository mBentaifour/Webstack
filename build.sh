#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Collect static files
python webstack_django/manage.py collectstatic --noinput

# Apply migrations if needed
# python webstack_django/manage.py migrate --noinput
