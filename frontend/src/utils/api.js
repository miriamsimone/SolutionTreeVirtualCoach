import axios from 'axios';
import { auth } from '../config/firebase';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  async (config) => {
    try {
      const user = auth.currentUser;
      if (user) {
        const token = await user.getIdToken();
        config.headers.Authorization = `Bearer ${token}`;
      }
    } catch (error) {
      console.error('Error getting auth token:', error);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;

      if (status === 401) {
        // Unauthorized - possibly token expired
        console.error('Authentication error:', data);
        // Could trigger logout here
      } else if (status === 429) {
        // Rate limit
        console.error('Rate limit exceeded');
      } else if (status === 500) {
        // Server error - log but don't block user
        console.error('Server error (500):', data);
      }

      return Promise.reject({
        message: data.detail || data.message || 'An error occurred',
        status,
        data
      });
    } else if (error.request) {
      // Request made but no response
      console.error('No response from server');
      return Promise.reject({
        message: 'No response from server. Please check your connection.',
        status: 0
      });
    } else if (error.code === 'ERR_NETWORK') {
      // Network error
      console.error('Network error - backend may not be running');
      return Promise.reject({
        message: 'Cannot connect to backend. Please ensure the backend server is running.',
        status: 0
      });
    } else {
      // Something else happened
      return Promise.reject({
        message: error.message || 'An unexpected error occurred',
        status: 0
      });
    }
  }
);

// API methods
export const api = {
  // Auth
  verifyToken: async () => {
    const response = await apiClient.post('/api/auth/verify');
    return response.data;
  },

  // Chat
  sendMessage: async ({ agent_id, query, session_id = null }) => {
    const response = await apiClient.post('/api/chat', {
      agent_id,
      query,
      session_id
    });
    return response.data;
  },

  // Streaming Chat
  streamMessage: async ({ agent_id, query, session_id = null, onCitations, onContent, onDone, onError }) => {
    try {
      const user = auth.currentUser;
      const token = user ? await user.getIdToken() : null;

      const response = await fetch(`${import.meta.env.VITE_BACKEND_API_URL}/api/chat/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : ''
        },
        body: JSON.stringify({
          query,
          agent_id,
          session_id
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || ''; // Keep incomplete line in buffer

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));

              switch (data.type) {
                case 'citations':
                  if (onCitations) onCitations(data);
                  break;
                case 'content':
                  if (onContent) onContent(data.content);
                  break;
                case 'done':
                  if (onDone) onDone();
                  return;
                case 'error':
                  if (onError) onError(data.error);
                  return;
              }
            } catch (parseError) {
              console.error('Error parsing SSE data:', parseError, line);
            }
          }
        }
      }
    } catch (error) {
      console.error('Streaming error:', error);
      if (onError) onError(error.message || 'Streaming failed');
      throw error;
    }
  },

  // Sessions
  getSessions: async () => {
    const response = await apiClient.get('/api/sessions');
    return response.data;
  },

  getSession: async (sessionId) => {
    const response = await apiClient.get(`/api/sessions/${sessionId}`);
    return response.data;
  },

  createSession: async (data) => {
    const response = await apiClient.post('/api/sessions', data);
    return response.data;
  },

  deleteSession: async (sessionId) => {
    const response = await apiClient.delete(`/api/sessions/${sessionId}`);
    return response.data;
  },

  // Feedback
  submitFeedback: async ({ session_id, message_id, rating, comment = null }) => {
    const response = await apiClient.post('/api/feedback', {
      session_id,
      message_id,
      rating,
      comment
    });
    return response.data;
  },

  // Agents
  getAgents: async () => {
    const response = await apiClient.get('/api/agents');
    return response.data;
  },

  // Analytics
  getAnalytics: async () => {
    const response = await apiClient.get('/api/analytics');
    return response.data;
  }
};

export default apiClient;
