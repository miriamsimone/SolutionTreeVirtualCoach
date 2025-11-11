#!/bin/bash

# Manual deployment script with step-by-step instructions
# Use this if the automatic deploy.sh doesn't work

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== Manual Deployment Guide ===${NC}"
echo ""

PROJECT_ID="solutiontreevirtualcoach"
REGION="us-central1"
SERVICE_NAME="plc-coach-backend"

echo -e "${YELLOW}Step 1: Set GCloud Project${NC}"
echo "Run: gcloud config set project $PROJECT_ID"
read -p "Press enter when done..."

echo -e "${YELLOW}Step 2: Enable APIs${NC}"
echo "Run these commands:"
echo "  gcloud services enable run.googleapis.com"
echo "  gcloud services enable containerregistry.googleapis.com"
echo "  gcloud services enable cloudbuild.googleapis.com"
read -p "Press enter when done..."

echo -e "${YELLOW}Step 3: Build Docker Image${NC}"
echo "Run: docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME ."
read -p "Press enter when done..."

echo -e "${YELLOW}Step 4: Push to Container Registry${NC}"
echo "Run: docker push gcr.io/$PROJECT_ID/$SERVICE_NAME"
read -p "Press enter when done..."

echo -e "${YELLOW}Step 5: Deploy to Cloud Run${NC}"
echo "Run this command (all on one line):"
echo ""
echo "gcloud run deploy $SERVICE_NAME \\"
echo "  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \\"
echo "  --platform managed \\"
echo "  --region $REGION \\"
echo "  --allow-unauthenticated \\"
echo "  --memory 1Gi \\"
echo "  --cpu 1 \\"
echo "  --timeout 300 \\"
echo "  --set-env-vars OPENAI_API_KEY=\$OPENAI_API_KEY,PINECONE_API_KEY=\$PINECONE_API_KEY,PINECONE_INDEX_NAME=plc-coach,PINECONE_ENVIRONMENT=\$PINECONE_ENVIRONMENT,FIREBASE_DATABASE_URL=https://solutiontreevirtualcoach-default-rtdb.firebaseio.com/,FIREBASE_CREDENTIALS_PATH=/tmp/firebase-credentials.json"
echo ""
read -p "Press enter when done..."

echo -e "${GREEN}Deployment should be complete!${NC}"
echo ""
echo "Get your service URL with:"
echo "gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)'"
