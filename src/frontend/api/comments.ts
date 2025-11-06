/**
 * Comments API client
 */
import { http } from './http';

export interface Comment {
  _id: string;
  task_id: string;
  body: string;
  author: string | null;
  created_at: string;
  updated_at: string;
}

export interface CommentsResponse {
  comments: Comment[];
  count: number;
  limit: number;
  offset: number;
}

export interface CreateCommentDto {
  body: string;
  author?: string;
}

export interface UpdateCommentDto {
  body?: string;
  author?: string;
}

export const commentsApi = {
  list: (taskId: string, limit = 20, offset = 0) =>
    http.get<CommentsResponse>(
      `/tasks/${taskId}/comments?limit=${limit}&offset=${offset}`
    ),
  
  create: (taskId: string, data: CreateCommentDto) =>
    http.post<Comment>(`/tasks/${taskId}/comments`, data),
  
  update: (id: string, data: UpdateCommentDto) =>
    http.patch<Comment>(`/comments/${id}`, data),
  
  delete: (id: string) => http.delete<void>(`/comments/${id}`),
};