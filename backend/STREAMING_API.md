# Streaming Chat API

## New Endpoint: POST /api/chat/stream

For **much faster perceived response times**, use the streaming endpoint instead of the regular `/api/chat` endpoint.

### Benefits
- **Instant feedback**: First tokens appear in ~1-2 seconds
- **Better UX**: Users see response forming in real-time
- **Same quality**: Uses same RAG pipeline and citations

### How It Works

The streaming endpoint returns Server-Sent Events (SSE) with three event types:

#### 1. Citations Event (first)
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

#### 2. Content Events (streaming)
```json
{
  "type": "content",
  "content": "chunk of text"
}
```

#### 3. Done Event (last)
```json
{
  "type": "done"
}
```

### Frontend Usage Example

```javascript
async function streamChat(query, agentId, sessionId) {
  const response = await fetch('http://localhost:8000/api/chat/stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${firebaseToken}`
    },
    body: JSON.stringify({
      query,
      agent_id: agentId,
      session_id: sessionId
    })
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  let citations = [];
  let sessionId = null;
  let messageId = null;
  let fullResponse = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split('\n');

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.slice(6));

        if (data.type === 'citations') {
          citations = data.citations;
          sessionId = data.session_id;
          messageId = data.message_id;
          // Display citations immediately
          displayCitations(citations);
        } else if (data.type === 'content') {
          fullResponse += data.content;
          // Update UI with new content
          updateChatMessage(fullResponse);
        } else if (data.type === 'done') {
          // Streaming complete
          finalizeChatMessage(fullResponse, citations);
        } else if (data.type === 'error') {
          console.error('Streaming error:', data.error);
        }
      }
    }
  }
}
```

### React Example with EventSource

```jsx
import { useEffect, useState } from 'react';

function StreamingChat({ query, agentId, sessionId, token }) {
  const [response, setResponse] = useState('');
  const [citations, setCitations] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    setLoading(true);
    setResponse('');

    const response = await fetch('/api/chat/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ query, agent_id: agentId, session_id: sessionId })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n').filter(line => line.startsWith('data: '));

      for (const line of lines) {
        const data = JSON.parse(line.slice(6));

        if (data.type === 'citations') {
          setCitations(data.citations);
        } else if (data.type === 'content') {
          setResponse(prev => prev + data.content);
        } else if (data.type === 'done') {
          setLoading(false);
        }
      }
    }
  };

  return (
    <div>
      <div className="response">{response}</div>
      <div className="citations">
        {citations.map(c => (
          <div key={c.id}>{c.source_title} (p.{c.page_number})</div>
        ))}
      </div>
    </div>
  );
}
```

## Performance Comparison

### Regular Endpoint (/api/chat)
- Time to first byte: ~10 seconds
- Total time: ~10 seconds
- User waits: ~10 seconds

### Streaming Endpoint (/api/chat/stream)
- Time to first byte: ~1-2 seconds
- Total time: ~5-8 seconds
- **Perceived wait: ~1-2 seconds** ✨

## Additional Optimizations Applied

1. **Shorter system prompts**: ~75% fewer tokens
2. **Reduced max_tokens**: 500 (was 800)
3. **Shorter responses**: More concise, focused answers

## Expected Response Times

With all optimizations:
- **Streaming**: First tokens in 1-2s, complete in 5-8s
- **Regular**: Complete response in 5-8s (non-streaming)

## Fallback

The regular `/api/chat` endpoint still works if streaming is not desired.
