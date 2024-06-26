#!/bin/bash

# Create and Generate Service Account Key, save it as 'sa_key.json' in the root folder with the following IAM Permissions:
# Network Admin             # Create load balancer components
# Compute Security Admin    # Create Google-managed SSL certificates
# DNS Administrator         # To manage Cloud DNS
#
# You can also using your own user that has Owner/Editor permissions
# Comment `gcloud auth login --cred-file="$PARENT_DIR/sa_key.json"` command below
# Make sure you have already setup gcloud SDK (gcloud CLI) and login with your account
# Documentation : https://cloud.google.com/sdk/docs/authorizing

# Define required environment variables for this script
required_vars=("GCP_PROJECT_ID" "GCP_REGION" "AR_REPO_NAME" "AR_LOCATION" "SERVICE_NAME")

# Set Path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Validate environment variables or exit
source "$SCRIPT_DIR/common.sh"

# Setup gcloud CLI using Service Account Key
# echo "Setup gcloud CLI permissions using SA..."
# gcloud auth login --cred-file="$PARENT_DIR/sa_key.json" --quiet
# echo

# Set Default GCP Project
echo "Setting GCP project to $GCP_PROJECT_ID..."
gcloud config set project $GCP_PROJECT_ID
gcloud config set compute/region $GCP_REGION
echo

# Get Project Number
PROJECT_NUMBER=$(gcloud projects describe $GCP_PROJECT_ID --format="value(projectNumber)" 2>/dev/null)

# Reserve global static external IP address for Loadbalancer
echo "Reserving global static external IP address for Loadbalancer..."
if ! gcloud compute addresses describe $SERVICE_NAME-$PROJECT_NUMBER-ip --global > /dev/null 2>&1; then
    gcloud compute addresses create $SERVICE_NAME-$PROJECT_NUMBER-ip \
        --network-tier=PREMIUM \
        --ip-version=IPV4 \
        --global
else
  printf "\e[31mIP address $SERVICE_NAME-$PROJECT_NUMBER-ip already exists. Skipping creation.\e[0m"
fi

# Set the IP address as environment variable
echo "Fetching static IP address..."
STATIC_IP=$(gcloud compute addresses describe $SERVICE_NAME-$PROJECT_NUMBER-ip \
    --format="get(address)" \
    --global 2>/dev/null)
echo "Static IP: $STATIC_IP"
echo


# Create DNS zone if it doesn't exist
echo "Creating DNS zone..."
if ! gcloud dns managed-zones describe $GCP_DNS_ZONE_NAME > /dev/null 2>&1; then
    gcloud dns managed-zones create $GCP_DNS_ZONE_NAME --dns-name="$DOMAIN_NAME." --description="DNS zone for $DOMAIN_NAME"

    # Add a DNS record set for your domain, ww.domain, and dev.domain
    echo "Creating DNS record..."
    if ! gcloud dns record-sets describe $DOMAIN_NAME. --type=A --zone=$GCP_DNS_ZONE_NAME > /dev/null 2>&1; then
        gcloud dns record-sets create $DOMAIN_NAME. --zone="$GCP_DNS_ZONE_NAME" --type="A" --ttl="300" --rrdatas="$STATIC_IP"
    else
        printf "\e[31mDNS record $DOMAIN_NAME already exists. Skipping creation.\e[0m"
    fi
else
    printf "\e[31mDNS zone $GCP_DNS_ZONE_NAME already exists. Skipping creation.\e[0m"
fi
echo

# Create SSL Certificate for Loadbalancer
echo "Creating SSL certificate..."
if ! gcloud compute ssl-certificates describe $SERVICE_NAME-$PROJECT_NUMBER-ssl --global > /dev/null 2>&1; then
    gcloud compute ssl-certificates create $SERVICE_NAME-$PROJECT_NUMBER-ssl \
        --description="SSL Certificate for Loadbalancer" \
        --domains=$DOMAIN_NAME \
        --global
else
    printf "\e[31mSSL certificate $SERVICE_NAME-$PROJECT_NUMBER-ssl already exists. Skipping creation.\e[0m"
fi
echo


# Backend Service
# Create a serverless NEG
echo "Creating serverless NEG..."
if ! gcloud compute network-endpoint-groups describe $SERVICE_NAME-$PROJECT_NUMBER-neg > /dev/null 2>&1; then
    gcloud compute network-endpoint-groups create $SERVICE_NAME-$PROJECT_NUMBER-neg \
        --region=$GCP_REGION \
        --network-endpoint-type=serverless  \
        --cloud-run-service=$SERVICE_NAME
else
    printf "\e[31m$SERVICE_NAME-$PROJECT_NUMBER-neg already exists. Skipping creation.\e[0m"
fi
echo

# Create a backend service
echo "Creating a Backend Service..."
if ! gcloud compute backend-services describe $SERVICE_NAME-$PROJECT_NUMBER-bs > /dev/null 2>&1; then
    gcloud compute backend-services create $SERVICE_NAME-$PROJECT_NUMBER-bs \
        --load-balancing-scheme=EXTERNAL_MANAGED \
        --global
    echo
    
    # Add serverless NEG to the backend service
    echo "Add serverless NEG to the backend service..."
    gcloud compute backend-services add-backend $SERVICE_NAME-$PROJECT_NUMBER-bs \
        --global \
        --network-endpoint-group=$SERVICE_NAME-$PROJECT_NUMBER-neg \
        --network-endpoint-group-region=$GCP_REGION
else
    printf "\e[31m$SERVICE_NAME-$PROJECT_NUMBER-bs already exists. Skipping creation.\e[0m"
fi
echo


# URL map
# Create a URL map to route incoming requests to the backend service
echo "Creating URL map..."
if ! gcloud compute url-maps describe $SERVICE_NAME-$PROJECT_NUMBER-url-map > /dev/null 2>&1; then
gcloud compute url-maps create $SERVICE_NAME-$PROJECT_NUMBER-url-map \
    --default-service $SERVICE_NAME-$PROJECT_NUMBER-bs \
    --global
else
    printf "\e[31m$SERVICE_NAME-$PROJECT_NUMBER-url-map already exists. Skipping creation.\e[0m"
fi
echo

# Create a URL map to redirect HTTP to HTTPS
echo "Creating URL map for HTTP to HTTPS redirection..."
if ! gcloud compute url-maps describe http-to-https-redirect > /dev/null 2>&1; then
    gcloud compute url-maps import http-to-https-redirect \
        --source $SCRIPT_DIR/http-to-https.yaml \
        --global
else
    printf "\e[31mhttp-to-https-redirect already exists. Skipping creation.\e[0m"
fi
echo


# Target Proxy
# Create HTTP target proxy
echo "Creating HTTP target proxy..."
if ! gcloud compute target-http-proxies describe $SERVICE_NAME-$PROJECT_NUMBER-http-proxy > /dev/null 2>&1; then
    gcloud compute target-http-proxies create $SERVICE_NAME-$PROJECT_NUMBER-http-proxy \
        --url-map=http-to-https-redirect \
        --global
else
    printf "\e[31m$SERVICE_NAME-$PROJECT_NUMBER-http-proxy already exists. Skipping creation.\e[0m"
fi
echo

# Create HTTPS target proxy
echo "Creating HTTPS target proxy..."
if ! gcloud compute target-https-proxies describe $SERVICE_NAME-$PROJECT_NUMBER-https-proxy > /dev/null 2>&1; then
    gcloud compute target-https-proxies create $SERVICE_NAME-$PROJECT_NUMBER-https-proxy \
        --ssl-certificates=$SERVICE_NAME-$PROJECT_NUMBER-ssl \
        --url-map=$SERVICE_NAME-$PROJECT_NUMBER-url-map
        --global
else
    printf "\e[31m$SERVICE_NAME-$PROJECT_NUMBER-https-proxy already exists. Skipping creation.\e[0m"
fi
echo

# Forwarding Rules
# Create HTTP load balancer
echo "Creating HTTP load balancer..."
if ! gcloud compute forwarding-rules describe $SERVICE_NAME-$PROJECT_NUMBER-http-lb > /dev/null 2>&1; then
    gcloud compute forwarding-rules create $SERVICE_NAME-$PROJECT_NUMBER-http-lb \
        --load-balancing-scheme=EXTERNAL_MANAGED \
        --network-tier=PREMIUM \
        --address=$SERVICE_NAME-$PROJECT_NUMBER-ip \
        --target-http-proxy=$SERVICE_NAME-$PROJECT_NUMBER-http-proxy \
        --global \
        --ports=80
else
    printf "\e[31m$SERVICE_NAME-$PROJECT_NUMBER-http-lb already exists. Skipping creation.\e[0m"
fi
echo

# Create HTTPS load balancer
echo "Creating HTTPS load balancer..."
if ! gcloud compute forwarding-rules describe $SERVICE_NAME-$PROJECT_NUMBER-https-lb > /dev/null 2>&1; then
    gcloud compute forwarding-rules create $SERVICE_NAME-$PROJECT_NUMBER-https-lb \
        --load-balancing-scheme=EXTERNAL_MANAGED \
        --network-tier=PREMIUM \
        --address=$SERVICE_NAME-$PROJECT_NUMBER-ip \
        --target-https-proxy=$SERVICE_NAME-$PROJECT_NUMBER-https-proxy \
        --global \
        --ports=443
else
    printf "\e[31m$SERVICE_NAME-$PROJECT_NUMBER-https-lb already exists. Skipping creation.\e[0m"
fi
echo


printf "\nLoad balancer setup completed."