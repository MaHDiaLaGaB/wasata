#!/bin/bash

# This is run one-time during the first time Postgres is initialized

echo "Creating database ${DB_NAME} and user..."

# Create the user and database "api"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER ${POSTGRES_USER} WITH ENCRYPTED PASSWORD '${POSTGRES_PASSWORD}';
    CREATE DATABASE ${DB_NAME} OWNER ${POSTGRES_USER};
    GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${POSTGRES_USER};
EOSQL