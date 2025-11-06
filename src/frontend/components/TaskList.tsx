/**
 * List of tasks with inline edit/delete
 */
import { useState } from 'react';
import { Task, tasksApi } from '../api/tasks';

interface TaskListProps {
  tasks: Task[];
  selectedTaskId: string | null;
  onTaskSelect: (taskId: string) => void;
  onTasksChange: () => void;
}

export function TaskList({
  tasks,
  selectedTaskId,
  onTaskSelect,
  onTasksChange,
}: TaskListProps) {
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');
  const [editStatus, setEditStatus] = useState<'todo' | 'in_progress' | 'done'>('todo');
  const [loading, setLoading] = useState<string | null>(null);
  const [error, setError] = useState('');

  const startEdit = (task: Task) => {
    setEditingId(task._id);
    setEditTitle(task.title);
    setEditDescription(task.description || '');
    setEditStatus(task.status);
    setError('');
  };

  const cancelEdit = () => {
    setEditingId(null);
    setEditTitle('');
    setEditDescription('');
    setError('');
  };

  const saveEdit = async (id: string) => {
    setError('');
    setLoading(id);

    try {
      await tasksApi.update(id, {
        title: editTitle.trim(),
        description: editDescription.trim() || undefined,
        status: editStatus,
      });
      setEditingId(null);
      onTasksChange();
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
    } finally {
      setLoading(null);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this task and all its comments?')) {
      return;
    }

    setLoading(id);
    setError('');

    try {
      await tasksApi.delete(id);
      if (selectedTaskId === id) {
        onTaskSelect('');
      }
      onTasksChange();
    } catch (err: any) {
      setError(err.message || 'Failed to delete task');
    } finally {
      setLoading(null);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'todo':
        return 'bg-gray-100 text-gray-800';
      case 'in_progress':
        return 'bg-blue-100 text-blue-800';
      case 'done':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'todo':
        return 'To Do';
      case 'in_progress':
        return 'In Progress';
      case 'done':
        return 'Done';
      default:
        return status;
    }
  };

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        No tasks yet. Create one above!
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {error && (
        <div className="p-3 bg-red-50 text-red-700 rounded">
          {error}
        </div>
      )}

      {tasks.map((task) => (
        <div
          key={task._id}
          className={`bg-white p-4 rounded-lg shadow-md border-2 transition-colors ${
            selectedTaskId === task._id ? 'border-blue-500' : 'border-transparent'
          }`}
        >
          {editingId === task._id ? (
            <div className="space-y-3">
              <input
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Title"
              />
              <textarea
                value={editDescription}
                onChange={(e) => setEditDescription(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Description"
                rows={2}
              />
              <select
                value={editStatus}
                onChange={(e) => setEditStatus(e.target.value as any)}
                className="px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="todo">To Do</option>
                <option value="in_progress">In Progress</option>
                <option value="done">Done</option>
              </select>
              <div className="flex gap-2">
                <button
                  onClick={() => saveEdit(task._id)}
                  disabled={loading === task._id}
                  className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400"
                >
                  {loading === task._id ? 'Saving...' : 'Save'}
                </button>
                <button
                  onClick={cancelEdit}
                  disabled={loading === task._id}
                  className="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <>
              <div
                className="cursor-pointer"
                onClick={() => onTaskSelect(task._id)}
              >
                <div className="flex items-start justify-between mb-2">
                  <h3 className="text-lg font-semibold">{task.title}</h3>
                  <span
                    className={`px-2 py-1 text-xs rounded ${getStatusColor(
                      task.status
                    )}`}
                  >
                    {getStatusLabel(task.status)}
                  </span>
                </div>
                {task.description && (
                  <p className="text-gray-600 mb-2">{task.description}</p>
                )}
                <p className="text-xs text-gray-400">
                  Created: {new Date(task.created_at).toLocaleString()}
                </p>
              </div>
              <div className="flex gap-2 mt-3">
                <button
                  onClick={() => startEdit(task)}
                  disabled={loading === task._id}
                  className="px-3 py-1 text-sm bg-gray-200 text-gray-700 rounded hover:bg-gray-300 disabled:bg-gray-100"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(task._id)}
                  disabled={loading === task._id}
                  className="px-3 py-1 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200 disabled:bg-gray-100"
                >
                  {loading === task._id ? 'Deleting...' : 'Delete'}
                </button>
              </div>
            </>
          )}
        </div>
      ))}
    </div>
  );
}