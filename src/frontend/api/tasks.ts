/**
 * Tasks API client
 */
import { http } from './http';

export interface Task {
  _id: string;
  title: string;
  description: string | null;
  status: 'todo' | 'in_progress' | 'done';
  created_at: string;
  updated_at: string;
}

export interface CreateTaskDto {
  title: string;
  description?: string;
  status?: 'todo' | 'in_progress' | 'done';
}

export interface UpdateTaskDto {
  title?: string;
  description?: string;
  status?: 'todo' | 'in_progress' | 'done';
}

// ✅ Fixed endpoints to match Flask blueprint prefix `/api/tasks`
export const tasksApi = {
  list: () => http.get<Task[]>('/api/tasks'),
  
  get: (id: string) => http.get<Task>(`/api/tasks/${id}`),
  
  create: (data: CreateTaskDto) => http.post<Task>('/api/tasks', data),
  
  update: (id: string, data: UpdateTaskDto) =>
    http.patch<Task>(`/api/tasks/${id}`, data),
  
  delete: (id: string) => http.delete<void>(`/api/tasks/${id}`),
};
