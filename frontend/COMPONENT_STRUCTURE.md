# Component Structure & Data Flow

## Component Hierarchy

```
App.jsx (Root)
├── AuthProvider (Context)
│   └── ChatProvider (Context)
│       └── Router
│           ├── LoginPage (/login)
│           │   ├── GoogleAuthButton
│           │   └── MockAuthButtons
│           │
│           └── MainLayout (Protected Routes)
│               ├── Header
│               │   └── User Profile + Sign Out
│               ├── Sidebar
│               │   └── Navigation Links
│               └── Main Content Area
│                   ├── ChatPage (/chat)
│                   │   ├── AgentSwitcher
│                   │   │   └── AgentButton (x2)
│                   │   └── ChatWindow
│                   │       ├── MessageList
│                   │       │   ├── UserMessage (multiple)
│                   │       │   └── AssistantMessage (multiple)
│                   │       │       ├── Citation (multiple)
│                   │       │       └── RatingComponent
│                   │       └── Input Form
│                   │
│                   ├── SessionsPage (/sessions)
│                   │   └── Session List
│                   │       └── Session Cards
│                   │
│                   └── AnalyticsPage (/analytics)
│                       ├── Stats Cards
│                       ├── Agent Usage Chart
│                       └── Recent Activity
```

## Data Flow

### Authentication Flow
```
1. User clicks "Sign in with Google"
2. GoogleAuthButton → Firebase Auth
3. Firebase returns user token
4. AuthContext verifies token with backend (/api/auth/verify)
5. User object stored in AuthContext
6. Protected routes now accessible
```

### Chat Message Flow
```
1. User types message in ChatWindow
2. ChatWindow → useChat hook → sendMessage()
3. ChatContext sends to API (/api/chat) with:
   - agent_id (from currentAgent)
   - query (user message)
   - session_id (if exists)
4. Backend returns response with:
   - response text
   - citations array
   - session_id
   - agent_used
5. ChatContext updates messages array
6. MessageList re-renders with new messages
7. AssistantMessage displays with Citations
8. User can rate response via RatingComponent
```

### Agent Switching Flow
```
1. User clicks agent in AgentSwitcher
2. AgentSwitcher → ChatPage → useChat hook
3. Confirmation dialog appears (if messages exist)
4. clearMessages() resets conversation
5. switchAgent(newAgentId) updates currentAgent
6. Next message uses new agent_id
```

### Session Management Flow
```
1. SessionsPage loads → useSessions hook
2. useSessions → fetchSessions() → API (/api/sessions)
3. Sessions displayed in list
4. User clicks session
5. loadSession(sessionId) → API (/api/sessions/:id)
6. ChatContext populates messages from session
7. Navigate to /chat to view
```

## Context Structure

### AuthContext
```javascript
{
  user: {
    uid, email, displayName, photoURL
  },
  loading: boolean,
  error: string,
  signInWithGoogle: () => Promise,
  signOut: () => Promise,
  isAuthenticated: boolean
}
```

### ChatContext
```javascript
{
  messages: Array<Message>,
  currentAgent: 'professional_learning' | 'classroom_curriculum',
  sessionId: string,
  isLoading: boolean,
  error: string,
  sendMessage: (query) => Promise,
  switchAgent: (agentId) => void,
  clearMessages: () => void,
  loadSession: (sessionId) => Promise
}
```

## API Integration Points

### Request Format
```javascript
// Chat Request
POST /api/chat
{
  agent_id: "professional_learning",
  query: "How do we...",
  session_id: "uuid-or-null"
}

// Response
{
  response: "Based on...",
  citations: [{
    id, source_title, page_number,
    chunk_text, relevance_score
  }],
  agent_used: "professional_learning",
  session_id: "uuid"
}

// Feedback Request
POST /api/feedback
{
  session_id: "uuid",
  message_id: "msg-id",
  rating: 5,
  comment: null
}
```

## State Management

### Local State
- Component UI state (expanded, loading, etc.)
- Form inputs
- Sidebar open/close

### Context State
- Authentication (AuthContext)
- Chat messages and current agent (ChatContext)

### Server State (via hooks)
- Sessions list (useSessions)
- Individual session data (API calls)

## Styling Approach

### TailwindCSS Utilities
- Responsive breakpoints (sm, md, lg)
- Custom color palette (st-blue, st-green, etc.)
- Hover states and transitions
- Focus states for accessibility

### Custom CSS
- Scrollbar styling
- Animation keyframes
- Global resets

## Error Handling

### Levels
1. **Network Errors**: Caught in API interceptor
2. **API Errors**: Displayed in UI via error states
3. **Auth Errors**: Redirect to login
4. **Form Validation**: Inline validation messages

### User Feedback
- Toast notifications (future)
- Inline error messages
- Loading states
- Confirmation dialogs
