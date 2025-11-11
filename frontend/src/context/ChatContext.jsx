import { createContext, useState, useCallback } from 'react';
import { api } from '../utils/api';
import { AGENTS } from '../utils/constants';

export const ChatContext = createContext(null);

export const ChatProvider = ({ children }) => {
  const [messages, setMessages] = useState([]);
  const [currentAgent, setCurrentAgent] = useState(AGENTS.PROFESSIONAL_LEARNING.id);
  const [sessionId, setSessionId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendMessage = useCallback(async (query) => {
    if (!query.trim()) return;

    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: query,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await api.sendMessage({
        agent_id: currentAgent,
        query,
        session_id: sessionId
      });

      const assistantMessage = {
        id: Date.now().toString() + '-ai',
        role: 'assistant',
        content: response.response,
        citations: response.citations || [],
        agent_used: response.agent_used,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Update session ID if returned
      if (response.session_id && !sessionId) {
        setSessionId(response.session_id);
      }

      return assistantMessage;
    } catch (err) {
      console.error('Error sending message:', err);
      setError(err.message || 'Failed to send message');

      // Add error message to chat
      const errorMessage = {
        id: Date.now().toString() + '-error',
        role: 'system',
        content: 'Sorry, I encountered an error. Please try again.',
        error: true,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, errorMessage]);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [currentAgent, sessionId]);

  const switchAgent = useCallback((agentId) => {
    setCurrentAgent(agentId);
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setSessionId(null);
    setError(null);
  }, []);

  const loadSession = useCallback(async (sessionIdToLoad) => {
    try {
      setIsLoading(true);
      const sessionData = await api.getSession(sessionIdToLoad);

      setSessionId(sessionData.id);
      setMessages(sessionData.messages || []);
      setCurrentAgent(sessionData.agent_id || AGENTS.PROFESSIONAL_LEARNING.id);
      setError(null);
    } catch (err) {
      console.error('Error loading session:', err);
      setError('Failed to load session');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const value = {
    messages,
    currentAgent,
    sessionId,
    isLoading,
    error,
    sendMessage,
    switchAgent,
    clearMessages,
    loadSession
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
};
