#!/bin/bash

# Define required environment variables for this script
required_vars=("GCP_PROJECT_ID" "GCP_REGION" "GCP_SERVICE_NAME")

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

# Create secret in Secret Manager
show_section_header "Create secrets for Application..."


variable_names=("GCP_PROJECT_ID" \
 "GCP_REGION" \
\
 "GCP_DOCKER_REPO_ZONE" \
 "GCP_DOCKER_REPO_NAME" \
\
 "GCP_DNS_ZONE_NAME" \
 "DOMAIN_NAME" \
\
 "GCP_BUCKET_API_ZONE" \
 "GCP_BUCKET_API_NAME" \
 "GCP_BUCKET_APP_ZONE" \
 "GCP_BUCKET_APP_NAME" \
\
 "GCP_SERVICE_NAME" \
\
 "MYSQL_DATABASE" \
 "MYSQL_USER" \
 "MYSQL_PASSWORD" \
 "GCP_MYSQL_HOST" \
 "GCP_MYSQL_INSTANCE" \
 "GCP_MYSQL_ZONE" \

 "DJANGO_SECRET_KEY" \
 "DJANGO_SUPERUSER_USERNAME" \
 "DJANGO_SUPERUSER_PASSWORD" \
 "DJANGO_SUPERUSER_EMAIL" \
 "DJANGO_ALLOWED_HOSTS" \
 "DJANGO_CSRF_TRUSTED_ORIGINS" \

 "SMTP_PASSWORD" \
 "SMTP_EMAIL_ADDRESS" \

 "GOOGLE_OAUTH_SECRET" \
 "GOOGLE_OAUTH_CLIENT_ID"
 )

for var_name in "${variable_names[@]}"; do
    # Get the value of the variable (replace with your actual value retrieval method)
    var_value="${!var_name}"

    # Call the function to create secret
    create_secret "$var_name" "$var_value"
done