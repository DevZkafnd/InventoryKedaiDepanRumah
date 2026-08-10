#!/bin/bash
set -e  # Exit on error

echo "==== Installing Dependencies with uv ===="
uv pip install -r requirements.txt --system

echo "==== Collecting Static Files ===="
python3.9 manage.py collectstatic --noinput --clear

echo "==== Running Migrations ===="
python3.9 manage.py migrate --noinput

echo "==== Build Complete ===="
