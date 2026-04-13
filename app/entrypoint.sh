#!/bin/sh
set -e

DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}

echo "жду пока бд поднимется..."
until nc -z -v -w3 "$DB_HOST" "$DB_PORT"; do
  echo "Database is unavailable - sleeping"
  sleep 1
done

echo "запускаю миграции..."
alembic upgrade head

echo "запускаю сервер..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000