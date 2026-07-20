export type HealthResponse = {
  status: 'ok'
}

export type ReadinessResponse = {
  status: 'ready'
  checks: Record<string, 'ok'>
}

export type VersionResponse = {
  name: 'PlayerPulse API'
  version: string
  api_version: 'v1'
}

export type ApiErrorResponse = {
  code: string
  message: string
  details: Record<string, unknown> | null
  request_id: string
  timestamp: string
}
