#!/usr/bin/env bash

set -e
set -v

cd src/tuberlin

python manage.py dumpdata users > users/fixtures/customuser.json --indent=4
python manage.py dumpdata inventory > inventory/fixtures/inventory.json --indent=4