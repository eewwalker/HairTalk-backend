#!/bin/sh

echo "Starting Hair Talk backend application..."

#listen on all available network interfaces.
python manage.py run -h 0.0.0.0