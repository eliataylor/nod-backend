#!/bin/bash

# Define required environment variables for this script
required_vars=("GCP_SERVICE_NAME" "GCP_PROJECT_ID", "GCP_SA_KEY_PATH", "DOMAIN_NAME")

# Set Path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Validate environment variables or exit
source "$SCRIPT_DIR/common.sh"

# login manually
gcloud auth login


# Set Default GCP Project
gcloud config set project $GCP_PROJECT_ID

ROLES=(
    "roles/artifactregistry.admin"
    "roles/iam.serviceAccountUser"
    "roles/run.developer"
    "roles/cloudbuild.builds.builder"
    "roles/cloudsql.client"
    "roles/run.admin"
    "roles/secretmanager.secretAccessor"
    "roles/storage.objectCreator"
    "roles/storage.objectViewer"
)

# Create the service account
SERVICE_ACCOUNT_EXISTS=$(gcloud iam service-accounts list --filter="email:$SERVICE_ACCOUNT_EMAIL" --format="value(email)")

if [ -z "$SERVICE_ACCOUNT_EXISTS" ]; then
    echo "Creating service account: $SERVICE_ACCOUNT_NAME"
    gcloud iam service-accounts create "$SERVICE_ACCOUNT_ID" \
        --description="Service account for $DOMAIN_NAME deployment to Cloud Run and accessing Cloud Storage" \
        --display-name "$SERVICE_ACCOUNT_NAME"
else
    echo "Service account $SERVICE_ACCOUNT_NAME already exists."
fi


for ROLE in "${ROLES[@]}"; do
    gcloud projects add-iam-policy-binding "$GCP_PROJECT_ID" \
        --member "serviceAccount:$SERVICE_ACCOUNT_ID@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
        --role "$ROLE"
done


# CLOUD_RUN_SERVICE_NAME="my-cloud-run-service"
# echo "Assigning Cloud Run Developer role to $CLOUD_RUN_SERVICE_NAME"
# gcloud run services add-iam-policy-binding "$CLOUD_RUN_SERVICE_NAME" \
#    --member "serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
#    --role "roles/run.developer"

# Create and download the service account key
gcloud iam service-accounts keys create $GCP_SA_KEY_PATH \
    --iam-account=$SERVICE_ACCOUNT_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com
