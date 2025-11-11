import { createContext, useState, useCallback, useEffect } from 'react';
import { api } from '../utils/api';
import { AGENTS } from '../utils/constants';

export const ChatContext = createContext(null);

export const ChatProvider = ({ children }) => {
  const [messages, setMessages] = useState([]);
  const [currentAgent, setCurrentAgent] = useState(AGENTS.PROFESSIONAL_LEARNING.id);
  const [initialized, setInitialized] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamingContent, setStreamingContent] = useState('');
  const [streamingCitations, setStreamingCitations] = useState([]);
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
    setIsStreaming(true);
    setStreamingContent('');
    setStreamingCitations([]);
    setError(null);

    // Use refs to capture current values
    let currentContent = '';
    let currentCitations = [];
    let currentMessageId = null;

    try {
      await api.streamMessage({
        agent_id: currentAgent,
        query,
        session_id: sessionId,

        onCitations: (data) => {
          // Citations arrive first
          currentCitations = data.citations || [];
          currentMessageId = data.message_id;

          setStreamingCitations(currentCitations);

          // Update session ID if provided
          if (data.session_id && !sessionId) {
            setSessionId(data.session_id);
          }
        },

        onContent: (chunk) => {
          // Append each chunk to build the response
          currentContent += chunk;
          setStreamingContent(currentContent);
        },

        onDone: () => {
          // Streaming complete - add to message history using captured values
          const assistantMessage = {
            id: currentMessageId || Date.now().toString() + '-ai',
            role: 'assistant',
            content: currentContent,
            citations: currentCitations,
            agent_used: currentAgent,
            timestamp: new Date().toISOString()
          };

          setMessages(prev => [...prev, assistantMessage]);

          // Clear streaming state after a small delay to avoid flicker
          setTimeout(() => {
            setIsStreaming(false);
            setStreamingContent('');
            setStreamingCitations([]);
          }, 100);
        },

        onError: (errorMsg) => {
          console.error('Streaming error:', errorMsg);
          setError(errorMsg);
          setIsStreaming(false);

          // Add error message to chat
          const errorMessage = {
            id: Date.now().toString() + '-error',
            role: 'system',
            content: 'Sorry, I encountered an error. Please try again.',
            error: true,
            timestamp: new Date().toISOString()
          };

          setMessages(prev => [...prev, errorMessage]);
        }
      });
    } catch (err) {
      console.error('Error sending message:', err);
      setError(err.message || 'Failed to send message');
      setIsStreaming(false);

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
    }
  }, [currentAgent, sessionId]);

  const switchAgent = useCallback((agentId) => {
    setCurrentAgent(agentId);

    // Add welcome message from the new agent
    const agent = Object.values(AGENTS).find(a => a.id === agentId);
    if (agent && agent.welcomeMessage) {
      const welcomeMessage = {
        id: Date.now().toString() + '-welcome',
        role: 'assistant',
        content: agent.welcomeMessage,
        agent_used: agentId,
        timestamp: new Date().toISOString(),
        isWelcome: true
      };
      setMessages([welcomeMessage]);
    }
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

  // Initialize with welcome message on first load
  useEffect(() => {
    if (!initialized && messages.length === 0) {
      const agent = Object.values(AGENTS).find(a => a.id === currentAgent);
      if (agent && agent.welcomeMessage) {
        const welcomeMessage = {
          id: 'initial-welcome',
          role: 'assistant',
          content: agent.welcomeMessage,
          agent_used: currentAgent,
          timestamp: new Date().toISOString(),
          isWelcome: true
        };
        setMessages([welcomeMessage]);
      }
      setInitialized(true);
    }
  }, [initialized, messages.length, currentAgent]);

  const value = {
    messages,
    currentAgent,
    sessionId,
    isLoading,
    isStreaming,
    streamingContent,
    streamingCitations,
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
