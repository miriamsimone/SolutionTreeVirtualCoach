# API Reference - Quick Guide

## Base URL
```
http://localhost:8000
```

## Authentication
All endpoints (except `/` and `/health`) require Firebase ID token:
```
Authorization: Bearer <firebase_id_token>
```

## Agent IDs
- `professional_learning` - Professional Learning Coach
- `classroom_curriculum` - Classroom Curriculum Planning Coach

---

## Endpoints

### Analytics

**`GET /api/analytics?days=7`**

Get usage statistics and insights.

Query Parameters:
- `days` (optional): Number of days for recent activity (default: 7)

Response 200:
```json
{
  "total_conversations": 127,
  "active_users": 43,
  "avg_rating": 4.6,
  "sessions_this_week": 18,
  "agent_usage": {
    "professional_learning": 65.5,
    "classroom_curriculum": 34.5
  },
  "agent_usage_counts": {
    "professional_learning": 83,
    "classroom_curriculum": 44
  },
  "recent_activity": [
    {"date": "2025-01-08", "sessions": 12},
    {"date": "2025-01-09", "sessions": 15}
  ],
  "total_feedback_count": 89,
  "top_rated_sessions": [
    {
      "session_id": "uuid",
      "avg_rating": 5.0,
      "rating_count": 3
    }
  ],
  "generated_at": "2025-01-10T10:30:00Z"
}
```

**`GET /api/analytics/summary`**

Get quick analytics summary (faster, lightweight).

Response 200:
```json
{
  "total_conversations": 127,
  "active_users": 43,
  "avg_rating": 4.6,
  "total_feedback": 89
}
```

---

### Health & Info

**`GET /`**
```json
Response: {
  "name": "AI PLC Coach API",
  "version": "1.0.0",
  "status": "running"
}
```

**`GET /health`**
```json
Response: {
  "status": "healthy",
  "service": "ai-plc-coach-api"
}
```

---

### Authentication

**`POST /api/auth/verify`**

Verify Firebase token and get user info.

Headers:
```
Authorization: Bearer <token>
```

Response 200:
```json
{
  "user_id": "abc123",
  "email": "user@example.com",
  "name": "User Name",
  "verified": true
}
```

---

### Chat

**`POST /api/chat`**

Send message to AI coach.

Headers:
```
Authorization: Bearer <token>
```

Request:
```json
{
  "query": "How can we improve our PLC meetings?",
  "agent_id": "professional_learning",
  "session_id": "uuid-optional"
}
```

Response 200:
```json
{
  "response": "Based on Solution Tree's PLC framework...",
  "citations": [
    {
      "id": "cite_1",
      "source_title": "Learning by Doing",
      "page_number": 45,
      "chunk_text": "Teams that focus on the four critical questions...",
      "relevance_score": 0.92
    }
  ],
  "agent_used": "professional_learning",
  "session_id": "uuid",
  "message_id": "uuid"
}
```

**`GET /api/agents`**

Get available agents.

Response 200:
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

---

### Sessions

**`POST /api/sessions`**

Create new session.

Headers:
```
Authorization: Bearer <token>
```

Request:
```json
{
  "agent_id": "professional_learning",
  "title": "My PLC Session"
}
```

Response 201:
```json
{
  "session_id": "uuid",
  "user_id": "abc123",
  "agent_id": "professional_learning",
  "title": "My PLC Session",
  "messages": [],
  "created_at": "2025-01-15T10:30:00Z",
  "last_accessed": "2025-01-15T10:30:00Z"
}
```

**`GET /api/sessions?limit=50`**

Get all user's sessions.

Response 200:
```json
[
  {
    "session_id": "uuid",
    "user_id": "abc123",
    "agent_id": "professional_learning",
    "title": "My PLC Session",
    "messages": [...],
    "created_at": "2025-01-15T10:30:00Z",
    "last_accessed": "2025-01-15T10:35:00Z"
  }
]
```

**`GET /api/sessions/{session_id}`**

Get specific session with full history.

Response 200:
```json
{
  "session_id": "uuid",
  "user_id": "abc123",
  "agent_id": "professional_learning",
  "title": "My PLC Session",
  "messages": [
    {
      "role": "user",
      "content": "How can we improve?",
      "timestamp": "2025-01-15T10:31:00Z",
      "message_id": "msg-1"
    },
    {
      "role": "assistant",
      "content": "Based on the research...",
      "timestamp": "2025-01-15T10:31:05Z",
      "message_id": "msg-2",
      "citations": [...]
    }
  ],
  "created_at": "2025-01-15T10:30:00Z",
  "last_accessed": "2025-01-15T10:31:05Z"
}
```

**`DELETE /api/sessions/{session_id}`**

Delete session.

Response 204: (No content)

---

### Feedback

**`POST /api/feedback`**

Submit rating for a response.

Headers:
```
Authorization: Bearer <token>
```

Request:
```json
{
  "message_id": "msg-uuid",
  "session_id": "session-uuid",
  "rating": 5,
  "comment": "Very helpful!"
}
```

Response 201:
```json
{
  "feedback_id": "feedback-uuid",
  "message": "Feedback received successfully"
}
```

---

## Error Responses

All errors follow this format:
```json
{
  "detail": "Error description"
}
```

Status codes:
- `401` - Unauthorized (invalid/missing token)
- `404` - Not found (session/resource doesn't exist)
- `500` - Internal server error

---

## Example Flow

1. **Get Firebase token** from frontend auth
2. **Verify token**: `POST /api/auth/verify`
3. **Get available agents**: `GET /api/agents`
4. **Create session**: `POST /api/sessions`
5. **Send message**: `POST /api/chat` with session_id
6. **Continue conversation**: `POST /api/chat` with same session_id
7. **Rate response**: `POST /api/feedback`
8. **View history**: `GET /api/sessions/{session_id}`

---

## Testing with curl

```bash
# Set your token
TOKEN="your_firebase_token_here"

# Verify auth
curl -X POST http://localhost:8000/api/auth/verify \
  -H "Authorization: Bearer $TOKEN"

# Get agents
curl http://localhost:8000/api/agents

# Create session
curl -X POST http://localhost:8000/api/sessions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "professional_learning",
    "title": "Test Session"
  }'

# Send chat message
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How can we improve collaboration?",
    "agent_id": "professional_learning"
  }'
```
