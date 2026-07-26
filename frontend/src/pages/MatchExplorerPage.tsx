import { useQuery } from '@tanstack/react-query'
import { ArrowUpDown, Search } from 'lucide-react'
import { useMemo } from 'react'
import { Link, useParams, useSearchParams } from 'react-router-dom'

import { EmptyState, ErrorState, LoadingState } from '../components/ui/AsyncState'
import { DataQualityPanel } from '../components/ui/DataQualityPanel'
import { Panel } from '../components/ui/Panel'
import { StatusBadge } from '../components/ui/StatusBadge'
import { formatDistance, formatPercent } from '../lib/format'
import {
  getMatch,
  getMatchPlayers,
  getMatchQuality,
  getTeamSummary,
} from '../services/api/matches'

export function MatchExplorerPage() {
  const { matchId = '' } = useParams()
  const [params, setParams] = useSearchParams()
  const search = params.get('search') ?? ''
  const sort = params.get('sort') ?? 'distance'
  const team = params.get('team') ?? 'all'
  const match = useQuery({
    queryKey: ['match', matchId],
    queryFn: ({ signal }) => getMatch(matchId, signal),
    enabled: Boolean(matchId),
  })
  const players = useQuery({
    queryKey: ['match-players', matchId],
    queryFn: ({ signal }) => getMatchPlayers(matchId, signal),
    enabled: Boolean(matchId),
  })
  const quality = useQuery({
    queryKey: ['match-quality', matchId],
    queryFn: ({ signal }) => getMatchQuality(matchId, signal),
    enabled: Boolean(matchId),
  })
  const teams = useQuery({
    queryKey: ['team-summary', matchId],
    queryFn: ({ signal }) => getTeamSummary(matchId, signal),
    enabled: Boolean(matchId),
  })
  const filtered = useMemo(
    () =>
      (players.data ?? [])
        .filter(
          (player) =>
            (team === 'all' || player.team_id === team) &&
            player.name.toLowerCase().includes(search.toLowerCase()),
        )
        .sort((a, b) =>
          sort === 'quality'
            ? b.data_quality_score - a.data_quality_score
            : sort === 'name'
              ? a.name.localeCompare(b.name)
              : b.total_distance_m - a.total_distance_m,
        ),
    [players.data, search, sort, team],
  )
  if (match.isPending || players.isPending)
    return <LoadingState label="Loading match explorer" />
  if (match.isError || players.isError)
    return <ErrorState retry={() => void match.refetch()} />
  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <p className="eyebrow">Match explorer</p>
          <h1>{match.data?.competition ?? 'Match'}</h1>
          <p>
            {players.data?.length ?? 0} player summaries · processing{' '}
            {match.data?.processing_status}
          </p>
        </div>
        <StatusBadge
          label={match.data?.is_synthetic ? 'Synthetic demo' : 'Local import'}
          tone="info"
        />
      </header>
      <div className="content-grid">
        {teams.data?.map((item) => (
          <Panel key={item.team_id} title={item.team_name}>
            <dl className="stat-list">
              <div>
                <dt>Players</dt>
                <dd>{item.player_count}</dd>
              </div>
              <div>
                <dt>Distance</dt>
                <dd>{formatDistance(item.total_distance_m)}</dd>
              </div>
              <div>
                <dt>Sprints</dt>
                <dd>{item.sprint_count}</dd>
              </div>
            </dl>
          </Panel>
        ))}
      </div>
      <Panel
        title="Players"
        description="Filters remain in the URL for shareable views."
      >
        <div className="filter-bar">
          <label>
            <span>Search players</span>
            <div className="input-wrap">
              <Search aria-hidden="true" size={16} />
              <input
                value={search}
                onChange={(event) => {
                  params.set('search', event.target.value)
                  setParams(params)
                }}
              />
            </div>
          </label>
          <label>
            <span>Team</span>
            <select
              value={team}
              onChange={(event) => {
                params.set('team', event.target.value)
                setParams(params)
              }}
            >
              <option value="all">All teams</option>
              {teams.data?.map((item) => (
                <option key={item.team_id} value={item.team_id}>
                  {item.team_name}
                </option>
              ))}
            </select>
          </label>
          <label>
            <span>Sort by</span>
            <select
              value={sort}
              onChange={(event) => {
                params.set('sort', event.target.value)
                setParams(params)
              }}
            >
              <option value="distance">Workload</option>
              <option value="quality">Quality</option>
              <option value="name">Name</option>
            </select>
          </label>
        </div>
        {filtered.length === 0 ? (
          <EmptyState message="No players match the current filters." />
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Player</th>
                  <th>Role</th>
                  <th>
                    <ArrowUpDown aria-hidden="true" size={14} /> Distance
                  </th>
                  <th>Quality</th>
                  <th>
                    <span className="sr-only">Actions</span>
                  </th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((player) => (
                  <tr key={player.id}>
                    <td>{player.name}</td>
                    <td>{player.position ?? 'Unavailable'}</td>
                    <td>{formatDistance(player.total_distance_m)}</td>
                    <td>{formatPercent(player.data_quality_score)}</td>
                    <td>
                      <Link
                        className="text-link"
                        to={`/matches/${matchId}/players/${player.id}`}
                      >
                        Analyse
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        <Link className="button-secondary mt-5" to={`/matches/${matchId}/compare`}>
          Compare players
        </Link>
      </Panel>
      {quality.data && (
        <DataQualityPanel
          score={quality.data.data_quality_score}
          coverage={quality.data.player_metric_coverage}
          limitations={quality.data.limitations}
        />
      )}
    </div>
  )
}
