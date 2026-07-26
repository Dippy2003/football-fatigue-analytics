import { useQuery } from '@tanstack/react-query'
import { useState } from 'react'
import { useParams } from 'react-router-dom'

import { EmptyState, ErrorState, LoadingState } from '../components/ui/AsyncState'
import { Panel } from '../components/ui/Panel'
import { StatusBadge } from '../components/ui/StatusBadge'
import { formatDistance, formatNumber, formatPercent } from '../lib/format'
import { getMatchPlayers } from '../services/api/matches'
import { comparePlayers } from '../services/api/risk'

export function ComparisonPage() {
  const { matchId = '' } = useParams()
  const [selected, setSelected] = useState<string[]>([])
  const players = useQuery({
    queryKey: ['match-players', matchId],
    queryFn: ({ signal }) => getMatchPlayers(matchId, signal),
    enabled: Boolean(matchId),
  })
  const comparison = useQuery({
    queryKey: ['comparison', matchId, selected],
    queryFn: ({ signal }) => comparePlayers(matchId, selected, signal),
    enabled: selected.length >= 2,
  })
  if (players.isPending) return <LoadingState label="Loading player comparison" />
  if (players.isError) return <ErrorState retry={() => void players.refetch()} />
  const toggle = (id: string) =>
    setSelected((current) =>
      current.includes(id)
        ? current.filter((item) => item !== id)
        : current.length < 4
          ? [...current, id]
          : current,
    )
  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <p className="eyebrow">Contextual comparison</p>
          <h1>Compare players</h1>
          <p>Select two to four players. Unlike roles require additional context.</p>
        </div>
        <StatusBadge label={`${selected.length}/4 selected`} tone="info" />
      </header>
      <Panel title="Player selection">
        <div className="selection-grid">
          {players.data.map((player) => (
            <label className="check-card" key={player.id}>
              <input
                checked={selected.includes(player.id)}
                disabled={!selected.includes(player.id) && selected.length >= 4}
                onChange={() => toggle(player.id)}
                type="checkbox"
              />
              <span>
                <strong>{player.name}</strong>
                <small>{player.position ?? 'Role unavailable'}</small>
              </span>
            </label>
          ))}
        </div>
      </Panel>
      {selected.length < 2 ? (
        <EmptyState
          title="Select at least two players"
          message="Comparison data appears after two to four players are selected."
        />
      ) : comparison.isPending ? (
        <LoadingState />
      ) : comparison.isError ? (
        <ErrorState retry={() => void comparison.refetch()} />
      ) : (
        comparison.data && (
          <Panel title="Aligned workload comparison">
            <p className="mb-4 text-sm text-amber-700">{comparison.data.warning}</p>
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Player</th>
                    <th>Role</th>
                    <th>Distance</th>
                    <th>Max speed</th>
                    <th>Sprints</th>
                    <th>Quality</th>
                  </tr>
                </thead>
                <tbody>
                  {comparison.data.players.map((player) => (
                    <tr key={player.player_id}>
                      <td>{player.name}</td>
                      <td>{player.position ?? 'Unavailable'}</td>
                      <td>{formatDistance(player.total_distance_m)}</td>
                      <td>{formatNumber(player.max_speed_mps, 2)} m/s</td>
                      <td>{player.sprint_count}</td>
                      <td>{formatPercent(player.data_quality_score)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Panel>
        )
      )}
    </div>
  )
}
