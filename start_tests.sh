#! /usr/bin/env bash
set -e

python app/pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python app/initial_data.py

python -m unittest discover