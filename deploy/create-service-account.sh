#!/bin/bash

# Define required environment variables for this script
required_vars=("GCP_SERVICE_NAME" "GCP_PROJECT_ID", "GCP_SA_KEY_PATH")

# Set Path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Validate environment variables or exit
source "$SCRIPT_DIR/common.sh"

# login manually
gcloud auth login


# Set Default GCP Project
gcloud config set project $GCP_PROJECT_ID

# Create the service account
gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
    --description="Service account for deploying to Cloud Run and accessing Cloud Storage" \
    --display-name="Service Account for Cloud Run"

# Assign roles to the service account
gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/cloudsql.client"

# Create and download the service account key
gcloud iam service-accounts keys create $GCP_SA_KEY_PATH \
    --iam-account=$SERVICE_ACCOUNT_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com
