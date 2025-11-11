import { useState } from 'react';
import { Star } from 'lucide-react';
import { api } from '../../utils/api';
import { useChat } from '../../hooks/useChat';

const RatingComponent = ({ messageId, onRatingSubmit }) => {
  const [selectedRating, setSelectedRating] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const { sessionId } = useChat();

  const handleRating = async (rating) => {
    if (isSubmitting) return;

    try {
      setIsSubmitting(true);
      setError(null);
      setSelectedRating(rating);

      await api.submitFeedback({
        session_id: sessionId,
        message_id: messageId,
        rating
      });

      if (onRatingSubmit) {
        onRatingSubmit(rating);
      }
    } catch (err) {
      console.error('Error submitting rating:', err);
      setError('Failed to submit rating');
      setSelectedRating(null);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (selectedRating) {
    return null; // Hide after rating
  }

  return (
    <div className="flex items-center gap-2">
      <span className="text-xs text-gray-500">Rate:</span>
      <div className="flex items-center gap-1">
        {[1, 2, 3, 4, 5].map((rating) => (
          <button
            key={rating}
            onClick={() => handleRating(rating)}
            disabled={isSubmitting}
            className="p-1 hover:scale-110 transition-transform disabled:opacity-50"
            title={`${rating} star${rating > 1 ? 's' : ''}`}
          >
            <Star
              className={`w-4 h-4 ${
                rating <= (selectedRating || 0)
                  ? 'fill-st-orange text-st-orange'
                  : 'text-gray-400 hover:text-st-orange'
              }`}
            />
          </button>
        ))}
      </div>

      {error && (
        <span className="text-xs text-red-500">{error}</span>
      )}
    </div>
  );
};

export default RatingComponent;
