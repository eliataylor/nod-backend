#!/bin/bash

# Set Path
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

# Find root .env
ENV_FILE="$PARENT_DIR/.env"

# Load variables from root .env
if [ -f "$ENV_FILE" ]; then
  export $(grep -v '^#' "$ENV_FILE" | xargs)
else
  echo ".env file not found in the parent directory. Please create a .env file with the necessary variables."
  exit 1
fi

# Check if necessary variables are set
missing_vars=()
for var in "${required_vars[@]}"; do
  if [ -z "${!var}" ]; then
    missing_vars+=("$var")
  fi
done

if [ ${#missing_vars[@]} -ne 0 ]; then
  echo "The following required environment variables are missing:"
  for var in "${missing_vars[@]}"; do
    echo " $var"
  done
  exit 1
fi

# Function to sanitize bucket name
sanitize_bucket_name() {
  local name="$1"
  # Convert to lowercase
  name=$(echo "$name" | tr '[:upper:]' '[:lower:]')
  # Replace underscores with dashes
  name=$(echo "$name" | tr '_' '-')
  # Remove characters not allowed
  name=$(echo "$name" | sed -e 's/[^a-z0-9-]//g')
  # Trim to 63 characters max (to comply with bucket name length limit)
  name=$(echo "$name" | cut -c 1-63)
  echo "$name"
}