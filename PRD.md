# AI Powered PLC at Work Virtual Coach

**Organization:** Solution Tree  
**Project ID:** QS6bbY3IK5hYXLdWZ9sB_1762208994432  
**Timeline:** Complete by end of day (started ~12 PM)

---

# Product Requirements Document (PRD) - UPDATED

## 1. Executive Summary

The **AI Powered PLC at Work Virtual Coach** is an AI-driven solution by Solution Tree, designed to support educators in Professional Learning Communities (PLCs) by providing on-demand, context-aware coaching through two specialized agents: a **Professional Learning Coach** and a **Classroom Curriculum Planning Coach**. Each agent uses metadata-filtered access to a curated corpus of Solution Tree titles, delivering personalized guidance grounded in PLC frameworks and curriculum best practices.

## 2. Problem Statement

Collaborative teams in PLCs struggle to consistently apply best practices due to inaccessibility of vital guidance. This solution creates two specialized AI coaching assistants that deliver real-time, context-specific advice tailored to educators' needs—one focused on PLC team dynamics and processes, the other on curriculum planning and standards implementation.

## 3. Goals & Success Metrics

- **User Engagement**: Educators actively using both agents for different coaching needs
- **Resolution Rate**: High percentage of user inquiries satisfactorily resolved within context
- **User Satisfaction Score**: Average rating of 4.5/5 or above (via response rating component)
- **Content Utilization**: Appropriate routing and use of agent-specific documents
- **Response Accuracy**: Minimal hallucinations, high relevance to queries
- **Time to Assistance**: Low latency responses (seconds)
- **Citation Coverage**: Visible document and source citations in responses
- **Agent Routing Accuracy**: Correct agent selection and metadata filtering

## 4. Target Users & Personas

- **Educators**: Teachers and team leaders needing practical PLC guidance and curriculum planning support
- **School Administrators**: Overseeing PLC implementation and seeking data-driven coaching insights
- **Instructional Coaches**: Supporting educators with customized, AI-enhanced coaching

### Needs/Pain Points
- Immediate access to applicable strategies during PLC meetings
- Clear, filtered guidance appropriate to current task (team process vs. curriculum planning)
- Consistent application of frameworks to improve student outcomes

## 5. User Stories

1. **As an educator in a PLC meeting**, I want to switch to the Professional Learning Coach and get real-time advice on team collaboration so that we can work more effectively together.

2. **As a teacher planning curriculum**, I want to switch to the Classroom Curriculum Planning Coach and get standards-aligned guidance so that I can design better learning experiences.

3. **As a school administrator**, I want to see which coaching agents are being used and get basic usage feedback so that I can understand what types of support educators value most.

## 6. Functional Requirements

### P0: Must-have
- **Authentication**: Google OAuth via Firebase with JIT provisioning
- **Two AI Agents**: Professional Learning Coach and Classroom Curriculum Planning Coach with distinct personalities and metadata filtering
- **Agent Switcher UI**: Easy toggle between agents in the interface
- **RAG System**: Pinecone-backed retrieval with metadata filtering for agent-specific documents
- **Response Generation**: Grounded answers with visible citations from source documents
- **Simple Rating Component**: Users can rate responses (1-5 stars or thumbs up/down)

### P1: Should-have
- **Multi-turn Conversations**: Support follow-up questions within a session
- **Session History**: Save conversation sessions for future reference
- **Firebase Logging**: Basic logging of agent usage and user interactions
- **Mocked Admin Analytics**: Placeholder dashboard showing usage patterns

### P2: Nice-to-have
- **Firebase Analytics Dashboard**: Real tracking of user engagement metrics
- **Advanced Feedback Mechanism**: Detailed feedback on response quality
- **Export Sessions**: Allow users to download conversation history

## 7. Non-Functional Requirements

- **Performance**: Response time within 2-3 seconds; support 50+ concurrent users
- **Security**: Data privacy via Firebase auth, secure API communication, role-based access
- **Scalability**: Modular architecture for adding new agents or documents
- **Compliance**: Alignment with FERPA and educational data standards

## 8. User Experience & Design Considerations

- **Intuitive Interface**: Clean chat interface with visible agent switcher
- **Accessibility**: WCAG 2.1 AA compliance for diverse user needs
- **Feedback Integration**: Simple, non-intrusive rating mechanism
- **Responsive Design**: Works seamlessly on desktop and tablet devices

## 9. Technical Stack

- **Frontend**: React with Vite, TailwindCSS for styling
- **Backend**: Python FastAPI with async support
- **RAG Database**: Pinecone vector store with metadata filtering
- **AI Model**: OpenAI API (GPT-4 or latest available)
- **Hosting**: Firebase (Hosting, Authentication, Realtime Database for sessions)
- **Monitoring**: Firebase Analytics and Logging (best effort)
- **Authentication**: Google OAuth via Firebase

## 10. Data & Content

### Curated Source Documents (6 titles)
1. Behavior Academies
2. Learning by Doing
3. The Way Forward
4. Essential Standards Second Grade Mathematics
5. American Government Smart Goals Worksheet
6. Third Grade Team Smart Goal

### Agent-Specific Metadata Tagging
- **Professional Learning Coach**: Focus on Behavior Academies, Learning by Doing, The Way Forward
- **Classroom Curriculum Planning Coach**: Focus on Essential Standards Second Grade Mathematics, American Government Smart Goals Worksheet, Third Grade Team Smart Goal

(Note: Overlap is acceptable; filtering is by primary relevance)

## 11. Dependencies & Assumptions

- Access to Solution Tree's curated titles for ingestion
- OpenAI API account and quota
- Firebase project setup (auth, hosting, database)
- Pinecone account and API key
- Assumed user familiarity with basic digital tools

## 12. Out of Scope

- Development of new content outside existing Solution Tree titles
- Integration with external educational platforms
- Real-time collaborative editing features
- Complex role-based hierarchies (admin panels are mocked)

## Integration Checklist

- [ ] Backend FastAPI server running and accessible
- [ ] Pinecone index populated with embeddings and metadata
- [ ] Frontend connected to backend API with auth working
- [ ] Agent switcher updates metadata filters in Pinecone queries
- [ ] Citations rendering correctly in chat messages
- [ ] Rating component sending feedback to backend
- [ ] Session history saving and loading
- [ ] Firebase auth tokens validating on backend
- [ ] Error handling working across all three components

