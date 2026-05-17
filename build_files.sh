#!/bin/bash
cd gamezone
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py ensure_superuser
python manage.py seed_gamezone --if-empty
