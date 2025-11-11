import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Trash2, MessageSquare, Calendar, AlertCircle } from 'lucide-react';
import { useSessions } from '../hooks/useSessions';
import { useChat } from '../hooks/useChat';
import { formatDate } from '../utils/formatting';
import { AGENTS } from '../utils/constants';

const SessionsPage = () => {
  const navigate = useNavigate();
  const { sessions, loading, error, deleteSession } = useSessions();
  const { loadSession } = useChat();
  const [deletingId, setDeletingId] = useState(null);

  const handleLoadSession = async (sessionId) => {
    try {
      await loadSession(sessionId);
      navigate('/chat');
    } catch (err) {
      console.error('Error loading session:', err);
      alert('Failed to load session');
    }
  };

  const handleDeleteSession = async (sessionId, e) => {
    e.stopPropagation();

    const confirmed = window.confirm('Are you sure you want to delete this session?');
    if (!confirmed) return;

    try {
      setDeletingId(sessionId);
      await deleteSession(sessionId);
    } catch (err) {
      console.error('Error deleting session:', err);
      alert('Failed to delete session');
    } finally {
      setDeletingId(null);
    }
  };

  const getAgentInfo = (agentId) => {
    return Object.values(AGENTS).find(a => a.id === agentId) || AGENTS.PROFESSIONAL_LEARNING;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-st-blue border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading sessions...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-full p-4">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-3" />
          <h3 className="text-lg font-semibold text-red-800 text-center mb-2">
            Error Loading Sessions
          </h3>
          <p className="text-sm text-red-600 text-center">{error}</p>
        </div>
      </div>
    );
  }

  if (sessions.length === 0) {
    return (
      <div className="flex items-center justify-center h-full p-4">
        <div className="text-center max-w-md">
          <MessageSquare className="w-20 h-20 text-gray-300 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-700 mb-2">
            No Sessions Yet
          </h3>
          <p className="text-gray-600 mb-6">
            Your conversation sessions will appear here. Start a new chat to create your first session.
          </p>
          <button
            onClick={() => navigate('/chat')}
            className="px-6 py-3 bg-st-blue text-white rounded-lg hover:bg-st-blue-dark transition-colors"
          >
            Start Chatting
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full overflow-y-auto bg-gray-50">
      <div className="max-w-4xl mx-auto p-6">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-800 mb-2">Your Sessions</h1>
          <p className="text-gray-600">View and manage your coaching conversation history</p>
        </div>

        <div className="space-y-4">
          {sessions.map((session) => {
            const agent = getAgentInfo(session.agent_id);

            return (
              <div
                key={session.id}
                onClick={() => handleLoadSession(session.id)}
                className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-2xl">{agent.icon}</span>
                      <h3 className="font-semibold text-gray-800">{agent.name}</h3>
                    </div>

                    {session.title && (
                      <p className="text-sm text-gray-700 mb-2">{session.title}</p>
                    )}

                    <div className="flex items-center gap-4 text-sm text-gray-600">
                      <div className="flex items-center gap-1">
                        <Calendar className="w-4 h-4" />
                        <span>{formatDate(session.created_at || session.timestamp)}</span>
                      </div>

                      {session.message_count && (
                        <div className="flex items-center gap-1">
                          <MessageSquare className="w-4 h-4" />
                          <span>{session.message_count} messages</span>
                        </div>
                      )}
                    </div>
                  </div>

                  <button
                    onClick={(e) => handleDeleteSession(session.id, e)}
                    disabled={deletingId === session.id}
                    className="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-50"
                    title="Delete session"
                  >
                    {deletingId === session.id ? (
                      <div className="w-5 h-5 border-2 border-red-600 border-t-transparent rounded-full animate-spin"></div>
                    ) : (
                      <Trash2 className="w-5 h-5" />
                    )}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default SessionsPage;
