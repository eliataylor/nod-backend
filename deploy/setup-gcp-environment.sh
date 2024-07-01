#!/bin/bash

# Please make sure you have enable billing for your project
# Please make sure you enable Service Usage API https://console.cloud.google.com/project/_/apis/library/serviceusage.googleapis.com
# Before running this script

# Define required environment variables for this script
required_vars=("GCP_PROJECT_ID" "GCP_REGION" "GCP_DOCKER_REPO_ZONE" "GCP_DOCKER_REPO_NAME" "GCP_DNS_ZONE_NAME" "GCP_BUCKET_API_ZONE" "GCP_BUCKET_API_NAME" "GCP_SERVICE_NAME")

# Set Path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Validate environment variables or exit
source "$SCRIPT_DIR/common.sh"


# Section 1: Setup gcloud CLI using Service Account Key
show_section_header "Setting up gcloud CLI permissions using Service Account..."
show_loading "Configuring gcloud CLI with Service Account"
gcloud auth activate-service-account $GCP_SERVICE_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com \
    --key-file=$GCP_SA_KEY_PATH \
    --project=$GCP_PROJECT_ID

if [ $? -ne 0 ]; then
    print_error "Configure gcloud CLI with Service Account" "Failed"
    exit 1
fi
print_success "Configure gcloud CLI with Service Account" "Success"


# Section 2: Enable necessary Google Cloud APIs
show_section_header "Enabling necessary Google Cloud APIs..."
show_loading "Enabling Google Cloud APIs"
apis=(
    "cloudresourcemanager.googleapis.com"
    "artifactregistry.googleapis.com"
    "cloudbuild.googleapis.com"
    "run.googleapis.com"
    "secretmanager.googleapis.com"
    "sqladmin.googleapis.com"
    "sql-component.googleapis.com"
    "compute.googleapis.com"
    "dns.googleapis.com"
)
for api in "${apis[@]}"; do
    gcloud services enable "$api"
    if [ $? -ne 0 ]; then
        print_error "$api" "Failed"
    else
        print_success "$api" "Enabled"
    fi
done
echo

# Section 3: Create an Artifact Registry repository
show_section_header "Creating Artifact Registry repository..."
show_loading "Creating repository"
if ! gcloud artifacts repositories describe $GCP_DOCKER_REPO_NAME --location=$GCP_DOCKER_REPO_ZONE > /dev/null 2>&1; then
    gcloud artifacts repositories create $GCP_DOCKER_REPO_NAME \
        --repository-format=docker \
        --location="$GCP_DOCKER_REPO_ZONE" \
        --description="DESCRIPTION" \
        --async
    if [ $? -ne 0 ]; then
        print_error "$GCP_DOCKER_REPO_NAME repository creation" "Failed"
        exit 1
    else
        print_success "$GCP_DOCKER_REPO_NAME repository" "Created"
    fi
else
    print_warning "$GCP_DOCKER_REPO_NAME repository already exists" "Skipped"
fi


# Section 4: GCS Bucket Creation
show_section_header "Creating Cloud Storage bucket..."
show_loading "Creating bucket"
if ! gcloud storage buckets describe gs://$GCP_BUCKET_API_NAME --format="json(name)" > /dev/null 2>&1; then
    gcloud storage buckets create gs://$GCP_BUCKET_API_NAME \
        --project=$GCP_PROJECT_ID \
        --default-storage-class=standard \
        --location=$GCP_BUCKET_API_ZONE

    if [ $? -ne 0 ]; then
        print_error "gs://$GCP_BUCKET_API_NAME creation" "Failed"
    else
        print_success "gs://$GCP_BUCKET_API_NAME bucket" "Created"
    fi
else
    print_warning "gs://$GCP_BUCKET_API_NAME bucket already exists" "Skipped"
fi