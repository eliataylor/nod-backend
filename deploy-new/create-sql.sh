#!/bin/bash

# Please make sure you have enable billing for your project
# Please make sure you enable Service Usage API https://console.cloud.google.com/project/_/apis/library/serviceusage.googleapis.com
# Before running this script

# Define required environment variables for this script
required_vars=("GCP_PROJECT_ID" "GCP_REGION" "GCP_DOCKER_REPO_ZONE" "GCP_DNS_ZONE_NAME" "GCP_BUCKET_API_ZONE" "GCP_BUCKET_API_NAME" "GCP_SERVICE_NAME" "MYSQL_PASSWORD" "MYSQL_DATABASE" "MYSQL_USER" "MYSQL_HOST" "MYSQL_INSTANCE" "MYSQL_ZONE")

# Set Path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Validate environment variables or exit
source "$SCRIPT_DIR/common.sh"

CURRENT_USER=$(gcloud config get-value account)
REQUIRED_ROLE="roles/owner"

show_section_header "Check if the user has the required role $REQUIRED_ROLE"
ROLE_EXISTS=$(gcloud projects get-iam-policy $GCP_PROJECT_ID --format=json | jq -e --arg role "$REQUIRED_ROLE" --arg user "$CURRENT_USER" '
    .bindings[] | select(.role == $role) | .members[] | select(. == "user:" + $user)
' > /dev/null 2>&1)

if [ $? -ne 0 ]; then
    print_warning "The current user does not have the required role. Please login."
    gcloud auth login
    if [ $? -ne 0 ]; then
      print_error "Configure gcloud CLI with Service Account" "Failed"
      exit 1
    fi

else
    print_success "The current user has the required role $REQUIRED_ROLE."
fi

print_success "Configure gcloud CLI with Service Account" "Success"

PROJECT_IDS=$(gcloud projects list --format="value(projectId)")
show_section_header "Search all projects for SQL instance $MYSQL_INSTANCE... across $PROJECT_IDS"

INSTANCE_EXISTS=false
for PROJECT_ID in $PROJECT_IDS; do
    if gcloud sql instances describe $MYSQL_INSTANCE --project=$PROJECT_ID --format="json(name)" > /dev/null 2>&1; then
        print_success "\nSQL instance $MYSQL_INSTANCE exists in project $PROJECT_ID"
        INSTANCE_EXISTS=true
        break
    else
      print_warning "$PROJECT_ID does not have SQL instance $MYSQL_INSTANCE"
    fi
done

if [ "$INSTANCE_EXISTS" = false ]; then
    show_section_header "Creating Cloud SQL for MySQL instance $MYSQL_INSTANCE..."
    gcloud sql instances create $MYSQL_INSTANCE \
        --database-version=MYSQL_8_0 \
        --tier=db-f1-micro \
        --region=$MYSQL_REGION \
        --availability-type=ZONAL
    if [ $? -ne 0 ]; then
        print_error "mysql $MYSQL_INSTANCE instance creation" "Failed"
    else
        print_success "mysql $MYSQL_INSTANCE instance" "Created"
    fi
else
    print_warning "mysql $MYSQL_INSTANCE instance already exists" "Skipped"
fi

# Section 5: Cloud SQL for MySQL instance creation
echo -e "\nGoogle Cloud environment setup completed successfully.\n"




# Section 2: Setup necessary permissions
# Setup MySQL databsase
show_section_header "Setup Cloud SQL for MySQL database..."
show_loading "Creating MySQL database..."
if ! gcloud sql databases describe $MYSQL_DATABASE --instance=$MYSQL_INSTANCE > /dev/null 2>&1; then
    gcloud sql databases create $MYSQL_DATABASE \
        --instance=$MYSQL_INSTANCE
    if [ $? -ne 0 ]; then
        print_error "$MYSQL_DATABASE database creation" "Failed"
    else
        # Set root password
        show_loading "Creating root password..."
        gcloud sql users set-password root \
            --host=% \
            --instance=$MYSQL_INSTANCE \
            --password=$MYSQL_ROOT_PASSWORD
        if [ $? -ne 0 ]; then
            print_error "$MYSQL_INSTANCE set root password" "Failed"
        else
            print_success "$MYSQL_INSTANCE set root password" "Success"
        fi
    fi
else
    print_warning "$MYSQL_DATABASE database already exists" "Skipped"
fi

# Setup MySQL user
show_loading "Creating MySQL user..."
if gcloud sql databases describe $MYSQL_DATABASE --instance=$MYSQL_INSTANCE && ! gcloud sql users describe $MYSQL_USER --instance=$MYSQL_INSTANCE > /dev/null 2>&1; then
    gcloud sql users create $MYSQL_USER \
        --host=% \
        --instance=$MYSQL_INSTANCE \
        --password=$MYSQL_PASSWORD
    if [ $? -ne 0 ]; then
        print_error "MySQL User creation" "Failed"
    else
        print_success "MySQL User creation" "Success"
    fi
else
    print_warning "MySQL User already exists" "Skipped"
fi
