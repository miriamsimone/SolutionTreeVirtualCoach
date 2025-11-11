import { useState } from 'react';
import { Send } from 'lucide-react';
import { useChat } from '../../hooks/useChat';
import MessageList from './MessageList';

const ChatWindow = () => {
  const [input, setInput] = useState('');
  const { messages, sendMessage, isLoading } = useChat();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const messageText = input.trim();
    setInput('');

    try {
      await sendMessage(messageText);
    } catch (err) {
      console.error('Error sending message:', err);
      // Error is already handled in ChatContext
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="flex flex-col h-full bg-gray-50">
      <MessageList messages={messages} isLoading={isLoading} />

      {/* Input Area */}
      <div className="border-t border-gray-200 bg-white p-4">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
          <div className="flex gap-2">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask your coach a question..."
              disabled={isLoading}
              rows={1}
              className="flex-1 resize-none border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-st-blue focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
              style={{
                minHeight: '48px',
                maxHeight: '150px'
              }}
              onInput={(e) => {
                e.target.style.height = 'auto';
                e.target.style.height = e.target.scrollHeight + 'px';
              }}
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="px-6 py-3 bg-st-blue text-white rounded-lg hover:bg-st-blue-dark transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center gap-2 font-medium"
            >
              {isLoading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Sending...</span>
                </>
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  <span>Send</span>
                </>
              )}
            </button>
          </div>

          <p className="text-xs text-gray-500 mt-2 text-center">
            Press Enter to send, Shift+Enter for new line
          </p>
        </form>
      </div>
    </div>
  );
};

export default ChatWindow;
