#!/bin/bash

# Get the list of all secrets
secrets=$(gcloud secrets list --format="value(name)")

if [ -z "$secrets" ]; then
  echo "No secrets found."
  exit 0
fi

# Iterate over each secret and delete it
for secret in $secrets; do
  echo "Deleting secret: $secret"
  gcloud secrets delete "$secret" --quiet
done

echo "All secrets purged."
