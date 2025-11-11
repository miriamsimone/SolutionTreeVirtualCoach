# AI Powered PLC at Work Virtual Coach

**Organization:** Solution Tree
**Project ID:** QS6bbY3IK5hYXLdWZ9sB_1762208994432

An AI-driven solution designed to support educators in Professional Learning Communities (PLCs) by providing on-demand, context-aware coaching through two specialized AI agents.

## 🎯 Overview

The AI Powered PLC at Work Virtual Coach delivers personalized guidance to educators through:

- **Professional Learning Coach**: Expert in PLC team dynamics, collaboration, and professional learning processes
- **Classroom Curriculum Planning Coach**: Expert in standards-aligned curriculum design, assessment, and instructional planning

Both agents use RAG (Retrieval Augmented Generation) with metadata-filtered access to a curated corpus of Solution Tree titles, delivering responses grounded in research-based best practices.

## 🏗️ Architecture

```
SolutionTree/
├── backend/              # FastAPI + RAG backend
├── frontend/             # React + Vite frontend
├── scraper/              # Document ingestion pipeline
├── PRD.md               # Product Requirements Document
├── TASKLIST_BACKEND.md  # Backend implementation checklist
├── TASKLIST_FRONTEND.md # Frontend implementation checklist
└── TASKLIST_RAG.md      # RAG system checklist
```

### Tech Stack

**Backend:**
- FastAPI (Python)
- OpenAI API (GPT-4o-mini + embeddings)
- Pinecone (vector database)
- Firebase (authentication + Realtime Database)
- Google Cloud Run (deployment)

**Frontend:**
- React 18 + Vite
- TailwindCSS
- Firebase Authentication (Google OAuth)
- Firebase Hosting

**RAG System:**
- Pinecone vector database (1024 dimensions)
- OpenAI text-embedding-3-small
- Metadata filtering for agent-specific documents
- 147 document chunks from 6 Solution Tree titles

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Docker (for deployment)
- Google Cloud account with billing enabled
- Firebase project configured
- OpenAI API key
- Pinecone account

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run locally
uvicorn app.main:app --reload

# Access API docs: http://localhost:8000/docs
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your Firebase config and backend URL

# Run locally
npm run dev

# Access app: http://localhost:3000
```

### Deploy Backend to Cloud Run

```bash
cd backend
./deploy.sh
```

### Deploy Frontend to Firebase Hosting

```bash
cd frontend
npm run build
firebase deploy --only hosting
```

## 📚 Documentation

### Project Planning
- **[PRD.md](PRD.md)** - Complete Product Requirements Document
- **[TASKLIST_BACKEND.md](TASKLIST_BACKEND.md)** - Backend implementation tasks
- **[TASKLIST_FRONTEND.md](TASKLIST_FRONTEND.md)** - Frontend implementation tasks
- **[TASKLIST_RAG.md](TASKLIST_RAG.md)** - RAG system implementation tasks

### Backend Documentation
- **[backend/README.md](backend/README.md)** - Backend setup and API reference
- **[backend/API_REFERENCE.md](backend/API_REFERENCE.md)** - Complete API documentation
- **[backend/DEPLOYMENT.md](backend/DEPLOYMENT.md)** - Cloud Run deployment guide
- **[backend/STREAMING_API.md](backend/STREAMING_API.md)** - Streaming endpoint documentation
- **[backend/OPTIMIZATIONS.md](backend/OPTIMIZATIONS.md)** - Performance optimizations applied
- **[backend/TEST_RESULTS.md](backend/TEST_RESULTS.md)** - Test coverage and results

### Frontend Documentation
- **[FRONTEND_STREAMING_TASK.md](FRONTEND_STREAMING_TASK.md)** - Streaming implementation guide

## 🔑 Key Features

### ✅ Implemented

- **Dual AI Agents** with distinct personalities and expertise areas
- **RAG-based responses** with citations from Solution Tree materials
- **Real-time streaming** for fast response times (1-2s to first token)
- **Multi-turn conversations** with context awareness
- **Session management** with Firebase Realtime Database
- **Response ratings** and feedback collection
- **Analytics dashboard** with usage insights
- **Firebase Authentication** with Google OAuth
- **Agent-specific document filtering** via Pinecone metadata
- **Background task processing** for non-blocking operations
- **Performance optimizations** (2-3s average response time)

### 📊 Analytics Endpoint

The backend provides comprehensive usage analytics:

```bash
GET /api/analytics
```

Returns:
- Total conversations
- Active users
- Average rating
- Sessions this week
- Agent usage breakdown
- Recent activity (daily sessions)
- Top rated sessions

## 🎨 User Interface

- Clean, intuitive chat interface
- Agent switcher for easy switching between coaches
- Real-time streaming responses
- Citation display with source references
- Session history and management
- Response rating system
- Responsive design (desktop + tablet)

## 🔒 Security

- Firebase Authentication required for all API endpoints
- JWT token verification on backend
- CORS properly configured
- API keys stored in environment variables
- Non-root Docker container user
- Firebase Admin SDK for secure server-side operations

## 📈 Performance

### Response Times
- **Streaming endpoint**: First tokens in 1-2 seconds
- **Complete response**: 2-3 seconds average
- **Regular endpoint**: 5-8 seconds for full response

### Optimizations Applied
- GPT-4o-mini model (10x faster than GPT-4)
- Reduced context size (3 citations, 500 max tokens)
- Shorter system prompts (~75% reduction)
- Background Firebase saves
- Compact prompt formatting

### Cost Efficiency
- **95% reduction** in LLM API costs vs GPT-4
- **Cloud Run scales to $0** when idle
- ~$5-10/month for normal usage levels

## 🗄️ Database Schema

### Firebase Realtime Database

**Sessions:**
```
sessions/
  {user_id}/
    {session_id}/
      - session_id: string
      - user_id: string
      - agent_id: "professional_learning" | "classroom_curriculum"
      - title: string
      - created_at: ISO timestamp
      - last_accessed: ISO timestamp
      - messages: Message[]
```

**Feedback:**
```
feedback/
  {feedback_id}/
    - feedback_id: string
    - user_id: string
    - session_id: string
    - message_id: string
    - rating: number (1-5)
    - comment: string (optional)
    - timestamp: ISO timestamp
```

### Pinecone Vector Database

**Document Metadata:**
```json
{
  "doc_title": "Learning by Doing",
  "doc_name": "learning_by_doing.pdf",
  "chunk_index": 45,
  "text": "Document content...",
  "agent_professional_learning": true,
  "agent_curriculum_planning": false,
  "token_count": 150
}
```

## 📡 API Endpoints

### Authentication
- `POST /api/auth/verify` - Verify Firebase token

### Chat
- `POST /api/chat` - Send message (full response)
- `POST /api/chat/stream` - Send message (streaming response)
- `GET /api/agents` - List available agents

### Sessions
- `POST /api/sessions` - Create session
- `GET /api/sessions` - List user sessions
- `GET /api/sessions/{id}` - Get session details
- `DELETE /api/sessions/{id}` - Delete session

### Feedback
- `POST /api/feedback` - Submit response rating

### Analytics
- `GET /api/analytics?days=7` - Get usage analytics
- `GET /api/analytics/summary` - Get quick summary

## 🧪 Testing

### Backend Tests
```bash
cd backend
source venv/bin/activate

# Run all tests
python3 test_backend.py

# Test Pinecone connection
python3 test_pinecone.py

# Test analytics (requires token)
python3 test_analytics.py
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📦 Deployment

### Backend (Cloud Run)

```bash
cd backend
./deploy.sh
```

Service will be available at: `https://plc-coach-backend-xxxxx-uc.a.run.app`

**Monitoring:**
```bash
# View logs
gcloud run logs tail plc-coach-backend

# View metrics
gcloud run services describe plc-coach-backend
```

### Frontend (Firebase Hosting)

```bash
cd frontend

# Build
npm run build

# Deploy
firebase deploy --only hosting
```

Site will be available at: `https://solutiontreevirtualcoach.web.app`

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```bash
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=500

PINECONE_API_KEY=pcsk_...
PINECONE_INDEX_NAME=plc-coach
PINECONE_ENVIRONMENT=https://...
PINECONE_TOP_K=3

FIREBASE_CREDENTIALS_PATH=/tmp/firebase-credentials.json
FIREBASE_DATABASE_URL=https://solutiontreevirtualcoach-default-rtdb.firebaseio.com/

MAX_CONVERSATION_HISTORY=2
```

**Frontend (.env):**
```bash
REACT_APP_API_URL=http://localhost:8000
REACT_APP_FIREBASE_API_KEY=...
REACT_APP_FIREBASE_AUTH_DOMAIN=...
REACT_APP_FIREBASE_PROJECT_ID=...
```

## 📊 Curated Source Documents

6 Solution Tree titles ingested:
1. Behavior Academies
2. Learning by Doing
3. The Way Forward
4. Essential Standards Second Grade Mathematics
5. American Government Smart Goals Worksheet
6. Third Grade Team Smart Goal

**Total vectors in Pinecone:** 147 chunks

## 🎯 Success Metrics

- ✅ Total conversations: Real-time tracking via analytics
- ✅ Active users: Unique user count
- ✅ Average rating: 4.6/5 target
- ✅ Response accuracy: Citations from authoritative sources
- ✅ Time to assistance: 1-2s to first token
- ✅ Agent routing accuracy: Metadata-filtered queries

## 🛠️ Development

### Running Locally

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Making Changes

1. Create feature branch
2. Make changes
3. Test locally
4. Deploy to staging (if available)
5. Deploy to production

### Code Quality

```bash
# Backend
cd backend
black app/  # Format code
mypy app/   # Type checking

# Frontend
cd frontend
npm run lint
npm run format
```

## 🐛 Troubleshooting

### Backend Issues

**500 errors on /api/chat:**
- Check OpenAI API key is valid
- Verify Pinecone index exists and has documents
- Check Firebase credentials are correct

**No citations returned:**
- Verify Pinecone has documents with correct metadata
- Check metadata filters match document tags

**Slow responses:**
- Use streaming endpoint: `/api/chat/stream`
- Reduce `OPENAI_MAX_TOKENS` in .env
- Check OpenAI API status

### Frontend Issues

**Authentication fails:**
- Verify Firebase config in .env
- Check Google OAuth is enabled in Firebase Console

**API calls fail:**
- Verify `REACT_APP_API_URL` points to backend
- Check CORS settings in backend

**Streaming not working:**
- Ensure using `/api/chat/stream` endpoint
- Check browser supports EventSource/fetch streams

## 📞 Support

- **Project Lead:** miriam.rose.simone@gmail.com
- **Firebase Project:** solutiontreevirtualcoach
- **GCloud Project:** solutiontreevirtualcoach

## 📝 License

Copyright © 2025 Solution Tree. All rights reserved.

## 🙏 Acknowledgments

Built with:
- OpenAI GPT-4o-mini
- Pinecone Vector Database
- Firebase
- FastAPI
- React
- Google Cloud Platform

---

**Version:** 1.0.0
**Last Updated:** November 11, 2025
**Status:** ✅ Production Ready
