#!/bin/bash
set -e

echo "==== Build Started ===="

echo "📂 Collecting Static Files..."
python3.12 manage.py collectstatic --noinput --clear || python3 manage.py collectstatic --noinput --clear

echo "🗄️ Running Migrations..."
python3.12 manage.py migrate --noinput || python3 manage.py migrate --noinput

echo "✅ Build Complete!"
