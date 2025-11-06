/**
 * List of comments with inline edit/delete
 */
import { useState } from 'react';
import { Comment, commentsApi } from '../api/comments';

interface CommentListProps {
  comments: Comment[];
  totalCount: number;
  onCommentsChange: () => void;
}

export function CommentList({
  comments,
  totalCount,
  onCommentsChange,
}: CommentListProps) {
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editBody, setEditBody] = useState('');
  const [editAuthor, setEditAuthor] = useState('');
  const [loading, setLoading] = useState<string | null>(null);
  const [error, setError] = useState('');

  const startEdit = (comment: Comment) => {
    setEditingId(comment._id);
    setEditBody(comment.body);
    setEditAuthor(comment.author || '');
    setError('');
  };

  const cancelEdit = () => {
    setEditingId(null);
    setEditBody('');
    setEditAuthor('');
    setError('');
  };

  const saveEdit = async (id: string) => {
    setError('');
    setLoading(id);

    try {
      await commentsApi.update(id, {
        body: editBody.trim(),
        author: editAuthor.trim() || undefined,
      });
      setEditingId(null);
      onCommentsChange();
    } catch (err: any) {
      setError(err.message || 'Failed to update comment');
    } finally {
      setLoading(null);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this comment?')) {
      return;
    }

    setLoading(id);
    setError('');

    try {
      await commentsApi.delete(id);
      onCommentsChange();
    } catch (err: any) {
      setError(err.message || 'Failed to delete comment');
    } finally {
      setLoading(null);
    }
  };

  if (comments.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No comments yet. Be the first to comment!
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold">Comments ({totalCount})</h3>
      </div>

      {error && (
        <div className="p-3 bg-red-50 text-red-700 rounded text-sm">
          {error}
        </div>
      )}

      {comments.map((comment) => (
        <div
          key={comment._id}
          className="bg-gray-50 p-4 rounded-lg"
        >
          {editingId === comment._id ? (
            <div className="space-y-2">
              <textarea
                value={editBody}
                onChange={(e) => setEditBody(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows={3}
              />
              <input
                type="text"
                value={editAuthor}
                onChange={(e) => setEditAuthor(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Author (optional)"
              />
              <div className="flex gap-2">
                <button
                  onClick={() => saveEdit(comment._id)}
                  disabled={loading === comment._id}
                  className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400"
                >
                  {loading === comment._id ? 'Saving...' : 'Save'}
                </button>
                <button
                  onClick={cancelEdit}
                  disabled={loading === comment._id}
                  className="px-3 py-1 text-sm bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <>
              <p className="text-gray-800 mb-2">{comment.body}</p>
              <div className="flex items-center justify-between text-xs text-gray-500">
                <div>
                  <span className="font-medium">
                    {comment.author || 'Anonymous'}
                  </span>
                  {' • '}
                  <span>{new Date(comment.created_at).toLocaleString()}</span>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => startEdit(comment)}
                    disabled={loading === comment._id}
                    className="text-blue-600 hover:text-blue-800 disabled:text-gray-400"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(comment._id)}
                    disabled={loading === comment._id}
                    className="text-red-600 hover:text-red-800 disabled:text-gray-400"
                  >
                    {loading === comment._id ? 'Deleting...' : 'Delete'}
                  </button>
                </div>
              </div>
            </>
          )}
        </div>
      ))}
    </div>
  );
}