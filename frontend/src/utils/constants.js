export const AGENTS = {
  PROFESSIONAL_LEARNING: {
    id: 'professional_learning',
    name: 'Professional Learning Coach',
    description: 'Get guidance on PLC team dynamics, collaboration, and professional development',
    icon: '👥',
    color: 'st-blue'
  },
  CLASSROOM_CURRICULUM: {
    id: 'classroom_curriculum',
    name: 'Classroom Curriculum Planning Coach',
    description: 'Get support with curriculum design, standards alignment, and lesson planning',
    icon: '📚',
    color: 'st-green'
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
