#!/bin/bash

# Create and Generate Service Account Key, save it as 'sa_key.json' in the root folder with the following IAM Permissions:
# Artifact Registry Administrator
# Service Account User (roles/iam.serviceAccountUser)
# Cloud Run Developer (roles/run.developer) on the Cloud Run service
# Artifact Registry Administrator
# Cloud Build Service Account
# Cloud Run Admin
# Secret Manager Secret Accessor (roles/secretmanager.secretAccessor)
# Service Account User
# Storage Object Creator
# Storage Object Viewer
#
# You can also using your own user that has Owner/Editor permissions
# Comment `gcloud auth login --cred-file="$PARENT_DIR/sa_key.json"` command below
# Make sure you have already setup gcloud SDK (gcloud CLI) and login with your account
# Documentation : https://cloud.google.com/sdk/docs/authorizing

# Define required environment variables for this script
required_vars=("GCP_PROJECT_ID" "GCP_REGION" "AR_REPO_NAME" "AR_LOCATION")

# Set Path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Validate environment variables or exit
source "$SCRIPT_DIR/common.sh"

# Setup gcloud CLI using Service Account Key
# gcloud auth login --cred-file="$PARENT_DIR/keys/djremoter.json"
gcloud auth login

# Configure necessary permissions required by the application
# Get Project Number
PROJECT_NUMBER=$(gcloud projects describe $GCP_PROJECT_ID --format="value(projectNumber)" 2>/dev/null)

# CLOUD_RUN_SERVICE_NAME="my-cloud-run-service"
echo "You may need to assign the Cloud Run Developer role to your cloud run service?"
# gcloud run services add-iam-policy-binding "$CLOUD_RUN_SERVICE_NAME" \
#    --member "serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
#    --role "roles/run.developer"

# Deploy to Cloud Run
echo "Deploying container to Cloud Run..."
gcloud run deploy $PROGRAM_NAME \
    --image $AR_LOCATION-docker.pkg.dev/$GCP_PROJECT_ID/$AR_REPO_NAME/$PROGRAM_NAME \
    --region $GCP_REGION \
    --port 8000 \
    --allow-unauthenticated \
    --min-instances 1 \
    --add-cloudsql-instances=$CLOUD_SQL_CONN \
    --set-env-vars ^,^DJANGO_ENV=$DJANGO_ENV,GCP_PROJECT_ID=$GCP_PROJECT_ID,GCP_BUCKET_NAME=$PROGRAM_NAME-$PROJECT_NUMBER-bucket \
    --set-env-vars ^@^DJANGO_ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS@DJANGO_CSRF_TRUSTED_ORIGINS=$DJANGO_CSRF_TRUSTED_ORIGINS \
    --set-secrets ^,^DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY,DJANGO_SUPERUSER_USERNAME=$DJANGO_SUPERUSER_USERNAME,DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_USERNAME,DJANGO_SUPERUSER_EMAIL=$DJANGO_SUPERUSER_EMAIL,MYSQL_HOST=$MYSQL_HOST,MYSQL_DATABASE=$MYSQL_DATABASE,MYSQL_USER=$MYSQL_USER,MYSQL_PASSWORD=$MYSQL_PASSWORD
echo

echo -e "\nBuild and Deploy to Cloud Run completed."