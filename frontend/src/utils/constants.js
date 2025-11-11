export const AGENTS = {
  PROFESSIONAL_LEARNING: {
    id: 'professional_learning',
    name: 'Professional Learning Coach',
    description: 'Team collaboration & PLC best practices',
    icon: 'Users',
    color: 'st-blue',
    welcomeMessage: `Welcome! I'm your Professional Learning Coach, here to help you build effective Professional Learning Communities.

Here are some questions I can help you with:

• How do we establish norms for our PLC team meetings?
• What are the four critical questions every PLC should address?
• How can we improve collaboration within our teaching team?
• What strategies help teams focus on student learning outcomes?

Feel free to ask me anything about PLC team dynamics, collaboration, or professional development!`
  },
  CLASSROOM_CURRICULUM: {
    id: 'classroom_curriculum',
    name: 'Curriculum Planning Coach',
    description: 'Standards-aligned lesson design',
    icon: 'BookOpen',
    color: 'st-green',
    welcomeMessage: `Welcome! I'm your Curriculum Planning Coach, here to help you design effective, standards-aligned curriculum.

Here are some questions I can help you with:

• How do I write SMART goals for my students?
• What's the best way to align my curriculum with state standards?
• How can I use backward design in lesson planning?
• What makes an effective learning target or essential standard?

Ask me anything about curriculum design, standards alignment, or instructional planning!`
  }
};

export const API_ENDPOINTS = {
  AUTH_VERIFY: '/api/auth/verify',
  CHAT: '/api/chat',
  SESSIONS: '/api/sessions',
  FEEDBACK: '/api/feedback',
  AGENTS: '/api/agents'
};

export const MESSAGE_ROLES = {
  USER: 'user',
  ASSISTANT: 'assistant',
  SYSTEM: 'system'
};

export const RATING_OPTIONS = [
  { value: 1, label: '⭐' },
  { value: 2, label: '⭐⭐' },
  { value: 3, label: '⭐⭐⭐' },
  { value: 4, label: '⭐⭐⭐⭐' },
  { value: 5, label: '⭐⭐⭐⭐⭐' }
];
