#!/bin/bash

# Define required environment variables for this script
required_vars=("GCP_PROJECT_ID" "SERVICE_ACCOUNT_NAME")

# Set Path
SCRIPT_DIR="$(realpath $(dirname $0))"

# Export all functions
source "$SCRIPT_DIR/functions.sh"

# Check and Set environment variables
check_required_vars "${required_vars[@]}"
read_env

# Set your variables
KEY_FILE_PATH="$SCRIPT_DIR/$SERVICE_ACCOUNT_NAME.json"

# Authenticate with Google Cloud
show_section_header "Setting up gcloud CLI permissions using your own account..."
show_loading "Configuring gcloud CLI with your own account..."
gcloud auth login
if [ $? -ne 0 ]; then
    print_error "Configure gcloud CLI with Service Account" "Failed"
    exit 1
else
    print_success "Configure gcloud CLI with Service Account" "Success"
fi

show_loading "Setting GCP Poject..."
gcloud config set project $GCP_PROJECT_ID
if [ $? -ne 0 ]; then
    print_error "Setting GCP Project" "Failed"
    exit 1
else
    print_success "Setting GCP Project" "Success"
fi

show_loading "Enable required IAM API..."
gcloud services enable iam.googleapis.com
if [ $? -ne 0 ]; then
    print_error "Enabling IAM API" "Failed"
    exit 1
else
    print_success "Enabling IAM API" "Success"
fi


# Add necessary IAM permissions for service account
show_section_header "Setup service account and permissions..."
show_loading "Creating service account..."
if ! gcloud iam service-accounts describe $SERVICE_ACCOUNT_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com > /dev/null 2>&1; then
    gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
    --description="Service account for automatic deployment to google cloud" \
    --display-name="$SERVICE_ACCOUNT_NAME"
    if [ $? -ne 0 ]; then
        print_error "Service account creation" "Failed"
    else
        print_success "Service account creation" "Success"
    fi
else
    print_warning "$SERVICE_ACCOUNT_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com already exists" "Skipped"
fi

show_loading "Add necessary IAM permissions for service account..."
roles=(
    "roles/viewer"
    "roles/artifactregistry.admin"
    "roles/cloudbuild.builds.builder"
    "roles/run.admin"
    "roles/cloudsql.admin"
    "roles/compute.instanceAdmin.v1"
    "roles/compute.networkAdmin"
    "roles/compute.securityAdmin"
    "roles/dns.admin"
    "roles/secretmanager.admin"
    "roles/iam.serviceAccountUser"
    "roles/serviceusage.serviceUsageAdmin"
    "roles/storage.admin"
)
for role in "${roles[@]}"; do
    if [[ $(gcloud projects get-iam-policy $GCP_PROJECT_ID --flatten="bindings[].members" --format='table(bindings.role)' --filter="bindings.members:$SERVICE_ACCOUNT_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com AND bindings.role:$role") == ROLE* ]]; then
        print_warning "$role role already exists" "Skipped"
    else
        gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
        --member="serviceAccount:$SERVICE_ACCOUNT_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
        --role="$role" \
        --quiet
        if [ $? -ne 0 ]; then
            print_error "$role added to Service Account" "Failed"
        else
            print_success "$role added to Service Account" "Success"
        fi
    fi
done


# Create and download the service account key
show_loading "Create and download the service account key..."
gcloud iam service-accounts keys create $KEY_FILE_PATH \
    --iam-account=$SERVICE_ACCOUNT_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com
if [ $? -ne 0 ]; then
    print_error "Service account key creation" "Failed"
else
    print_success "Service account key creation" "Success"
fi