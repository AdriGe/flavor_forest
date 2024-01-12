#!/bin/sh

# Define the path to your SQL dump file, database name, user, and container name
DUMP_FILE=$HOME/git/flavor_forest/postgres/dump.sql
DB_NAME="flavor_forest"
DB_USER="username"
CONTAINER_NAME="db_postgres"
CHANGED_DUMP=`git diff HEAD@{1} --stat -- $HOME/git/flavor_forest/postgres/dump.sql | wc -l`

# Function to check if the container is running
is_container_running() {
    [ "$(docker inspect -f '{{.State.Running}}' $CONTAINER_NAME)" = "true" ]
}

# Function to terminate active connections
terminate_connections() {
    echo "Terminating active connections to the database..."
    docker exec -i $CONTAINER_NAME psql -U $DB_USER -d postgres -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '$DB_NAME' AND pid <> pg_backend_pid();"
}

# Check if the SQL dump file exists
if [ $CHANGED_DUMP -gt 0 ]; then

    # Check if the container is running
    CONTAINER_WAS_RUNNING=true
    if ! is_container_running; then
        CONTAINER_WAS_RUNNING=false
        echo "Starting Docker container..."
        docker start $CONTAINER_NAME
        # Wait a bit for the container to start up
        sleep 10
    fi

    # Terminate active connections
    terminate_connections

    # Wait for a brief moment to ensure connections are closed
    sleep 5

    # Import the SQL data into PostgreSQL
    cat "$DUMP_FILE" | docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME

    # Stop the container if it was not running before the script
    if [ "$CONTAINER_WAS_RUNNING" = "false" ]; then
        echo "Stopping Docker container..."
        docker stop $CONTAINER_NAME
    fi
fi
