# Solution Tree Virtual Coach - Frontend

AI-powered PLC coaching application built with React, Vite, and TailwindCSS.

## Features

- **Dual AI Coaching Agents**
  - Professional Learning Coach
  - Classroom Curriculum Planning Coach

- **Authentication**
  - Google OAuth via Firebase
  - Secure token-based API communication

- **Interactive Chat Interface**
  - Real-time messaging
  - Citation display with expandable context
  - Response rating system

- **Session Management**
  - Save and load conversation history
  - View past sessions
  - Delete old sessions

- **Analytics Dashboard** (Mocked)
  - Usage metrics placeholder
  - Ready for Firebase Analytics integration

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **TailwindCSS** - Utility-first CSS framework
- **Firebase** - Authentication and database
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Lucide React** - Icon library

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend API running on `http://localhost:8000`
- Firebase project configured

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
VITE_FIREBASE_API_KEY=your_api_key
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_AUTH_DOMAIN=your_auth_domain
VITE_FIREBASE_DATABASE_URL=your_database_url
VITE_BACKEND_API_URL=http://localhost:8000
```

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Agent/          # Agent switcher components
│   ├── Auth/           # Authentication components
│   ├── Chat/           # Chat interface components
│   ├── Feedback/       # Rating component
│   └── Layout/         # Header, Sidebar
├── context/            # React context providers
├── hooks/              # Custom React hooks
├── pages/              # Main page components
├── utils/              # Utilities and helpers
└── config/             # Configuration files
```

## Key Components

### Authentication
- Google OAuth integration
- JWT token management
- Protected routes

### Chat Interface
- Real-time messaging
- Agent switching
- Citation rendering
- Response ratings

### Session Management
- Load previous conversations
- Delete sessions
- View session metadata

## API Integration

The frontend communicates with the backend via REST API:

- `POST /api/auth/verify` - Verify Firebase token
- `POST /api/chat` - Send message, get response
- `GET /api/sessions` - Fetch all sessions
- `GET /api/sessions/:id` - Get specific session
- `DELETE /api/sessions/:id` - Delete session
- `POST /api/feedback` - Submit rating

## Development

```bash
# Run with hot reload
npm run dev

# Lint code
npm run lint
```

## Deployment

```bash
# Build for production
npm run build

# The dist/ folder contains the production build
# Deploy to Firebase Hosting, Vercel, or any static host
```

## Accessibility

- WCAG 2.1 AA compliant
- Keyboard navigation support
- Screen reader friendly
- Proper ARIA labels

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## License

Proprietary - Solution Tree
