#!/bin/bash

# Upgrade pip
/opt/conda/bin/python /opt/conda/bin/pip install --upgrade pip

# Install requirements
/opt/conda/bin/python /opt/conda/bin/pip install -r requirements.txt

# Collect static files
/opt/conda/bin/python manage.py collectstatic --noinput

# Run migrations
/opt/conda/bin/python manage.py migrate --noinput
