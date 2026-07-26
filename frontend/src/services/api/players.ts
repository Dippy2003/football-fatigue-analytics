import type {
  Baseline,
  Heatmap,
  PlayerEvents,
  PlayerMetrics,
  PlayerProfile,
  Timeline,
} from '../../types/domain'
import { apiClient } from './client'

export const getPlayer = async (playerId: string, signal?: AbortSignal) =>
  (await apiClient.get<PlayerProfile>(`/players/${playerId}`, { signal })).data

export const getPlayerMetrics = async (
  matchId: string,
  playerId: string,
  signal?: AbortSignal,
) =>
  (
    await apiClient.get<PlayerMetrics>(
      `/matches/${matchId}/players/${playerId}/metrics`,
      { signal },
    )
  ).data

export const getPlayerTimeline = async (
  matchId: string,
  playerId: string,
  signal?: AbortSignal,
) =>
  (
    await apiClient.get<Timeline>(`/matches/${matchId}/players/${playerId}/timeline`, {
      signal,
    })
  ).data

export const getPlayerHeatmap = async (
  matchId: string,
  playerId: string,
  signal?: AbortSignal,
) =>
  (
    await apiClient.get<Heatmap>(`/matches/${matchId}/players/${playerId}/heatmap`, {
      signal,
    })
  ).data

export const getPlayerEvents = async (
  matchId: string,
  playerId: string,
  signal?: AbortSignal,
) =>
  (
    await apiClient.get<PlayerEvents>(
      `/matches/${matchId}/players/${playerId}/events`,
      { signal },
    )
  ).data

export const getPlayerBaseline = async (playerId: string, signal?: AbortSignal) =>
  (await apiClient.get<Baseline>(`/players/${playerId}/baseline`, { signal })).data
