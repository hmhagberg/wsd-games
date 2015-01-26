#!/bin/bash
# Script for resetting the database

# remove old database:
rm db.sqlite3
# remove old migrations:
rm games/migrations/*initial.py
# make and do migrations:
python3 manage.py makemigrations
python3 manage.py migrate
# load fixture
python3 manage.py loaddata games/fixtures/wsd-games-data.xml
