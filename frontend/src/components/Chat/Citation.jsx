import { useState } from 'react';
import { ChevronDown, ChevronUp, BookOpen } from 'lucide-react';

const Citation = ({ citation, index }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="border border-st-blue/30 rounded-lg bg-st-blue-light/10 p-3 hover:shadow-md transition-shadow">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-start gap-3 text-left"
      >
        <div className="flex-shrink-0 w-6 h-6 rounded-full bg-st-blue text-white flex items-center justify-center text-xs font-semibold">
          {index + 1}
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <BookOpen className="w-4 h-4 text-st-blue flex-shrink-0" />
            <h4 className="font-semibold text-sm text-gray-800 truncate">
              {citation.source_title}
            </h4>
            {citation.page_number && (
              <span className="text-xs text-gray-600 flex-shrink-0">
                p. {citation.page_number}
              </span>
            )}
          </div>

          {citation.relevance_score && (
            <div className="flex items-center gap-2 mb-2">
              <div className="flex-1 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-st-green transition-all duration-300"
                  style={{ width: `${citation.relevance_score * 100}%` }}
                />
              </div>
              <span className="text-xs text-gray-600 flex-shrink-0">
                {Math.round(citation.relevance_score * 100)}%
              </span>
            </div>
          )}
        </div>

        <div className="flex-shrink-0">
          {isExpanded ? (
            <ChevronUp className="w-5 h-5 text-gray-500" />
          ) : (
            <ChevronDown className="w-5 h-5 text-gray-500" />
          )}
        </div>
      </button>

      {isExpanded && citation.chunk_text && (
        <div className="mt-3 pt-3 border-t border-st-blue/20">
          <p className="text-sm text-gray-700 leading-relaxed italic">
            &ldquo;{citation.chunk_text}&rdquo;
          </p>
        </div>
      )}
    </div>
  );
};

export default Citation;
