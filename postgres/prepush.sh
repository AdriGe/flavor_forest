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

# Function to start the container if not running and return it to its initial state afterwards
handle_container_state() {
    CONTAINER_WAS_RUNNING=true
    if ! is_container_running; then
        CONTAINER_WAS_RUNNING=false
        echo "Starting Docker container..."
        docker start $CONTAINER_NAME
        while ! is_container_running; do sleep 2; done
    fi
}

# Function to stop the container if it was not initially running
stop_container_if_needed() {
    if [ "$CONTAINER_WAS_RUNNING" = "false" ]; then
        echo "Stopping Docker container..."
        docker stop $CONTAINER_NAME
    fi
}

# Start the container if not running
handle_container_state

# Perform the database dump
echo "Creating database dump..."
docker exec -t $CONTAINER_NAME pg_dumpall -c -U $DB_USER > "$DUMP_FILE"

# Check if there are changes in the dump file
if ! git diff --exit-code --quiet -- "$DUMP_FILE"; then
    echo "Changes detected in the database dump. Creating a new commit..."
    git add "$DUMP_FILE"
    git commit -m "Update database dump"

    # Inform the user and exit with a non-zero status
    echo "Push rejected because a new commit containing the pg dum was added. Please re-run 'git push'."
    exit 1
fi

# Stop the container if it was not running before the script
stop_container_if_needed

# Continue with the push if no new commit was created
exit 0

#test