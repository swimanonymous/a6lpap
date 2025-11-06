/**
 * Main tasks page with comments
 */
import { useState, useEffect } from 'react';
import { Task, tasksApi } from '../api/tasks';
import { commentsApi, CommentsResponse } from '../api/comments';
import { TaskForm } from '../components/TaskForm';
import { TaskList } from '../components/TaskList';
import { CommentForm } from '../components/CommentForm';
import { CommentList } from '../components/CommentList';

export function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [selectedTaskId, setSelectedTaskId] = useState<string | null>(null);
  const [comments, setComments] = useState<CommentsResponse | null>(null);
  const [loadingTasks, setLoadingTasks] = useState(true);
  const [loadingComments, setLoadingComments] = useState(false);
  const [error, setError] = useState('');

  const loadTasks = async () => {
    setLoadingTasks(true);
    setError('');

    try {
      const data = await tasksApi.list();
      setTasks(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load tasks');
    } finally {
      setLoadingTasks(false);
    }
  };

  const loadComments = async (taskId: string) => {
    setLoadingComments(true);
    setError('');

    try {
      const data = await commentsApi.list(taskId);
      setComments(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load comments');
    } finally {
      setLoadingComments(false);
    }
  };

  useEffect(() => {
    loadTasks();
  }, []);

  useEffect(() => {
    if (selectedTaskId) {
      loadComments(selectedTaskId);
    } else {
      setComments(null);
    }
  }, [selectedTaskId]);

  const handleTaskSelect = (taskId: string) => {
    setSelectedTaskId(taskId === selectedTaskId ? null : taskId);
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="max-w-7xl mx-auto px-4">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Task Manager
        </h1>

        {error && (
          <div className="mb-6 p-4 bg-red-50 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column: Task Management */}
          <div className="space-y-6">
            <TaskForm onSuccess={loadTasks} />

            <div className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-xl font-semibold mb-4">
                All Tasks ({tasks.length})
              </h2>
              
              {loadingTasks ? (
                <div className="text-center py-8 text-gray-500">
                  Loading tasks...
                </div>
              ) : (
                <TaskList
                  tasks={tasks}
                  selectedTaskId={selectedTaskId}
                  onTaskSelect={handleTaskSelect}
                  onTasksChange={loadTasks}
                />
              )}
            </div>
          </div>

          {/* Right Column: Comments */}
          <div className="space-y-6">
            {selectedTaskId ? (
              <>
                <div className="bg-blue-50 p-4 rounded-lg">
                  <p className="text-sm text-blue-800">
                    <strong>Selected Task:</strong>{' '}
                    {tasks.find((t) => t._id === selectedTaskId)?.title}
                  </p>
                </div>

                <CommentForm
                  taskId={selectedTaskId}
                  onSuccess={() => loadComments(selectedTaskId)}
                />

                <div className="bg-white p-6 rounded-lg shadow-md">
                  {loadingComments ? (
                    <div className="text-center py-8 text-gray-500">
                      Loading comments...
                    </div>
                  ) : comments ? (
                    <CommentList
                      comments={comments.comments}
                      totalCount={comments.count}
                      onCommentsChange={() => loadComments(selectedTaskId)}
                    />
                  ) : null}
                </div>
              </>
            ) : (
              <div className="bg-white p-12 rounded-lg shadow-md text-center text-gray-500">
                <p className="text-lg">Select a task to view and manage comments</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}