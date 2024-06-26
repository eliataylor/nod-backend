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
required_vars=("GCP_PROJECT_ID" "GCP_REGION" "AR_REPO_NAME" "AR_LOCATION" "SERVICE_NAME")

# Set Path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Validate environment variables or exit
source "$SCRIPT_DIR/common.sh"

# Setup gcloud CLI using Service Account Key
# echo "Setup gcloud CLI permissions using SA..."
# gcloud auth login --cred-file="$PARENT_DIR/keys/djremoter.json"
gcloud auth login

# echo


# Configure necessary permissions required by the application
# Get Project Number
PROJECT_NUMBER=$(gcloud projects describe $GCP_PROJECT_ID --format="value(projectNumber)" 2>/dev/null)

# Create GCS Bucket
echo "Creating GCS bucket..."
if ! gcloud storage buckets describe gs://$SERVICE_NAME-$PROJECT_NUMBER-bucket --format="json(name)" > /dev/null 2>&1; then
    # Create GCS Bucket
    gcloud storage buckets create gs://$SERVICE_NAME-$PROJECT_NUMBER-bucket \
        --project=$GCP_PROJECT_ID \
        --default-storage-class=standard \
        --location='us'
else
  echo -e "\e[31m$SERVICE_NAME-$PROJECT_NUMBER-bucket already exists. Skipping creation.\e[0m"
fi

# Create Cloud SQL for MySQL Database
# echo "Creating Cloud SQL for MySQL instance..."
# if ! gcloud sql instances describe $SERVICE_NAME-$PROJECT_NUMBER-mysql > /dev/null 2>&1; then
#     gcloud sql instances create $SERVICE_NAME-$PROJECT_NUMBER-mysql \
#         --database-version=MYSQL_8_0 \
#         --cpu=2 \
#         --memory=3840MB \
#         --region=$GCP_REGION
# else
#   echo -e "\e[31m$SERVICE_NAME-$PROJECT_NUMBER-mysql already exists. Skipping creation.\e[0m"
# fi

# Set Secret Manager Secret Accessor to access Secrets
gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
    --member="serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"

# Set Cloud SQL Client to connect to Cloud SQL
gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
    --member="serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
    --role="roles/cloudsql.client"

# Set Cloud Storage Admin access to specific GCS bucket used for this application
gcloud storage buckets add-iam-policy-binding \
    gs://$SERVICE_NAME-$PROJECT_NUMBER-bucket \
    --member="serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
    --role="roles/storage.admin"


# Building Containers
# Create an Artifact Registry repository
echo "Create an Artifact Registry repository..."
if ! gcloud artifacts repositories describe $AR_REPO_NAME > /dev/null 2>&1; then
    gcloud artifacts repositories create $AR_REPO_NAME \
        --repository-format=docker \
        --location=$AR_LOCATION \
        --description="DESCRIPTION" \
        --immutable-tags \
        --async
else
    echo -e "\e[31mArtifact Registry repository $AR_REPO_NAME already exists. Skipping creation.\e[0m"
fi
echo

# Configure Docker to get access to Artifact Registry
echo "Authenticating Docker to Artifact Registry..."
gcloud auth configure-docker $AR_LOCATION-docker.pkg.dev
echo

# Build container and submit to Artifact Registry repository
echo "Building container and submit to Artifact Registry..."
gcloud builds submit . \
    --tag $AR_LOCATION-docker.pkg.dev/$GCP_PROJECT_ID/$AR_REPO_NAME/$SERVICE_NAME:latest \
    --region $GCP_REGION

# Update Django ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS (optional)
# gcloud run services update nod-django-app \
#     --region us-west1 \
#     --update-env-vars DJANGO_ALLOWED_HOSTS='nod-django-app-7z6iwfp5aa-uw.a.run.app' \
#     --update-env-vars DJANGO_CSRF_TRUSTED_ORIGINS='https://nod-django-app-7z6iwfp5aa-uw.a.run.app'

echo -e "\ Setup completed."