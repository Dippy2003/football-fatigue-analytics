import axios from 'axios'
import type { AxiosError } from 'axios'

import type { ApiErrorResponse } from '../../types/api'

const DEFAULT_API_BASE_URL = 'http://localhost:8000/api/v1'

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? DEFAULT_API_BASE_URL,
  headers: {
    Accept: 'application/json',
  },
  timeout: 10_000,
})

export function getApiErrorMessage(error: unknown): string {
  if (!axios.isAxiosError<ApiErrorResponse>(error)) {
    return 'The request could not be completed.'
  }
  return error.response?.data?.message ?? 'The PlayerPulse API is unavailable.'
}

export function shouldRetryQuery(failureCount: number, error: unknown): boolean {
  const status = (error as AxiosError | undefined)?.response?.status
  if (status != null && status >= 400 && status < 500) return false
  return failureCount < 2
}
