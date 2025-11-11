import { useState } from 'react';
import { ChevronDown, ChevronUp, BookOpen } from 'lucide-react';

const Citation = ({ citations, index }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  // citations is now an array of citations from the same source
  const sourceTitle = citations[0].source_title;
  const pages = citations.map(c => c.page_number).filter(Boolean).sort((a, b) => a - b);
  const avgRelevance = citations.reduce((sum, c) => sum + (c.relevance_score || 0), 0) / citations.length;

  // Format page numbers nicely (e.g., "p. 4, 5, 13, 41, 47")
  const formatPages = (pageNumbers) => {
    if (pageNumbers.length === 0) return '';
    if (pageNumbers.length === 1) return `p. ${pageNumbers[0]}`;
    return `pp. ${pageNumbers.join(', ')}`;
  };

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
              {sourceTitle}
            </h4>
            {pages.length > 0 && (
              <span className="text-xs text-gray-600 flex-shrink-0">
                {formatPages(pages)}
              </span>
            )}
          </div>

          <div className="flex items-center gap-2 mb-2">
            <div className="flex-1 h-1.5 bg-gray-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-st-green transition-all duration-300"
                style={{ width: `${avgRelevance * 100}%` }}
              />
            </div>
            <span className="text-xs text-gray-600 flex-shrink-0">
              {Math.round(avgRelevance * 100)}%
            </span>
          </div>
        </div>

        <div className="flex-shrink-0">
          {isExpanded ? (
            <ChevronUp className="w-5 h-5 text-gray-500" />
          ) : (
            <ChevronDown className="w-5 h-5 text-gray-500" />
          )}
        </div>
      </button>

      {isExpanded && (
        <div className="mt-3 pt-3 border-t border-st-blue/20 space-y-3">
          {citations.map((citation, idx) => (
            <div key={citation.id || idx}>
              {citation.page_number && (
                <p className="text-xs font-semibold text-gray-600 mb-1">
                  Page {citation.page_number}
                  {citation.relevance_score && (
                    <span className="ml-2 text-gray-500">
                      ({Math.round(citation.relevance_score * 100)}% match)
                    </span>
                  )}
                </p>
              )}
              {citation.chunk_text && (
                <p className="text-sm text-gray-700 leading-relaxed italic">
                  &ldquo;{citation.chunk_text}&rdquo;
                </p>
              )}
              {idx < citations.length - 1 && (
                <div className="mt-3 border-b border-gray-200" />
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Citation;
