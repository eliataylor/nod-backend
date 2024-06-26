#!/bin/bash

# Define required environment variables for this script
required_vars=("GCP_PROJECT_ID" "GCP_REGION" "AR_REPO_NAME" "AR_LOCATION"
"DJANGO_ENV" "GCP_PROJECT_ID" "DJANGO_ALLOWED_HOSTS" "DJANGO_CSRF_TRUSTED_ORIGINS"
"DJANGO_SECRET_KEY" "DJANGO_SUPERUSER_USERNAME" "DJANGO_SUPERUSER_PASSWORD" "DJANGO_SUPERUSER_EMAIL" "MYSQL_HOST" "MYSQL_DATABASE" "MYSQL_USER" "MYSQL_PASSWORD"
)

# Set Path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Validate environment variables or exit
source "$SCRIPT_DIR/common.sh"

# Setup gcloud CLI using Service Account Key

# Configure necessary permissions required by the application
# Get Project Number
PROJECT_NUMBER=$(gcloud projects describe $GCP_PROJECT_ID --format="value(projectNumber)" 2>/dev/null)
GCP_BUCKET_NAME=$PROGRAM_NAME-$PROJECT_NUMBER-bucket

if [ -z "$PROJECT_NUMBER" ]; then
  # gcloud auth login --cred-file=$GCP_SA_KEY_PATH
  gcloud auth login
  PROJECT_NUMBER=$(gcloud projects describe $GCP_PROJECT_ID --format="value(projectNumber)" 2>/dev/null)
fi

# CLOUD_RUN_SERVICE_NAME="my-cloud-run-service"
# echo "You may need to assign the Cloud Run Developer role to your cloud run service ?"
# gcloud run services add-iam-policy-binding "$CLOUD_RUN_SERVICE_NAME" \
#    --member "serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
#    --role "roles/run.developer"

# Define your arrays of environment variable and secret names
env_vars=("DJANGO_ENV" "GCP_PROJECT_ID" "GCP_BUCKET_NAME" "DJANGO_ALLOWED_HOSTS" "DJANGO_CSRF_TRUSTED_ORIGINS")
secret_vars=("DJANGO_SECRET_KEY" "DJANGO_SUPERUSER_USERNAME" "DJANGO_SUPERUSER_PASSWORD" "DJANGO_SUPERUSER_EMAIL" "MYSQL_HOST" "MYSQL_DATABASE" "MYSQL_USER" "MYSQL_PASSWORD")

# Construct the --set-env-vars argument
env_arg=""
delimiter=","
for var in "${env_vars[@]}"; do
  value="${!var}"
  encoded_value=$(urlencode "$value")
  if [ -n "$env_arg" ]; then
    env_arg+="$delimiter"
  fi
  env_arg+="$var=$encoded_value"
#  echo "Env Var: $var=$encoded_value"  # Debug print
done

# Construct the --set-secrets argument
secret_arg=""
delimiter=","
for var in "${secret_vars[@]}"; do
  secret_value="$var:latest"
#  secret_value="projects/$GCP_PROJECT_ID/secrets/$var:latest"
  if [ -n "$secret_arg" ]; then
    secret_arg+="$delimiter"
  fi
  secret_arg+="$var=$secret_value"
#  echo "Secret Var: $var=$secret_value"  # Debug print
done

echo "\n\n$secret_arg"
echo "\n\n$env_arg"

# Deploy to Cloud Run
echo "Deploying project number - $PROJECT_NUMBER - container to Cloud Run..."


gcloud run deploy $PROGRAM_NAME \
    --image $AR_LOCATION-docker.pkg.dev/$GCP_PROJECT_ID/$AR_REPO_NAME/$PROGRAM_NAME \
    --region $GCP_REGION \
    --port 8000 \
    --allow-unauthenticated \
    --min-instances 1 \
    --add-cloudsql-instances=$CLOUD_SQL_CONN \
    --set-env-vars "$env_arg" \
    --set-secrets "$secret_arg"

echo -e "\nBuild and Deploy to Cloud Run completed."