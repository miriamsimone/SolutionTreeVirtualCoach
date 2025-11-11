import { useEffect, useRef } from 'react';
import UserMessage from './UserMessage';
import AssistantMessage from './AssistantMessage';

const MessageList = ({ messages, isLoading }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  if (messages.length === 0 && !isLoading) {
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
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
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

      {isLoading && (
        <div className="flex justify-start items-start gap-3 mb-4">
          <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-st-blue to-st-blue-dark flex items-center justify-center text-white">
            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          </div>
          <div className="bg-white border border-gray-200 rounded-lg rounded-tl-sm px-4 py-3 shadow-sm">
            <div className="flex gap-1">
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
            </div>
          </div>
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;
