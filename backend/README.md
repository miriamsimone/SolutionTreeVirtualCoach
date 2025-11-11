# AI Powered PLC at Work Virtual Coach - Backend

FastAPI backend service for the AI Powered PLC at Work Virtual Coach application.

## Overview

This backend provides RESTful API endpoints for:
- **Two AI Coaching Agents**: Professional Learning Coach and Classroom Curriculum Planning Coach
- **RAG-based responses**: Context-aware answers using Pinecone vector database
- **Firebase Authentication**: Google OAuth with JIT provisioning
- **Session Management**: Multi-turn conversation support
- **User Feedback**: Response rating and feedback collection

## Architecture

- **Framework**: FastAPI with async support
- **Vector DB**: Pinecone for document retrieval with metadata filtering
- **LLM**: OpenAI GPT-4 for response generation
- **Authentication**: Firebase Admin SDK
- **Database**: Firebase Realtime Database for sessions and feedback

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── config.py                  # Configuration and settings
│   ├── dependencies.py            # FastAPI dependencies
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py            # Pydantic models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py               # Authentication endpoints
│   │   ├── chat.py               # Chat endpoints
│   │   ├── sessions.py           # Session management
│   │   └── feedback.py           # Feedback endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── openai_service.py     # OpenAI integration
│   │   ├── pinecone_service.py   # Pinecone integration
│   │   ├── firebase_service.py   # Firebase integration
│   │   └── agent_router.py       # Agent routing logic
│   └── utils/
│       ├── __init__.py
│       ├── logging.py            # Logging configuration
│       └── prompts.py            # Prompt utilities
├── requirements.txt
├── .env.example
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- OpenAI API key
- Pinecone account and API key
- Firebase project with:
  - Authentication enabled (Google provider)
  - Realtime Database created
  - Service account credentials JSON file

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   cd backend
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and fill in your credentials:
   ```bash
   # OpenAI
   OPENAI_API_KEY=sk-...

   # Pinecone
   PINECONE_API_KEY=...
   PINECONE_ENVIRONMENT=us-east-1-aws
   PINECONE_INDEX_NAME=plc-coach-documents

   # Firebase
   FIREBASE_CREDENTIALS_PATH=/absolute/path/to/firebase-credentials.json
   FIREBASE_DATABASE_URL=https://your-project-id.firebaseio.com
   ```

5. **Download Firebase credentials**:
   - Go to Firebase Console → Project Settings → Service Accounts
   - Click "Generate New Private Key"
   - Save the JSON file and update `FIREBASE_CREDENTIALS_PATH` in `.env`

### Running the Server

**Development mode** (with auto-reload):
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Production mode**:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## API Endpoints

### Authentication

#### `POST /api/auth/verify`
Verify Firebase ID token and return user information.

**Headers**:
```
Authorization: Bearer <firebase_id_token>
```

**Response**:
```json
{
  "user_id": "firebase_uid",
  "email": "user@example.com",
  "name": "User Name",
  "verified": true
}
```

### Chat

#### `POST /api/chat`
Send a message and get AI response with citations.

**Headers**:
```
Authorization: Bearer <firebase_id_token>
```

**Request Body**:
```json
{
  "query": "How can our PLC team improve collaboration?",
  "agent_id": "professional_learning",
  "session_id": "optional-uuid"
}
```

**Response**:
```json
{
  "response": "Based on the PLC framework...",
  "citations": [
    {
      "id": "cite_1",
      "source_title": "Learning by Doing",
      "page_number": 45,
      "chunk_text": "Relevant excerpt...",
      "relevance_score": 0.92
    }
  ],
  "agent_used": "professional_learning",
  "session_id": "uuid",
  "message_id": "uuid"
}
```

#### `GET /api/agents`
Get list of available AI agents.

**Response**:
```json
[
  {
    "agent_id": "professional_learning",
    "name": "Professional Learning Coach",
    "description": "Expert in PLC team dynamics..."
  },
  {
    "agent_id": "classroom_curriculum",
    "name": "Classroom Curriculum Planning Coach",
    "description": "Expert in standards-aligned curriculum..."
  }
]
```

### Sessions

#### `POST /api/sessions`
Create a new session.

**Headers**:
```
Authorization: Bearer <firebase_id_token>
```

**Request Body**:
```json
{
  "agent_id": "professional_learning",
  "title": "PLC Planning Session"
}
```

#### `GET /api/sessions`
Get all sessions for the authenticated user.

**Query Parameters**:
- `limit` (optional): Maximum number of sessions (default: 50)

#### `GET /api/sessions/{session_id}`
Get a specific session with full message history.

#### `DELETE /api/sessions/{session_id}`
Delete a session.

### Feedback

#### `POST /api/feedback`
Submit rating for a chat response.

**Headers**:
```
Authorization: Bearer <firebase_id_token>
```

**Request Body**:
```json
{
  "message_id": "uuid",
  "session_id": "uuid",
  "rating": 5,
  "comment": "Very helpful response!"
}
```

## Agent Configuration

Agents are configured in `app/config.py`:

### Professional Learning Coach
- **Focus**: PLC team dynamics, collaboration, professional learning
- **Metadata Filter**: `agent_category` in `["professional_learning", "general"]`
- **Personality**: Collaborative, supportive, team-focused

### Classroom Curriculum Planning Coach
- **Focus**: Standards alignment, curriculum design, SMART goals
- **Metadata Filter**: `agent_category` in `["classroom_curriculum", "general"]`
- **Personality**: Detail-oriented, systematic, student-centered

## Pinecone Document Metadata

When ingesting documents into Pinecone, use this metadata structure:

```python
{
    "source_title": "Learning by Doing",
    "page_number": 45,
    "text": "Content of the chunk...",
    "agent_category": "professional_learning"  # or "classroom_curriculum" or "general"
}
```

## Firebase Database Schema

### Sessions
```
sessions/
  {user_id}/
    {session_id}/
      session_id: string
      user_id: string
      agent_id: string
      title: string
      created_at: ISO timestamp
      last_accessed: ISO timestamp
      messages: [
        {
          role: "user" | "assistant"
          content: string
          timestamp: ISO timestamp
          message_id: string
          citations: [...] (optional)
        }
      ]
```

### Feedback
```
feedback/
  {feedback_id}/
    feedback_id: string
    user_id: string
    session_id: string
    message_id: string
    rating: number (1-5)
    comment: string (optional)
    timestamp: ISO timestamp
```

## Configuration Options

All settings can be configured via environment variables (see `.env.example`):

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4` |
| `OPENAI_TEMPERATURE` | Response creativity (0-1) | `0.7` |
| `OPENAI_MAX_TOKENS` | Max response length | `1000` |
| `PINECONE_TOP_K` | Number of documents to retrieve | `5` |
| `MAX_CONVERSATION_HISTORY` | Previous message pairs to include | `5` |

## Error Handling

The API uses standard HTTP status codes:
- `200`: Success
- `201`: Created
- `204`: No Content
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `500`: Internal Server Error

Error responses include details:
```json
{
  "detail": "Error description"
}
```

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black app/
```

### Type Checking
```bash
mypy app/
```

## Deployment Considerations

For production deployment:

1. **Set `DEBUG=false`** in environment variables
2. **Use a production ASGI server** like Gunicorn with Uvicorn workers
3. **Enable HTTPS** and configure CORS appropriately
4. **Set up monitoring** and logging
5. **Implement rate limiting** at the infrastructure level
6. **Use secrets management** for API keys (e.g., AWS Secrets Manager)
7. **Configure auto-scaling** based on load

## Troubleshooting

### Common Issues

1. **Firebase authentication fails**:
   - Verify `FIREBASE_CREDENTIALS_PATH` is absolute and file exists
   - Check Firebase Database URL is correct
   - Ensure service account has proper permissions

2. **Pinecone queries fail**:
   - Verify index exists and API key is correct
   - Check index dimension matches embedding model (1536 for ada-002)
   - Ensure documents are ingested with proper metadata

3. **OpenAI requests fail**:
   - Check API key is valid
   - Verify account has sufficient quota
   - Review model name (ensure it's available in your account)

## Support

For issues or questions:
- Review the interactive API docs at `/docs`
- Check Firebase Console for auth/database issues
- Review Pinecone Console for index status
- Check application logs for detailed error messages

## License

Copyright © 2025 Solution Tree
