import type {
  DataSource,
  DemoDataset,
  ImportCapabilities,
  LocalImportResult,
} from '../../types/domain'
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

export async function getImportCapabilities(
  signal?: AbortSignal,
): Promise<ImportCapabilities> {
  const response = await apiClient.get<ImportCapabilities>(
    '/datasets/import-capabilities',
    { signal },
  )
  return response.data
}

export type LocalImportRequest = {
  sourceMatchId: string
  competition: string
  tracking: File
  events?: File
}

export async function importLocalDataset(
  request: LocalImportRequest,
): Promise<LocalImportResult> {
  const files = [
    { role: 'tracking', file: request.tracking },
    ...(request.events ? [{ role: 'events', file: request.events }] : []),
  ]
  const body = new FormData()
  body.set('provider', 'metrica_sample_data')
  body.set(
    'manifest',
    JSON.stringify({
      source_match_id: request.sourceMatchId,
      competition: request.competition,
      rights_acknowledged: true,
      files: files.map(({ role, file }) => ({ role, filename: file.name })),
    }),
  )
  files.forEach(({ file }) => body.append('files', file))
  const response = await apiClient.post<LocalImportResult>('/datasets/upload', body)
  return response.data
}
