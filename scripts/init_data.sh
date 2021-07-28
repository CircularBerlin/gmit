#!/usr/bin/env bash

set -e
set -v

cd src/tuberlin

echo "Clearing the database"
python manage.py flush

echo "Migrating the database"
python manage.py migrate

python manage.py createsuperuser

python manage.py loaddata inventory.json

python manage.py init_categories

