#!/bin/bash

# Define required environment variables for this script
required_vars=("GCP_PROJECT_ID" "GCP_REGION" "GCP_DOCKER_REPO_ZONE" "GCP_SERVICE_NAME" "SERVICE_NAME")

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

# Get Project Number
show_loading "Get GCP Project number"
PROJECT_NUMBER=$(gcloud projects describe $GCP_PROJECT_ID --format="value(projectNumber)")
if [ $? -ne 0 ]; then
  print_error "Retrieving project number" "Failed"
  exit 1
fi
print_success "Project number: $PROJECT_NUMBER" "Retrieved"

# Create secret in Secret Manager
show_section_header "Create secrets for Application..."
create_secret "MYSQL_HOST" "/cloudsql/$GCP_MYSQL_PROJECT_ID:$MYSQL_REGION:$MYSQL_INSTANCE"
create_secret "MYSQL_DATABASE" "$MYSQL_DATABASE"
create_secret "MYSQL_USER" "$MYSQL_USER"
create_secret "MYSQL_PASSWORD" "$MYSQL_PASSWORD"