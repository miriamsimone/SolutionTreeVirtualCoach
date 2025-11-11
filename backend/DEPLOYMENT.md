# Deployment Guide - Google Cloud Run

This guide covers deploying the PLC Coach Backend to Google Cloud Run.

## Prerequisites

1. **Google Cloud Account** with billing enabled
2. **gcloud CLI** installed: https://cloud.google.com/sdk/docs/install
3. **Docker** installed: https://docs.docker.com/get-docker/
4. **Firebase Credentials** (already have: /tmp/firebase-credentials.json)

## Quick Deploy

### Option 1: Automated Script (Recommended)

```bash
cd backend
./deploy.sh
```

This script will:
1. Set the GCloud project
2. Enable required APIs
3. Build Docker container
4. Push to Container Registry
5. Deploy to Cloud Run
6. Display the service URL

### Option 2: Manual Deployment

```bash
cd backend
./deploy-manual.sh
```

Follow the step-by-step prompts.

## Detailed Manual Steps

### 1. Install and Configure gcloud CLI

```bash
# Install gcloud (if not installed)
# Visit: https://cloud.google.com/sdk/docs/install

# Login to Google Cloud
gcloud auth login

# Set your project
gcloud config set project solutiontreevirtualcoach

# Authenticate Docker with GCR
gcloud auth configure-docker
```

### 2. Enable Required APIs

```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 3. Prepare Environment Variables

Your current `.env` file has all required variables. Cloud Run will use them.

**Important**: Make sure these are set:
- `OPENAI_API_KEY`
- `PINECONE_API_KEY`
- `PINECONE_INDEX_NAME`
- `PINECONE_ENVIRONMENT`
- `FIREBASE_DATABASE_URL`
- `FIREBASE_CREDENTIALS_PATH`

### 4. Build Docker Image

```bash
docker build -t gcr.io/solutiontreevirtualcoach/plc-coach-backend .
```

Test locally (optional):
```bash
docker run -p 8080:8080 --env-file .env gcr.io/solutiontreevirtualcoach/plc-coach-backend
```

### 5. Push to Google Container Registry

```bash
docker push gcr.io/solutiontreevirtualcoach/plc-coach-backend
```

### 6. Deploy to Cloud Run

```bash
gcloud run deploy plc-coach-backend \
  --image gcr.io/solutiontreevirtualcoach/plc-coach-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10 \
  --min-instances 0 \
  --set-env-vars "OPENAI_API_KEY=${OPENAI_API_KEY},PINECONE_API_KEY=${PINECONE_API_KEY},PINECONE_INDEX_NAME=plc-coach,PINECONE_ENVIRONMENT=${PINECONE_ENVIRONMENT},FIREBASE_DATABASE_URL=https://solutiontreevirtualcoach-default-rtdb.firebaseio.com/,FIREBASE_CREDENTIALS_PATH=/tmp/firebase-credentials.json"
```

### 7. Get Service URL

```bash
gcloud run services describe plc-coach-backend \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

Example output: `https://plc-coach-backend-xxxxx-uc.a.run.app`

## Configuration

### Cloud Run Settings

- **Region**: us-central1 (Iowa)
- **Memory**: 1GB (can increase to 2GB if needed)
- **CPU**: 1
- **Timeout**: 300s (5 minutes)
- **Max Instances**: 10 (auto-scales based on traffic)
- **Min Instances**: 0 (scales to zero when idle = no cost)

### Environment Variables

Set via `--set-env-vars` flag or Cloud Run console:

```bash
OPENAI_API_KEY=sk-proj-...
PINECONE_API_KEY=pcsk_...
PINECONE_INDEX_NAME=plc-coach
PINECONE_ENVIRONMENT=https://plc-coach-w9l88ji.svc.aped-4627-b74a.pinecone.io
FIREBASE_DATABASE_URL=https://solutiontreevirtualcoach-default-rtdb.firebaseio.com/
FIREBASE_CREDENTIALS_PATH=/tmp/firebase-credentials.json
```

### Firebase Credentials

The Firebase service account key is already in your environment variables. Cloud Run will use the credentials from the environment.

## Testing Deployment

### 1. Health Check

```bash
curl https://YOUR-SERVICE-URL/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "ai-plc-coach-api"
}
```

### 2. Test API Documentation

Visit: `https://YOUR-SERVICE-URL/docs`

### 3. Test Chat Endpoint

```bash
curl -X POST https://YOUR-SERVICE-URL/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN" \
  -d '{
    "query": "How can we improve team collaboration?",
    "agent_id": "professional_learning"
  }'
```

## Update Frontend

After deployment, update your frontend environment variables:

```bash
# In frontend/.env
REACT_APP_API_URL=https://YOUR-SERVICE-URL
```

## Monitoring

### View Logs

```bash
# Real-time logs
gcloud run logs tail plc-coach-backend --region us-central1

# Recent logs
gcloud run logs read plc-coach-backend --region us-central1 --limit 50
```

### View Metrics

Visit Google Cloud Console:
1. Go to Cloud Run
2. Select `plc-coach-backend`
3. View Metrics tab for:
   - Request count
   - Response times
   - Error rate
   - Instance count

## Cost Estimation

Cloud Run pricing (us-central1):
- **CPU**: $0.00002400 per vCPU-second
- **Memory**: $0.00000250 per GiB-second
- **Requests**: $0.40 per million requests
- **Free tier**: 2 million requests/month

**Example Monthly Cost** (1000 users, 10k requests/month):
- Compute time: ~$5-10
- Requests: ~$0.04
- **Total**: ~$5-10/month

Scales to zero = **$0 when idle**!

## CI/CD (Optional)

### Automated Deployment with Cloud Build

```bash
# Set up Cloud Build trigger
gcloud builds submit --config cloudbuild.yaml
```

This will:
1. Build on every push to main
2. Run tests (if configured)
3. Deploy automatically

### GitHub Integration

1. Connect GitHub repo to Cloud Build
2. Create trigger on push to `main`
3. Uses `cloudbuild.yaml` configuration
4. Automatic deployment on merge

## Troubleshooting

### Container won't start

Check logs:
```bash
gcloud run logs read plc-coach-backend --limit 100
```

Common issues:
- Missing environment variables
- Port mismatch (Cloud Run expects port from $PORT env var)
- Firebase credentials not found

### Cold starts are slow

Solution: Set min instances to 1
```bash
gcloud run services update plc-coach-backend --min-instances 1
```

Note: This keeps 1 instance always running (costs ~$5-10/month)

### High costs

- Reduce max-instances: `--max-instances 5`
- Reduce memory: `--memory 512Mi`
- Set min-instances to 0 (scale to zero)
- Review logs for unnecessary requests

### Authentication errors

Ensure CORS is configured correctly:
```python
# In app/main.py
cors_origins = [
    "https://your-frontend-domain.web.app",
    "http://localhost:3000"
]
```

## Rollback

If deployment fails, rollback to previous version:

```bash
gcloud run services update-traffic plc-coach-backend \
  --to-revisions PREVIOUS_REVISION=100
```

List revisions:
```bash
gcloud run revisions list --service plc-coach-backend
```

## Security

### Best Practices

1. ✅ Firebase credentials via environment (not in code)
2. ✅ API keys in environment variables
3. ✅ Non-root user in Docker container
4. ✅ CORS properly configured
5. ⚠️ Consider adding rate limiting
6. ⚠️ Consider adding API authentication beyond Firebase

### Secrets Management (Advanced)

Use Google Secret Manager instead of environment variables:

```bash
# Create secret
echo -n "$OPENAI_API_KEY" | gcloud secrets create openai-api-key --data-file=-

# Grant access to Cloud Run
gcloud secrets add-iam-policy-binding openai-api-key \
  --member serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --role roles/secretmanager.secretAccessor

# Deploy with secret
gcloud run deploy plc-coach-backend \
  --set-secrets OPENAI_API_KEY=openai-api-key:latest
```

## Support

- **Cloud Run Docs**: https://cloud.google.com/run/docs
- **Pricing Calculator**: https://cloud.google.com/products/calculator
- **Status Page**: https://status.cloud.google.com/

## Next Steps

1. Deploy backend to Cloud Run
2. Get the service URL
3. Update frontend API URL
4. Deploy frontend to Firebase Hosting
5. Test end-to-end
6. Set up monitoring and alerts
7. Configure custom domain (optional)
