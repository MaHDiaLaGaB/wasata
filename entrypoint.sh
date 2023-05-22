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

# Wait for the dev-postgres container to be ready
#wait_for_postgres

# Execute alembic stamp head command with retry
execute_alembic_command "alembic stamp head" 3

# Execute alembic revision --autogenerate -m "start-tables" command with retry
execute_alembic_command "alembic revision --autogenerate -m 'start-tables'" 3

# Execute alembic upgrade head command with retry
execute_alembic_command "alembic upgrade head" 3

# Start the server
uvicorn app.server:app --host 0.0.0.0 --port 8888
