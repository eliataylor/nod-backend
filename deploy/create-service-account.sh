# Set your variables
SERVICE_ACCOUNT_NAME="djremoter"
PROJECT_ID="instant-jetty-426808-u5"
KEY_FILE_PATH="deploy/djremoter.json"

# Authenticate with Google Cloud
gcloud auth login
gcloud config set project $PROJECT_ID

# Create the service account
gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
    --description="Service account for deploying to Cloud Run and accessing Cloud Storage" \
    --display-name="Service Account for Cloud Run"

# Assign roles to the service account
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/cloudsql.client"

# Create and download the service account key
gcloud iam service-accounts keys create $KEY_FILE_PATH \
    --iam-account=$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com
