#!/bin/sh

# Only wait for PostgreSQL if using local Docker database (host=db)
if [ "$DB_HOST" = "db" ]; then
    echo "Waiting for local PostgreSQL to be ready..."
    echo "DB_HOST: $DB_HOST"
    echo "DB_PORT: $DB_PORT"
    echo "DB_NAME: $DB_NAME"
    echo "DB_USER: $DB_USER"

    max_attempts=60
    attempt=0

    until python -c "import psycopg2; psycopg2.connect(host='$DB_HOST', port=$DB_PORT, user='$DB_USER', password='$DB_PASSWORD', dbname='$DB_NAME')" 2>/dev/null; do
        attempt=$((attempt + 1))
        if [ $attempt -ge $max_attempts ]; then
            echo "PostgreSQL is still unavailable after $max_attempts attempts. Exiting."
            exit 1
        fi
        echo "PostgreSQL is unavailable - sleeping (attempt $attempt/$max_attempts)"
        sleep 2
    done

    echo "PostgreSQL is ready!"
else
    echo "Using external database - skipping PostgreSQL wait"
    echo "DB_HOST: $DB_HOST"
fi

echo "Running migrations..."
python manage.py makemigrations --noinput || true
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput || true

echo "Importing products..."
python manage.py import_produtos --file core/management/commands/produtos_backup.json || true

echo "Starting server..."
exec "$@"

