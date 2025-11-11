## Task List 2: Frontend (React + Vite)

**Owner:** Frontend Engineer  
**Parallel Start:** Immediately

### Project Structure
```
frontend/
├── src/
│   ├── index.css                  [CREATE]
│   ├── App.jsx                    [CREATE]
│   ├── main.jsx                   [CREATE]
│   ├── config/
│   │   ├── firebase.js            [CREATE]
│   │   ├── api.js                 [CREATE]
│   ├── components/
│   │   ├── Layout/
│   │   │   ├── Header.jsx         [CREATE]
│   │   │   ├── Sidebar.jsx        [CREATE]
│   │   ├── Chat/
│   │   │   ├── ChatWindow.jsx     [CREATE]
│   │   │   ├── MessageList.jsx    [CREATE]
│   │   │   ├── UserMessage.jsx    [CREATE]
│   │   │   ├── AssistantMessage.jsx [CREATE]
│   │   │   ├── Citation.jsx       [CREATE]
│   │   ├── Agent/
│   │   │   ├── AgentSwitcher.jsx  [CREATE]
│   │   │   ├── AgentButton.jsx    [CREATE]
│   │   ├── Feedback/
│   │   │   ├── RatingComponent.jsx [CREATE]
│   │   ├── Auth/
│   │   │   ├── LoginPage.jsx      [CREATE]
│   │   │   ├── GoogleAuthButton.jsx [CREATE]
│   │   │   ├── MockAuthButtons.jsx [CREATE]
│   │   ├── Analytics/
│   │   │   ├── AnalyticsDashboard.jsx [CREATE - MOCKED]
│   ├── hooks/
│   │   ├── useAuth.js             [CREATE]
│   │   ├── useChat.js             [CREATE]
│   │   ├── useSessions.js         [CREATE]
│   ├── context/
│   │   ├── AuthContext.jsx        [CREATE]
│   │   ├── ChatContext.jsx        [CREATE]
│   ├── pages/
│   │   ├── ChatPage.jsx           [CREATE]
│   │   ├── AnalyticsPage.jsx      [CREATE - MOCKED]
│   │   ├── SessionsPage.jsx       [CREATE]
│   ├── utils/
│   │   ├── api.js                 [CREATE]
│   │   ├── formatting.js          [CREATE]
│   │   ├── constants.js           [CREATE]
├── public/
│   ├── index.html                 [CREATE]
├── package.json                   [CREATE]
├── vite.config.js                 [CREATE]
├── tailwind.config.js             [CREATE]
├── .env.example                   [CREATE]
└── README.md                      [CREATE]
```

### Key Deliverables

1. **Authentication Flow** (`components/Auth/` + `hooks/useAuth.js`)
   - Google OAuth login button (real Firebase integration)
   - Mock additional auth buttons (display only, non-functional)
   - Session persistence
   - Logout functionality

2. **Agent Switcher** (`components/Agent/`)
   - Toggle between Professional Learning Coach and Classroom Curriculum Planning Coach
   - Visual indication of active agent
   - Persist agent selection in local state

3. **Chat Interface** (`components/Chat/` + `pages/ChatPage.jsx`)
   - Message input field with send button
   - Real-time message display (user + assistant)
   - Typing indicators during API calls
   - Conversation history in current session

4. **Message Rendering** (`components/Chat/AssistantMessage.jsx`)
   - Parse and display assistant responses
   - Extract and render citations as clickable/expandable components
   - Format code blocks, lists, and text appropriately

5. **Citation Component** (`components/Chat/Citation.jsx`)
   - Display source document and page/section reference
   - Expandable to show surrounding context (optional)
   - Visual styling to distinguish citations

6. **Response Rating** (`components/Feedback/RatingComponent.jsx`)
   - Simple 1-5 star or thumbs up/down rating UI
   - Only visible after assistant response
   - Send rating to backend on selection

7. **Session Management** (`pages/SessionsPage.jsx` + `hooks/useSessions.js`)
   - Display list of past conversations
   - Load previous session by clicking
   - Show session metadata (date, agent used, message count)

8. **Mocked Analytics Dashboard** (`pages/AnalyticsPage.jsx`)
   - Display placeholder metrics (e.g., "Total Queries: --", "Top Agents: --")
   - No real data collection yet (ready for Firebase integration)
   - Simple visual layout (cards/charts)

9. **Layout & Navigation** (`components/Layout/`)
   - Responsive header with logo and user profile
   - Navigation between chat, sessions, and analytics pages
   - Mobile-friendly layout

10. **API Client** (`utils/api.js` + `config/api.js`)
    - Centralized API calls to backend
    - Automatic token injection in headers
    - Error handling and retry logic

### Files to Edit During Development
- `package.json` — Add dependencies (react, vite, tailwindcss, firebase, axios, etc.)
- `.env.example` — Document Firebase config keys and API endpoint

### Integration Points
- Backend endpoints: `/chat`, `/auth/verify`, `/sessions`, `/feedback`
- Firebase for authentication and session storage
- TailwindCSS for consistent styling

---
