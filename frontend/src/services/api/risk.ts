import type { Comparison, RiskAssessment } from '../../types/domain'
import { apiClient } from './client'

export const getPlayerRisk = async (
  matchId: string,
  playerId: string,
  signal?: AbortSignal,
) =>
  (
    await apiClient.get<RiskAssessment>(
      `/matches/${matchId}/players/${playerId}/risk`,
      { signal },
    )
  ).data

export const comparePlayers = async (
  matchId: string,
  playerIds: string[],
  signal?: AbortSignal,
) =>
  (
    await apiClient.get<Comparison>(`/matches/${matchId}/compare-players`, {
      params: { player_ids: playerIds },
      paramsSerializer: { indexes: null },
      signal,
    })
  ).data
