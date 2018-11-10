#!/bin/sh
source env/bin/activate

exec gunicorn -b :5000 --workers=2 --access-logfile - --error-logfile - app:app
