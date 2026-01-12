#!/bin/bash

# Load environment variables from .env if present
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | xargs)
fi

# Set default values if not in .env
DB_NAME=${DB_NAME:-revana_hms_db}
DB_USER=${DB_USER:-root}
DB_PASSWORD=${DB_PASSWORD:-root}
DB_HOST=${DB_HOST:-127.0.0.1}
DB_PORT=${DB_PORT:-3306}

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
FILENAME="db_backup_${TIMESTAMP}.sql"

echo "Exporting database '${DB_NAME}' from ${DB_HOST}..."

# Try exporting using docker if container exists
if docker ps --format '{{.Names}}' | grep -q "rhms_db"; then
    echo "Detected running Docker container 'rhms_db'. Exporting via Docker..."
    docker exec rhms_db mysqldump -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" > "$FILENAME"
else
    # Fallback to local mysqldump
    if ! command -v mysqldump &> /dev/null; then
        echo "Error: mysqldump could not be found and no 'rhms_db' container is running."
        exit 1
    fi
    mysqldump -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" > "$FILENAME"
fi

if [ $? -eq 0 ]; then
    echo "Database exported successfully to ${FILENAME}"
else
    echo "Error exporting database!"
    rm "$FILENAME"
    exit 1
fi
