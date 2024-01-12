#!/bin/sh

# Define the container name, database name, user, and dump file path
CONTAINER_NAME="db_postgres"
DB_NAME="flavor_forest"
DB_USER="username"
DUMP_FILE="$HOME/git/flavor_forest/postgres/dump.sql"

# Function to check if the container is running
is_container_running() {
    [ "$(docker inspect -f '{{.State.Running}}' $CONTAINER_NAME)" = "true" ]
}

# Start the container if not running
CONTAINER_WAS_RUNNING=true
if ! is_container_running; then
    CONTAINER_WAS_RUNNING=false
    echo "Starting Docker container..."
    docker start $CONTAINER_NAME
    
    # Check every 2 seconds if the container is up, for a maximum of 5 tries
    MAX_TRIES=5
    TRIES=0
    while ! is_container_running && [ $TRIES -lt $MAX_TRIES ]; do
        sleep 2
        TRIES=$((TRIES+1))
    done

    if ! is_container_running; then
        echo "Error: Docker container failed to start."
        exit 1
    fi
fi

# Perform the database dump
echo "Creating database dump..."
docker exec -t $CONTAINER_NAME pg_dumpall -c -U $DB_USER > "$DUMP_FILE"

# Add the dump file to the commit
git add "$DUMP_FILE"

# Stop the container if it was not running before the script
if [ "$CONTAINER_WAS_RUNNING" = "false" ]; then
    echo "Stopping Docker container..."
    docker stop $CONTAINER_NAME
fi

# Continue with the push
exit 0
#test6