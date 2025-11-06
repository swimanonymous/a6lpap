/**
 * HTTP client utilities
 */

const API_BASE = import.meta.env.VITE_API_BASE || '/api';

export interface ApiError {
  error: string;
}

export class HttpError extends Error {
  constructor(public status: number, public data: ApiError) {
    super(data.error);
  }
}

async function request<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (response.status === 204) {
    return undefined as T;
  }

  const data = await response.json();

  if (!response.ok) {
    throw new HttpError(response.status, data);
  }

  return data;
}

export const http = {
  get: <T>(endpoint: string) => request<T>(endpoint, { method: 'GET' }),
  
  post: <T>(endpoint: string, body: unknown) =>
    request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(body),
    }),
  
  patch: <T>(endpoint: string, body: unknown) =>
    request<T>(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(body),
    }),
  
  delete: <T>(endpoint: string) =>
    request<T>(endpoint, { method: 'DELETE' }),
};