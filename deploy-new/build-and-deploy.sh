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
required_vars=("GCP_PROJECT_ID" "GCP_REGION" "AR_LOCATION" "SERVICE_ACCOUNT_NAME" "SERVICE_NAME")

# Set Path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Validate environment variables or exit
source "$SCRIPT_DIR/common.sh"

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

# Get Project Number
show_loading "Get GCP Project number"
PROJECT_NUMBER=$(gcloud projects describe $GCP_PROJECT_ID --format="value(projectNumber)")
if [ $? -ne 0 ]; then
  print_error "Retrieving project number" "Failed"
  exit 1
fi
print_success "Project number: $PROJECT_NUMBER" "Retrieved"


# Section 2: Setup necessary permissions
# Setup MySQL databsase
show_section_header "Setup Cloud SQL for MySQL database..."   
show_loading "Creating MySQL database..."
if ! gcloud sql databases describe $SERVICE_NAME-$PROJECT_NUMBER-db --instance=$SERVICE_NAME-$PROJECT_NUMBER-mysql > /dev/null 2>&1; then
    gcloud sql databases create $SERVICE_NAME-$PROJECT_NUMBER-db \
        --instance=$SERVICE_NAME-$PROJECT_NUMBER-mysql
    if [ $? -ne 0 ]; then
        print_error "$SERVICE_NAME-$PROJECT_NUMBER-db database creation" "Failed"
    else
        # Set root password
        show_loading "Creating root password..."
        gcloud sql users set-password root \
            --host=% \
            --instance=$SERVICE_NAME-$PROJECT_NUMBER-mysql \
            --password=$MYSQL_ROOT_PASSWORD
        if [ $? -ne 0 ]; then
            print_error "$SERVICE_NAME-$PROJECT_NUMBER-mysql set root password" "Failed"
        else
            print_success "$SERVICE_NAME-$PROJECT_NUMBER-mysql set root password" "Success"
        fi
    fi
else
    print_warning "$SERVICE_NAME-$PROJECT_NUMBER-db database already exists" "Skipped"
fi

# Setup MySQL user
show_loading "Creating MySQL user..."
if gcloud sql databases describe $SERVICE_NAME-$PROJECT_NUMBER-db --instance=$SERVICE_NAME-$PROJECT_NUMBER-mysql && ! gcloud sql users describe $SERVICE_NAME-$PROJECT_NUMBER-db-user --instance=$SERVICE_NAME-$PROJECT_NUMBER-mysql > /dev/null 2>&1; then
    gcloud sql users create $SERVICE_NAME-$PROJECT_NUMBER-db-user \
        --host=% \
        --instance=$SERVICE_NAME-$PROJECT_NUMBER-mysql \
        --password=$MYSQL_USER_PASSWORD
    if [ $? -ne 0 ]; then
        print_error "MySQL User creation" "Failed"
    else
        print_success "MySQL User creation" "Success"
    fi
else
    print_warning "MySQL User already exists" "Skipped"
fi


# Create secret in Secret Manager
show_section_header "Create secrets for Application..." 
create_secret "MYSQL_HOST" "/cloudsql/$GCP_PROJECT_ID:$GCP_REGION:$SERVICE_NAME-$PROJECT_NUMBER-mysql"
create_secret "MYSQL_DATABASE" "$SERVICE_NAME-$PROJECT_NUMBER-db"
create_secret "MYSQL_USER" "$SERVICE_NAME-$PROJECT_NUMBER-db-user"
create_secret "MYSQL_PASSWORD" "$MYSQL_USER_PASSWORD"

show_loading "Importing all secrets to Secret Manager..."
import_secret_env "$SCRIPT_DIR/.django.secrets"

# Section 3: Building & submit containers
show_section_header "Building & submit containers..."   
show_loading "Authenticating Docker to Artifact Registry..."
gcloud auth configure-docker $AR_LOCATION-docker.pkg.dev
if [ $? -ne 0 ]; then
    print_error "Authenticating Docker" "Failed"
    exit 1
fi
print_success "Docker authenticated to Artifact Registry" "Success"

# Build container and submit to Artifact Registry repository
show_loading "Building container and submit to Artifact Registry..."
gcloud builds submit --dir=$PARENT_DIR/Dockerfile \
    --tag $AR_LOCATION-docker.pkg.dev/$GCP_PROJECT_ID/$SERVICE_NAME-$PROJECT_NUMBER-repo/$SERVICE_NAME:latest \
    --region $GCP_REGION
if [ $? -ne 0 ]; then
    print_error "Building & submitting container" "Failed"
    exit 1
fi
print_success "Building & submitting container" "Success"

# Section 4: Deploy to Cloud Run
show_section_header "Deploy container to Cloud Run"
show_loading "Deploying container to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $AR_LOCATION-docker.pkg.dev/$GCP_PROJECT_ID/$SERVICE_NAME-$PROJECT_NUMBER-repo/$SERVICE_NAME:latest \
    --region $GCP_REGION \
    --service-account $SERVICE_ACCOUNT_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com \
    --port 8000 \
    --add-cloudsql-instances=$GCP_PROJECT_ID:$GCP_REGION:$SERVICE_NAME-$PROJECT_NUMBER-mysql \
    --set-env-vars ^,^DJANGO_ENV=$DJANGO_ENV,GCP_PROJECT_ID=$GCP_PROJECT_ID,GCP_BUCKET_NAME=$SERVICE_NAME-$PROJECT_NUMBER-bucket \
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