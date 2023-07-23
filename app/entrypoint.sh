#!/bin/bash

# Function to execute Alembic command with retry on error
execute_alembic_command() {
  local command=$1
  local max_attempts=$2
  local attempt=0

  while true; do
    ((attempt++))
    echo "Executing Alembic command: $command (Attempt: $attempt)"

    if $command; then
      echo "Alembic command executed successfully."
      break
    fi

    if ((attempt >= max_attempts)); then
      echo "Max attempts reached. Unable to execute Alembic command."
      exit 1
    fi

    echo "Error executing Alembic command. Retrying in 2 seconds..."
    sleep 2
  done
}


# Execute alembic upgrade head command with retry

execute_alembic_command "alembic -c alembic.ini upgrade head"

# Start the server
uvicorn app.server:app --host 0.0.0.0 --port "${WASATA_PORT}" --reload
