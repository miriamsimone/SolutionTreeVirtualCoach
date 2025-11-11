# 🚀 Quick Deploy to Cloud Run

## Prerequisites
- Google Cloud account with billing enabled
- gcloud CLI installed
- Docker installed

## 1-Command Deploy

```bash
./deploy.sh
```

That's it! The script handles everything.

## What Happens

1. ✅ Sets GCloud project to `solutiontreevirtualcoach`
2. ✅ Enables Cloud Run, Container Registry, Cloud Build APIs
3. ✅ Builds Docker container
4. ✅ Pushes to Google Container Registry
5. ✅ Deploys to Cloud Run (auto-scales, $0 when idle)
6. ✅ Gives you the service URL

## Expected Output

```
=== Deployment Complete! ===
Service URL: https://plc-coach-backend-xxxxx-uc.a.run.app
Health Check: https://plc-coach-backend-xxxxx-uc.a.run.app/health
API Docs: https://plc-coach-backend-xxxxx-uc.a.run.app/docs
```

## Update Frontend

After deployment, update frontend:

```bash
cd ../frontend
# Edit .env
REACT_APP_API_URL=https://plc-coach-backend-xxxxx-uc.a.run.app
```

## Test Deployment

```bash
curl https://YOUR-SERVICE-URL/health
```

Should return:
```json
{"status": "healthy", "service": "ai-plc-coach-api"}
```

## Cost

- **Idle**: $0/month (scales to zero)
- **Active** (10k requests/month): ~$5-10/month
- Free tier: 2 million requests/month

## Troubleshooting

**If deploy.sh fails:**
```bash
./deploy-manual.sh  # Step-by-step guide
```

**View logs:**
```bash
gcloud run logs tail plc-coach-backend
```

**Redeploy:**
```bash
./deploy.sh  # Just run again
```

## Full Documentation

See `DEPLOYMENT.md` for detailed instructions.
