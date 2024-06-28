#!/bin/bash

# Source the functions.sh file to load the functions
source "$SCRIPT_DIR/functions.sh"

# Set Path
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

# Initialize an associative array to track which required variables are found
declare -A found_vars
for var in "${required_vars[@]}"; do
  found_vars["$var"]=0
done

# Path to the .env file
env_file="$PARENT_DIR/.env"

# Read the .env file to check for required variables, adding a newline to ensure the last line is read
while IFS= read -r line; do
  # Skip empty lines and lines starting with #
  [[ -z "$line" || "$line" == \#* ]] && continue

  # Extract the variable name from the line
  var_name=$(echo "$line" | cut -d '=' -f 1)

  # Check if the variable is in the required list
  if [[ " ${required_vars[*]} " == *" $var_name "* ]]; then
    found_vars["$var_name"]=1
  fi
done < <(cat "$env_file"; echo)

# Check if any required variables are missing
missing_vars=()
for var in "${required_vars[@]}"; do
  if [[ ${found_vars["$var"]} -eq 0 ]]; then
    missing_vars+=("$var")
  fi
done

# Output the result and exit if any required variables are missing
if [[ ${#missing_vars[@]} -ne 0 ]]; then
  echo "The following required variables are missing in $env_file:"
  for var in "${missing_vars[@]}"; do
    echo "$var"
  done
  exit 1
fi

# If all required variables are present, export all variables from the .env file, adding a newline to ensure the last line is read
while IFS= read -r line; do
  # Skip empty lines and lines starting with #
  [[ -z "$line" || "$line" == \#* ]] && continue

  # Validate that the line contains an equal sign and has a non-empty variable name
  if [[ "$line" == *=* ]]; then
    var_name=$(echo "$line" | cut -d '=' -f 1)
    var_value=$(echo "$line" | cut -d '=' -f 2-)

    # Export the variable to the environment only if var_name is not empty
    if [[ -n "$var_name" ]]; then
      export "$var_name=$var_value"
    fi
  fi
done < <(cat "$env_file"; echo)

echo "All required variables are present in $env_file and have been exported to the environment."