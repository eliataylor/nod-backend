#!/bin/bash


# Find root .env
ENV_FILE="$1"

# Load variables from root .env
if [ -f "$ENV_FILE" ]; then
  # Remove entire lines that are comments
  env_content=$(grep -vE '^\s*#' "$ENV_FILE")

  # Strip inline comments
  env_content=$(echo "$env_content" | sed 's/[[:space:]]*#.*//')

  # Remove any 'export ' prefix
  env_content=$(echo "$env_content" | sed 's/^export //')

  # Remove = followed by a space and a double quote
  env_content=$(echo "$env_content" | sed 's/=\s*"//g')

  # Remove = followed by a space and a single quote
  env_content=$(echo "$env_content" | sed "s/=\s*'//g")

  # Remove a double quote at the end
  env_content=$(echo "$env_content" | sed 's/"$//')

  # Remove a single quote at the end
  env_content=$(echo "$env_content" | sed "s/'$//")

  # Export the variables
  export $(echo "$env_content" | xargs)
else
  echo ".env file not found at $ENV_FILE. Please create a .env file with the necessary variables."
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