#!/bin/sh

# Define the container name, database name, user, and dump file path
CONTAINER_NAME="db_postgres"
DB_NAME="flavor_forest"
DB_USER="username"
DUMP_FILE="$HOME/git/flavor_forest/postgres/dump.sql"

# Perform the database dump
echo "Creating database dump..."
docker exec -t $CONTAINER_NAME pg_dumpall -c -U $DB_USER > "$DUMP_FILE"

# Continue with the push if no new commit was created
exit 0
