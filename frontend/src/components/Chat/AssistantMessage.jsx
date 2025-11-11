import { useState } from 'react';
import { Bot } from 'lucide-react';
import { formatRelativeTime } from '../../utils/formatting';
import Citation from './Citation';
import RatingComponent from '../Feedback/RatingComponent';

const AssistantMessage = ({ message }) => {
  const [hasRated, setHasRated] = useState(false);

  const handleRatingSubmit = () => {
    setHasRated(true);
  };

  return (
    <div className="flex justify-start items-start gap-3 mb-4">
      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-st-blue to-st-blue-dark flex items-center justify-center text-white">
        <Bot className="w-5 h-5" />
      </div>

      <div className="max-w-[70%] flex-1">
        <div className="bg-white border border-gray-200 rounded-lg rounded-tl-sm px-4 py-3 shadow-sm">
          <p className="text-sm text-gray-800 leading-relaxed whitespace-pre-wrap break-words">
            {message.content}
          </p>
        </div>

        {/* Citations */}
        {message.citations && message.citations.length > 0 && (
          <div className="mt-3 space-y-2">
            <h4 className="text-xs font-semibold text-gray-600 uppercase tracking-wide">
              Sources ({message.citations.length})
            </h4>
            {message.citations.map((citation, index) => (
              <Citation key={citation.id || index} citation={citation} index={index} />
            ))}
          </div>
        )}

        {/* Timestamp and Rating */}
        <div className="flex items-center justify-between mt-2">
          {message.timestamp && (
            <p className="text-xs text-gray-500">
              {formatRelativeTime(message.timestamp)}
              {message.agent_used && (
                <span className="ml-2 text-gray-400">· {message.agent_used}</span>
              )}
            </p>
          )}

          {!hasRated && !message.error && (
            <RatingComponent
              messageId={message.id}
              onRatingSubmit={handleRatingSubmit}
            />
          )}
        </div>

        {hasRated && (
          <p className="text-xs text-st-green mt-1">Thank you for your feedback!</p>
        )}
      </div>
    </div>
  );
};

export default AssistantMessage;
