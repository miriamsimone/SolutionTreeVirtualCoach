#!/bin/bash

# Deployment script for PLC Coach Backend to Google Cloud Run

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== PLC Coach Backend Deployment ===${NC}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed${NC}"
    echo "Install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Configuration
PROJECT_ID="solutiontreevirtualcoach"
REGION="us-central1"
SERVICE_NAME="plc-coach-backend"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo -e "${YELLOW}Project ID:${NC} $PROJECT_ID"
echo -e "${YELLOW}Region:${NC} $REGION"
echo -e "${YELLOW}Service:${NC} $SERVICE_NAME"
echo ""

# Set the project
echo -e "${YELLOW}Setting GCloud project...${NC}"
gcloud config set project $PROJECT_ID

# Enable required APIs
echo -e "${YELLOW}Enabling required APIs...${NC}"
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Build the container (for linux/amd64 platform - required by Cloud Run)
echo -e "${YELLOW}Building Docker container for linux/amd64...${NC}"
docker build --platform linux/amd64 -t $IMAGE_NAME:latest .

# Push to Google Container Registry
echo -e "${YELLOW}Pushing to Container Registry...${NC}"
docker push $IMAGE_NAME:latest

# Deploy to Cloud Run
echo -e "${YELLOW}Deploying to Cloud Run...${NC}"
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME:latest \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1 \
    --timeout 300 \
    --max-instances 10 \
    --min-instances 0 \
    --set-env-vars "$(cat .env | grep -v '^#' | grep -v '^$' | tr '\n' ',' | sed 's/,$//')"

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')

echo ""
echo -e "${GREEN}=== Deployment Complete! ===${NC}"
echo -e "${GREEN}Service URL:${NC} $SERVICE_URL"
echo -e "${GREEN}Health Check:${NC} $SERVICE_URL/health"
echo -e "${GREEN}API Docs:${NC} $SERVICE_URL/docs"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Update frontend REACT_APP_API_URL to: $SERVICE_URL"
echo "2. Test the API: curl $SERVICE_URL/health"
echo "3. View logs: gcloud run logs read --service $SERVICE_NAME"
