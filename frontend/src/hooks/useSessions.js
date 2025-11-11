import { useState, useEffect, useCallback } from 'react';
import { api } from '../utils/api';

export const useSessions = () => {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchSessions = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getSessions();
      setSessions(data);
    } catch (err) {
      console.error('Error fetching sessions:', err);
      setError(err.message || 'Failed to fetch sessions');
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteSession = useCallback(async (sessionId) => {
    try {
      await api.deleteSession(sessionId);
      setSessions(prev => prev.filter(s => s.id !== sessionId));
    } catch (err) {
      console.error('Error deleting session:', err);
      throw err;
    }
  }, []);

  const createSession = useCallback(async (data) => {
    try {
      const newSession = await api.createSession(data);
      setSessions(prev => [newSession, ...prev]);
      return newSession;
    } catch (err) {
      console.error('Error creating session:', err);
      throw err;
    }
  }, []);

  useEffect(() => {
    fetchSessions();
  }, [fetchSessions]);

  return {
    sessions,
    loading,
    error,
    fetchSessions,
    deleteSession,
    createSession
  };
};
