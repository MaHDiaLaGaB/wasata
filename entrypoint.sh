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

# Determine the environment and set the appropriate Alembic config file
if [ "$ENVIRONMENT" = "dev" ]; then
  alembic_config="alembic-dev.ini"
elif [ "$ENVIRONMENT" = "demo" ]; then
  alembic_config="alembic-demo.ini"
else
  echo "Invalid environment: $ENVIRONMENT. Please set ENV to 'dev' or 'demo'."
  exit 1
fi

# Execute alembic upgrade head command with retry
execute_alembic_command "alembic -c $alembic_config upgrade head" 3

# Start the server
uvicorn app.server:app --host 0.0.0.0 --port "${WASATA_PORT}" --reload
