import type {
  HealthResponse,
  ReadinessResponse,
  VersionResponse,
} from '../../types/api'
import { apiClient } from './client'

export async function getHealth(): Promise<HealthResponse> {
  const response = await apiClient.get<HealthResponse>('/health')
  return response.data
}

export async function getReadiness(): Promise<ReadinessResponse> {
  const response = await apiClient.get<ReadinessResponse>('/readiness')
  return response.data
}

export async function getVersion(): Promise<VersionResponse> {
  const response = await apiClient.get<VersionResponse>('/version')
  return response.data
}
