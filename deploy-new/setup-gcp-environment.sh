#!/bin/bash

# Please make sure you have enable billing for your project
# Please make sure you enable Service Usage API https://console.cloud.google.com/project/_/apis/library/serviceusage.googleapis.com
# Before running this script

# Define required environment variables for this script
required_vars=("GCP_PROJECT_ID" "GCP_REGION" "AR_LOCATION" "GCP_DNS_ZONE_NAME" "GCP_BUCKET_LOCATION" "SERVICE_ACCOUNT_NAME")

# Set Path
SCRIPT_DIR="$(realpath $(dirname $0))"

# Export all functions
source "$SCRIPT_DIR/functions.sh"

# Check and Set environment variables
check_required_vars "${required_vars[@]}"
read_env


# Section 1: Setup gcloud CLI using Service Account Key
show_section_header "Setting up gcloud CLI permissions using Service Account..."
show_loading "Configuring gcloud CLI with Service Account"
gcloud auth activate-service-account $SERVICE_ACCOUNT_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com \
    --key-file="$SCRIPT_DIR/$SERVICE_ACCOUNT_NAME.json" \
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

# Get Project Number
show_loading "Get GCP Project number"
PROJECT_NUMBER=$(gcloud projects describe $GCP_PROJECT_ID --format="value(projectNumber)")
if [ $? -ne 0 ]; then
  print_error "Retrieving project number" "Failed"
  exit 1
fi
print_success "Project number: $PROJECT_NUMBER" "Retrieved"


# Section 3: Create an Artifact Registry repository
show_section_header "Creating Artifact Registry repository..."
show_loading "Creating repository"
if ! gcloud artifacts repositories describe $SERVICE_NAME-repo --location=$AR_LOCATION > /dev/null 2>&1; then
    gcloud artifacts repositories create $SERVICE_NAME-repo \
        --repository-format=docker \
        --location=$AR_LOCATION \
        --description="DESCRIPTION" \
        --async
    if [ $? -ne 0 ]; then
        print_error "$SERVICE_NAME-repo repository creation" "Failed"
        exit 1
    else
        print_success "$SERVICE_NAME-repo repository" "Created"
    fi
else
    print_warning "$SERVICE_NAME-repo repository already exists" "Skipped"
fi

# Section 4: GCS Bucket Creation
show_section_header "Creating Cloud Storage bucket..."
show_loading "Creating bucket"
if ! gcloud storage buckets describe gs://$SERVICE_NAME-$PROJECT_NUMBER-bucket --format="json(name)" > /dev/null 2>&1; then
    gcloud storage buckets create gs://$SERVICE_NAME-$PROJECT_NUMBER-bucket \
        --project=$GCP_PROJECT_ID \
        --default-storage-class=standard \
        --location=$GCP_BUCKET_LOCATION

    if [ $? -ne 0 ]; then
        print_error "gs://$SERVICE_NAME-$PROJECT_NUMBER-bucket creation" "Failed"
    else
        print_success "gs://$SERVICE_NAME-$PROJECT_NUMBER-bucket bucket" "Created"
    fi
else
    print_warning "gs://$SERVICE_NAME-$PROJECT_NUMBER-bucket bucket already exists" "Skipped"
fi

Section 5: Cloud SQL for MySQL instance creation
show_section_header "Creating Cloud SQL for MySQL instance..."
show_loading "Creating MySQL instance"
if ! gcloud sql instances describe $SERVICE_NAME-mysql > /dev/null 2>&1; then
    gcloud sql instances create $SERVICE_NAME-mysql \
        --database-version=MYSQL_8_0 \
        --cpu=2 \
        --memory=3840MB \
        --region=$GCP_REGION \
        --availability-type=ZONAL

    if [ $? -ne 0 ]; then
        print_error "$SERVICE_NAME-mysql instance creation" "Failed"
    else
        print_success "$SERVICE_NAME-mysql instance" "Created"
    fi
else
    print_warning "$SERVICE_NAME-mysql instance already exists" "Skipped"
fi

echo -e "\nGoogle Cloud environment setup completed successfully.\n"
