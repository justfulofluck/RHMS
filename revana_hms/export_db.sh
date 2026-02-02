#!/bin/bash

# Load environment variables from .env if present
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | xargs)
fi

# Set default values if not in .env
DB_NAME=${DB_NAME:-reevanahms}
DB_USER=${DB_USER:-rhms_user}
DB_PASSWORD=${DB_PASSWORD:-klsaDb23@#}
DB_HOST=${DB_HOST:-127.0.0.1}
DB_PORT=${DB_PORT:-3306}

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
FILENAME="db_backup_${TIMESTAMP}.sql"

echo "Exporting database '${DB_NAME}' from ${DB_HOST}..."

# Check if mysqldump is available
if ! command -v mysqldump &> /dev/null; then
    echo "Error: mysqldump could not be found. Please install MySQL client tools."
    exit 1
fi

# Test database connection before exporting
echo "Testing database connection..."
if ! mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" -e "USE $DB_NAME;" &> /dev/null; then
    echo "Error: Cannot connect to database '$DB_NAME' with provided credentials."
    echo "Please check your .env file or database configuration."
    exit 1
fi

# Export database
echo "Exporting database '${DB_NAME}' from ${DB_HOST}..."
mysqldump --no-tablespaces -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" > "$FILENAME"

if [ $? -eq 0 ]; then
    echo "Database exported successfully to ${FILENAME}"
else
    echo "Error exporting database!"
    rm "$FILENAME"
    exit 1
fi
