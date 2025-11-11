## Task List 1: Backend (FastAPI + Pinecone Integration)

**Owner:** Backend Engineer  
**Parallel Start:** Immediately

### Project Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    [CREATE]
│   ├── config.py                  [CREATE]
│   ├── dependencies.py            [CREATE]
│   ├── models/
│   │   ├── __init__.py           [CREATE]
│   │   ├── schemas.py            [CREATE]
│   ├── routes/
│   │   ├── __init__.py           [CREATE]
│   │   ├── auth.py               [CREATE]
│   │   ├── chat.py               [CREATE]
│   │   ├── sessions.py           [CREATE]
│   │   ├── feedback.py           [CREATE]
│   ├── services/
│   │   ├── __init__.py           [CREATE]
│   │   ├── openai_service.py     [CREATE]
│   │   ├── pinecone_service.py   [CREATE]
│   │   ├── firebase_service.py   [CREATE]
│   │   ├── agent_router.py       [CREATE]
│   ├── utils/
│   │   ├── __init__.py           [CREATE]
│   │   ├── logging.py            [CREATE]
│   │   ├── prompts.py            [CREATE]
├── requirements.txt               [CREATE]
├── .env.example                   [CREATE]
├── Dockerfile                     [CREATE]
└── README.md                      [CREATE]
```

### Key Deliverables

1. **Authentication Endpoint** (`routes/auth.py`)
   - Firebase token validation
   - User session creation

2. **Chat Endpoint** (`routes/chat.py`)
   - Accept user query and selected agent
   - Pinecone retrieval with metadata filtering
   - OpenAI prompt construction (agent-specific system prompts)
   - Response generation with citations
   - Multi-turn support (conversation context passing)

3. **Pinecone Service** (`services/pinecone_service.py`)
   - Initialize Pinecone index
   - Metadata filtering logic for agent routing
   - Vector similarity search
   - Document retrieval with source information

4. **OpenAI Service** (`services/openai_service.py`)
   - System prompt management (different for each agent)
   - Chat completion requests
   - Citation extraction from retrieved documents
   - Error handling for API failures

5. **Agent Router** (`services/agent_router.py`)
   - Route queries to correct agent based on user selection
   - Apply appropriate system prompts and metadata filters
   - Agent personality differentiation

6. **Sessions Endpoint** (`routes/sessions.py`)
   - Save conversation history to Firebase Realtime DB
   - Retrieve past sessions for a user
   - Session metadata (created_at, last_accessed, agent_used)

7. **Feedback Endpoint** (`routes/feedback.py`)
   - Accept response ratings (1-5 or binary)
   - Store feedback in Firebase (for future analytics)

8. **Firebase Service** (`services/firebase_service.py`)
   - Initialize Firebase Admin SDK
   - Read/write sessions to Realtime DB
   - Basic logging to Firebase
   - User authentication verification

9. **Error Handling & Logging**
   - Comprehensive error responses
   - Request/response logging
   - Performance metrics logging

### Files to Edit During Development
- `requirements.txt` — Add dependencies (fastapi, openai, pinecone-client, firebase-admin, etc.)
- `.env.example` — Document all required environment variables

### Integration Points
- Frontend will POST to `/chat` endpoint with query and agent_id
- Frontend will use Firebase auth tokens in Authorization header
- Responses must include citations and source document info

