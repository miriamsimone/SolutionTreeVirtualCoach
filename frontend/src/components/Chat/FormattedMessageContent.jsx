import { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';

const FormattedMessageContent = ({ content, streaming }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  // Helper function to render text with markdown formatting
  const renderFormattedText = (text) => {
    if (!text) return null;

    // Split by **bold** markers while preserving the text
    const parts = [];
    let currentText = text;
    let key = 0;

    while (currentText.length > 0) {
      const boldStart = currentText.indexOf('**');

      if (boldStart === -1) {
        // No more bold text, add remaining text
        parts.push(<span key={key++}>{currentText}</span>);
        break;
      }

      // Add text before bold
      if (boldStart > 0) {
        parts.push(<span key={key++}>{currentText.substring(0, boldStart)}</span>);
      }

      // Find end of bold text
      const boldEnd = currentText.indexOf('**', boldStart + 2);

      if (boldEnd === -1) {
        // No closing **, treat as regular text
        parts.push(<span key={key++}>{currentText.substring(boldStart)}</span>);
        break;
      }

      // Add bold text
      const boldText = currentText.substring(boldStart + 2, boldEnd);
      parts.push(<strong key={key++} className="font-semibold text-gray-900">{boldText}</strong>);

      // Continue with remaining text
      currentText = currentText.substring(boldEnd + 2);
    }

    return parts;
  };

  // Parse the message content to extract summary and sections
  const parseContent = (text) => {
    const lines = text.split('\n');
    const parsed = {
      summary: [],
      sections: []
    };

    let currentSection = null;
    let inSummary = false;
    let summaryStarted = false;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();

      // Detect summary section
      if (line.match(/^(summary|key points?|quick summary|overview):?$/i)) {
        inSummary = true;
        summaryStarted = true;
        continue;
      }

      // Detect bullet points in summary
      if (inSummary && line.match(/^[•\-*]\s+/)) {
        parsed.summary.push(line.replace(/^[•\-*]\s+/, ''));
        continue;
      }

      // Exit summary when we hit a heading or empty line after summary items
      if (inSummary && (line.match(/^#{1,3}\s+/) || (line === '' && parsed.summary.length > 0))) {
        inSummary = false;
      }

      // Detect headings (markdown style or just bold text patterns)
      if (line.match(/^#{1,3}\s+(.+)$/)) {
        const headingText = line.replace(/^#{1,3}\s+/, '');
        if (currentSection) {
          parsed.sections.push(currentSection);
        }
        currentSection = {
          heading: headingText,
          content: []
        };
        continue;
      }

      // Detect headings without markdown (common patterns)
      if (line.match(/^[A-Z][A-Za-z\s&]+:$/) && !summaryStarted) {
        if (currentSection) {
          parsed.sections.push(currentSection);
        }
        currentSection = {
          heading: line.replace(/:$/, ''),
          content: []
        };
        continue;
      }

      // Add content to current section or as standalone
      if (!inSummary) {
        if (currentSection) {
          currentSection.content.push(lines[i]); // Keep original line with indentation
        } else if (line) {
          // Content before any section
          if (!parsed.sections.length) {
            parsed.sections.push({
              heading: null,
              content: [lines[i]]
            });
          } else {
            parsed.sections[parsed.sections.length - 1].content.push(lines[i]);
          }
        }
      }
    }

    // Add the last section
    if (currentSection) {
      parsed.sections.push(currentSection);
    }

    return parsed;
  };

  const parsed = parseContent(content);

  // If no structured content found, display as plain text with formatting
  if (parsed.summary.length === 0 && parsed.sections.length === 0) {
    const lines = content.split('\n');
    return (
      <div className="text-sm text-gray-800 leading-relaxed break-words space-y-2">
        {lines.map((line, idx) => (
          <div key={idx}>{renderFormattedText(line) || '\u00A0'}</div>
        ))}
        {streaming && (
          <span className="inline-flex ml-1">
            <span className="animate-pulse text-st-blue">▊</span>
          </span>
        )}
      </div>
    );
  }

  // Show expander only if we have summary AND sections
  const showExpander = parsed.summary.length > 0 && parsed.sections.length > 0;

  // Check if we're currently streaming content in the sections (not the summary)
  const streamingDetails = streaming && parsed.sections.length > 0;

  return (
    <div className="space-y-4">
      {/* Summary Section */}
      {parsed.summary.length > 0 && (
        <div className="bg-st-blue/5 border-l-4 border-st-blue rounded-r px-4 py-3">
          <h4 className="text-xs font-semibold text-st-blue-dark uppercase tracking-wide mb-2">
            Quick Summary
          </h4>
          <ul className="space-y-1.5">
            {parsed.summary.map((item, idx) => (
              <li key={idx} className="text-sm text-gray-800 flex items-start gap-2">
                <span className="text-st-blue mt-1">•</span>
                <span className="flex-1">{renderFormattedText(item)}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Expand/Collapse Button - Show after summary is loaded and we have sections */}
      {showExpander && (
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center gap-2 text-sm text-st-blue hover:text-st-blue-dark font-medium transition-colors"
        >
          {isExpanded ? (
            <>
              <ChevronUp className="w-4 h-4" />
              <span>Show less</span>
            </>
          ) : (
            <>
              <ChevronDown className="w-4 h-4" />
              <span>See more details{streamingDetails ? ' (loading...)' : ''}</span>
            </>
          )}
        </button>
      )}

      {/* Main Content Sections - Only show when expanded or if there's no summary */}
      {(isExpanded || !showExpander) && parsed.sections.map((section, idx) => (
        <div key={idx}>
          {section.heading && (
            <h3 className="font-bold text-gray-900 text-sm mb-2">
              {renderFormattedText(section.heading)}
            </h3>
          )}
          <div className="text-sm text-gray-800 leading-relaxed break-words space-y-2">
            {section.content.map((line, lineIdx) => (
              <div key={lineIdx}>{renderFormattedText(line) || '\u00A0'}</div>
            ))}
          </div>
        </div>
      ))}

      {streaming && (
        <span className="inline-flex ml-1">
          <span className="animate-pulse text-st-blue">▊</span>
        </span>
      )}
    </div>
  );
};

export default FormattedMessageContent;
