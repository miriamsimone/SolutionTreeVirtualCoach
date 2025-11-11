# Frontend Task: Implement Streaming Chat for Better Performance

## Problem
Chat responses are slow (5-10 seconds) with no feedback to the user. We need to implement streaming to show responses in real-time.

## Solution
The backend now has a streaming endpoint at `POST /api/chat/stream` that returns Server-Sent Events (SSE) for real-time responses.

## Task

Replace the current `/api/chat` endpoint usage with `/api/chat/stream` to implement real-time streaming responses.

### Current Flow (Slow)
1. User sends message
2. Loading spinner for 5-10 seconds
3. Complete response appears all at once

### New Flow (Fast)
1. User sends message
2. Citations appear immediately (~1-2s)
3. Response text streams in real-time (word by word)
4. Much better user experience

## API Details

### Endpoint
```
POST http://localhost:8000/api/chat/stream
```

### Request (Same as before)
```json
{
  "query": "How can we improve team collaboration?",
  "agent_id": "professional_learning",
  "session_id": "optional-uuid"
}
```

### Response (Server-Sent Events)

The endpoint returns a stream of events in this order:

#### 1. Citations Event (first event, ~1-2s)
```json
{
  "type": "citations",
  "citations": [
    {
      "id": "cite_1",
      "source_title": "Learning by Doing",
      "page_number": 45,
      "chunk_text": "...",
      "relevance_score": 0.92
    }
  ],
  "session_id": "uuid",
  "message_id": "uuid"
}
```

#### 2. Content Events (streaming, word by word)
```json
{
  "type": "content",
  "content": "Based "
}
{
  "type": "content",
  "content": "on the "
}
{
  "type": "content",
  "content": "research..."
}
```

#### 3. Done Event (final event)
```json
{
  "type": "done"
}
```

## Implementation Guide

### Step 1: Update API Service

Find where you're calling `/api/chat` and create a new streaming function:

```javascript
// In your API service file (e.g., api.js)

export async function streamChatMessage({ query, agentId, sessionId, token, onCitation, onContent, onDone, onError }) {
  try {
    const response = await fetch('http://localhost:8000/api/chat/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        query,
        agent_id: agentId,
        session_id: sessionId
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = JSON.parse(line.slice(6));

          switch (data.type) {
            case 'citations':
              onCitation(data);
              break;
            case 'content':
              onContent(data.content);
              break;
            case 'done':
              onDone();
              break;
            case 'error':
              onError(data.error);
              break;
          }
        }
      }
    }
  } catch (error) {
    console.error('Streaming error:', error);
    onError(error.message);
  }
}
```

### Step 2: Update Chat Component

Update your chat component to use streaming:

```javascript
// Example: In ChatWindow.jsx or similar

const [streamingResponse, setStreamingResponse] = useState('');
const [citations, setCitations] = useState([]);
const [isStreaming, setIsStreaming] = useState(false);

const handleSendMessage = async (message) => {
  setIsStreaming(true);
  setStreamingResponse('');
  setCitations([]);

  await streamChatMessage({
    query: message,
    agentId: selectedAgent,
    sessionId: currentSessionId,
    token: firebaseToken,

    onCitation: (data) => {
      // Citations arrive first
      setCitations(data.citations);
      setCurrentSessionId(data.session_id);
      setCurrentMessageId(data.message_id);
    },

    onContent: (chunk) => {
      // Append each chunk to build the full response
      setStreamingResponse(prev => prev + chunk);
    },

    onDone: () => {
      // Streaming complete
      setIsStreaming(false);
      // Optionally add to message history
      addMessageToHistory({
        role: 'assistant',
        content: streamingResponse,
        citations: citations
      });
    },

    onError: (error) => {
      setIsStreaming(false);
      console.error('Chat error:', error);
      // Show error to user
    }
  });
};
```

### Step 3: Update UI to Show Streaming

Show the streaming response in real-time:

```jsx
<div className="chat-messages">
  {messages.map((msg, idx) => (
    <Message key={idx} message={msg} />
  ))}

  {/* Show streaming response */}
  {isStreaming && (
    <div className="message assistant streaming">
      <div className="content">{streamingResponse}</div>
      <div className="streaming-indicator">●●●</div>
    </div>
  )}

  {/* Show citations as they arrive */}
  {citations.length > 0 && (
    <div className="citations">
      {citations.map(cite => (
        <Citation key={cite.id} citation={cite} />
      ))}
    </div>
  )}
</div>
```

## Testing

1. **Test streaming works**: Send a message and verify text appears word-by-word
2. **Test citations appear first**: Citations should show within 1-2 seconds
3. **Test error handling**: Disconnect network and verify error handling
4. **Test session persistence**: Verify messages save to Firebase correctly

## Expected Results

- **Before**: 5-10 second wait with no feedback
- **After**: Citations in 1-2s, response streams in real-time
- **User Experience**: Much better! Feels instant.

## Fallback

If you encounter issues, the old `/api/chat` endpoint still works (but slower):
```javascript
// Fallback to old endpoint
const response = await fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({ query, agent_id: agentId, session_id: sessionId })
});
const data = await response.json();
```

## Questions?

- Backend streaming endpoint: `POST /api/chat/stream`
- Backend docs: `backend/STREAMING_API.md`
- Both old and new endpoints work simultaneously
- The streaming endpoint has the same authentication requirements

## Success Criteria

✅ User sees citations within 1-2 seconds
✅ Response text appears word-by-word in real-time
✅ No long loading spinners
✅ Messages still save to Firebase correctly
✅ Error handling works properly
