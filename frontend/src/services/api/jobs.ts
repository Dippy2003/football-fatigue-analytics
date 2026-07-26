import type { ProcessingJob } from '../../types/domain'
import { apiClient } from './client'

export const processMatch = async (matchId: string) =>
  (await apiClient.post<ProcessingJob>(`/matches/${matchId}/process`)).data

export const getJob = async (jobId: string, signal?: AbortSignal) =>
  (await apiClient.get<ProcessingJob>(`/jobs/${jobId}`, { signal })).data
