import { useEffect, useRef, useCallback } from 'react';
import { useChat } from '../../hooks/useChat';
import UserMessage from './UserMessage';
import AssistantMessage from './AssistantMessage';

const MessageList = ({ messages }) => {
  const { isStreaming, streamingContent, streamingCitations } = useChat();
  const messagesEndRef = useRef(null);
  const scrollTimeoutRef = useRef(null);

  const scrollToBottom = useCallback((smooth = true) => {
    if (scrollTimeoutRef.current) {
      cancelAnimationFrame(scrollTimeoutRef.current);
    }

    scrollTimeoutRef.current = requestAnimationFrame(() => {
      messagesEndRef.current?.scrollIntoView({
        behavior: smooth ? 'smooth' : 'auto',
        block: 'end'
      });
    });
  }, []);

  // Smooth scroll for new messages
  useEffect(() => {
    scrollToBottom(true);
  }, [messages, scrollToBottom]);

  // Throttled scroll during streaming
  useEffect(() => {
    if (isStreaming) {
      scrollToBottom(false); // Use auto for faster, less jerky scrolling
    }
  }, [streamingContent, isStreaming, scrollToBottom]);

  // Cleanup
  useEffect(() => {
    return () => {
      if (scrollTimeoutRef.current) {
        cancelAnimationFrame(scrollTimeoutRef.current);
      }
    };
  }, []);

  if (messages.length === 0 && !isStreaming) {
    return (
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="text-center max-w-md">
          <div className="text-6xl mb-4">💬</div>
          <h3 className="text-xl font-semibold text-gray-700 mb-2">
            Start a Conversation
          </h3>
          <p className="text-gray-600">
            Ask your AI coach any question about professional learning communities or curriculum planning.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4" style={{ overflowAnchor: 'auto' }}>
      {messages.map((message) => {
        if (message.role === 'user') {
          return <UserMessage key={message.id} message={message} />;
        } else if (message.role === 'assistant') {
          return <AssistantMessage key={message.id} message={message} />;
        } else if (message.role === 'system' && message.error) {
          return (
            <div key={message.id} className="flex justify-center">
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-2 rounded-lg text-sm">
                {message.content}
              </div>
            </div>
          );
        }
        return null;
      })}

      {/* Streaming Response */}
      {isStreaming && (
        <AssistantMessage
          message={{
            id: 'streaming',
            role: 'assistant',
            content: streamingContent,
            citations: streamingCitations,
            streaming: true,
            timestamp: new Date().toISOString()
          }}
        />
      )}

      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;
