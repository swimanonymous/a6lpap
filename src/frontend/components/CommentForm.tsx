/**
 * Form for creating new comments
 */
import { useState, FormEvent } from 'react';
import { commentsApi } from '../api/comments';

interface CommentFormProps {
  taskId: string;
  onSuccess: () => void;
}

export function CommentForm({ taskId, onSuccess }: CommentFormProps) {
  const [body, setBody] = useState('');
  const [author, setAuthor] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');

    if (!body.trim()) {
      setError('Comment body is required');
      return;
    }

    setLoading(true);

    try {
      await commentsApi.create(taskId, {
        body: body.trim(),
        author: author.trim() || undefined,
      });
      
      setBody('');
      setAuthor('');
      onSuccess();
    } catch (err: any) {
      setError(err.message || 'Failed to create comment');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-4 rounded-lg shadow-md">
      <h3 className="font-semibold mb-3">Add Comment</h3>
      
      {error && (
        <div className="mb-3 p-2 bg-red-50 text-red-700 text-sm rounded">
          {error}
        </div>
      )}

      <div className="mb-3">
        <textarea
          value={body}
          onChange={(e) => setBody(e.target.value)}
          className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Write your comment..."
          rows={3}
          disabled={loading}
        />
      </div>

      <div className="mb-3">
        <input
          type="text"
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
          className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Your name (optional)"
          disabled={loading}
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
      >
        {loading ? 'Posting...' : 'Post Comment'}
      </button>
    </form>
  );
}