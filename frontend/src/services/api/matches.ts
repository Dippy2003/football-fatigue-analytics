import type { Match, MatchPlayer, MatchQuality, TeamSummary } from '../../types/domain'
import { apiClient } from './client'

export const getMatches = async (signal?: AbortSignal) =>
  (await apiClient.get<Match[]>('/matches', { signal })).data

export const getMatch = async (matchId: string, signal?: AbortSignal) =>
  (await apiClient.get<Match>(`/matches/${matchId}`, { signal })).data

export const getMatchPlayers = async (matchId: string, signal?: AbortSignal) =>
  (await apiClient.get<MatchPlayer[]>(`/matches/${matchId}/players`, { signal })).data

export const getTeamSummary = async (matchId: string, signal?: AbortSignal) =>
  (await apiClient.get<TeamSummary[]>(`/matches/${matchId}/team-summary`, { signal }))
    .data

export const getMatchQuality = async (matchId: string, signal?: AbortSignal) =>
  (await apiClient.get<MatchQuality>(`/matches/${matchId}/quality`, { signal })).data
