import type { DataSource, DemoDataset } from '../../types/domain'
import { apiClient } from './client'

export async function createDemo(signal?: AbortSignal): Promise<DemoDataset> {
  const response = await apiClient.post<DemoDataset>('/datasets/demo', undefined, {
    signal,
  })
  return response.data
}

export async function getSources(signal?: AbortSignal): Promise<DataSource[]> {
  const response = await apiClient.get<DataSource[]>('/datasets/sources', { signal })
  return response.data
}
