import { formatRelativeTime } from '../../utils/formatting';

const UserMessage = ({ message }) => {
  return (
    <div className="flex justify-end items-start gap-3 mb-4">
      <div className="max-w-[70%]">
        <div className="bg-st-blue text-white rounded-lg rounded-tr-sm px-4 py-3 shadow-sm">
          <p className="text-sm leading-relaxed whitespace-pre-wrap break-words">
            {message.content}
          </p>
        </div>
        {message.timestamp && (
          <p className="text-xs text-gray-500 mt-1 text-right">
            {formatRelativeTime(message.timestamp)}
          </p>
        )}
      </div>
      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-st-green flex items-center justify-center text-white font-semibold">
        U
      </div>
    </div>
  );
};

export default UserMessage;
