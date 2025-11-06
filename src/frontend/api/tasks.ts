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

export const tasksApi = {
  list: () => http.get<Task[]>('/tasks'),
  
  get: (id: string) => http.get<Task>(`/tasks/${id}`),
  
  create: (data: CreateTaskDto) => http.post<Task>('/tasks', data),
  
  update: (id: string, data: UpdateTaskDto) =>
    http.patch<Task>(`/tasks/${id}`, data),
  
  delete: (id: string) => http.delete<void>(`/tasks/${id}`),
};