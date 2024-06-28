#!/bin/bash

# Define required environment variables for this script
required_vars=("GCP_PROJECT_ID" "GCP_REGION" "GCP_DOCKER_REPO_ZONE" "GCP_SERVICE_NAME" "MYSQL_PASSWORD")

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


# Section 3: Building & submit containers
show_section_header "Building & submit containers..."   
show_loading "Authenticating Docker to Artifact Registry..."
gcloud auth configure-docker $GCP_DOCKER_REPO_ZONE-docker.pkg.dev
if [ $? -ne 0 ]; then
    print_error "Authenticating Docker" "Failed"
    exit 1
fi
print_success "Docker authenticated to Artifact Registry" "Success"

# Build container and submit to Artifact Registry repository
show_loading "Building container and submit to Artifact Registry..."
gcloud builds submit --dir=$PARENT_DIR/Dockerfile \
    --tag $GCP_DOCKER_REPO_ZONE-docker.pkg.dev/$GCP_PROJECT_ID/$GCP_DOCKER_REPO_NAME/$GCP_SERVICE_NAME:latest \
    --region $GCP_REGION
if [ $? -ne 0 ]; then
    print_error "Building & submitting container" "Failed"
    exit 1
fi
print_success "Building & submitting container" "Success"

# Section 4: Deploy to Cloud Run
show_section_header "Deploy container to Cloud Run"
show_loading "Deploying container to Cloud Run..."
gcloud run deploy $GCP_SERVICE_NAME \
    --image $GCP_DOCKER_REPO_ZONE-docker.pkg.dev/$GCP_PROJECT_ID/$GCP_DOCKER_REPO_NAME/$GCP_SERVICE_NAME:latest \
    --region $GCP_REGION \
    --service-account $GCP_SERVICE_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com \
    --port 8000 \
    --add-cloudsql-instances=$GCP_MYSQL_PROJECT_ID:$GCP_MYSQL_ZONE:$GCP_MYSQL_INSTANCE \
    --set-env-vars ^,^DJANGO_ENV=$DJANGO_ENV,GCP_PROJECT_ID=$GCP_PROJECT_ID,GCP_BUCKET_API_NAME=$GCP_BUCKET_API_NAME \
    --set-env-vars ^@^DJANGO_ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS@DJANGO_CSRF_TRUSTED_ORIGINS=$DJANGO_CSRF_TRUSTED_ORIGINS \
    --set-secrets ^,^DJANGO_SECRET_KEY=DJANGO_SECRET_KEY:latest,DJANGO_SUPERUSER_USERNAME=DJANGO_SUPERUSER_USERNAME:latest,DJANGO_SUPERUSER_PASSWORD=DJANGO_SUPERUSER_PASSWORD:latest,DJANGO_SUPERUSER_EMAIL=DJANGO_SUPERUSER_EMAIL:latest,MYSQL_HOST=MYSQL_HOST:latest,MYSQL_DATABASE=MYSQL_DATABASE:latest,MYSQL_USER=MYSQL_USER:latest,MYSQL_PASSWORD=MYSQL_PASSWORD:latest \
    --min-instances 1 \
    --allow-unauthenticated
if [ $? -ne 0 ]; then
    print_error "Deploying to Cloud Run" "Failed"
    exit 1
fi
print_success "Deploying to Cloud Run" "Success"

echo -e "\nBuild and Deploy to Cloud Run completed.\n"