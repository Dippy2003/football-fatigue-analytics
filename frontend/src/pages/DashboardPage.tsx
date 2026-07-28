import { useQueries, useQuery } from '@tanstack/react-query'
import { Activity, Gauge, ShieldCheck, Users } from 'lucide-react'
import { Link } from 'react-router-dom'

import { WorkloadBars } from '../components/charts/WorkloadBars'
import { EmptyState, ErrorState, LoadingState } from '../components/ui/AsyncState'
import { DataQualityPanel } from '../components/ui/DataQualityPanel'
import { MetricCard } from '../components/ui/MetricCard'
import { Panel } from '../components/ui/Panel'
import { StatusBadge } from '../components/ui/StatusBadge'
import { formatDistance } from '../lib/format'
import { getMatches, getMatchPlayers, getMatchQuality } from '../services/api/matches'
import { getPlayerRisk } from '../services/api/risk'

export function DashboardPage() {
  const matches = useQuery({
    queryKey: ['matches'],
    queryFn: ({ signal }) => getMatches(signal),
  })
  const matchId = matches.data?.[0]?.id
  const players = useQuery({
    queryKey: ['match-players', matchId],
    queryFn: ({ signal }) => getMatchPlayers(matchId!, signal),
    enabled: Boolean(matchId),
  })
  const quality = useQuery({
    queryKey: ['match-quality', matchId],
    queryFn: ({ signal }) => getMatchQuality(matchId!, signal),
    enabled: Boolean(matchId),
  })
  const risks = useQueries({
    queries: (players.data ?? []).map((player) => ({
      queryKey: ['risk', matchId, player.id],
      queryFn: ({ signal }: { signal: AbortSignal }) =>
        getPlayerRisk(matchId!, player.id, signal),
      enabled: Boolean(matchId),
    })),
  })
  if (matches.isPending || players.isPending)
    return <LoadingState label="Loading dashboard" />
  if (matches.isError || players.isError)
    return <ErrorState retry={() => void matches.refetch()} />
  if (!matchId || !players.data?.length)
    return (
      <EmptyState message="Load the deterministic demo to populate the dashboard." />
    )
  const highest = [...players.data].sort(
    (a, b) => b.total_distance_m - a.total_distance_m,
  )[0]!
  const selectedMatch = matches.data[0]!
  const elevated = risks.filter((risk) => (risk.data?.score ?? 0) >= 60).length
  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <p className="eyebrow">Team overview</p>
          <h1>Dashboard</h1>
          <p>Current match workload and performance-indicator summary.</p>
        </div>
        <StatusBadge
          label={selectedMatch.is_synthetic ? 'Synthetic demo' : 'Local import'}
          tone={selectedMatch.is_synthetic ? 'info' : 'success'}
        />
      </header>
      <div className="metric-grid">
        <MetricCard
          icon={Users}
          label="Players analysed"
          value={String(players.data.length)}
        />
        <MetricCard
          icon={Activity}
          label="Highest workload"
          value={formatDistance(highest.total_distance_m)}
          detail={highest.name}
        />
        <MetricCard
          icon={Gauge}
          label="Elevated indicators"
          value={String(elevated)}
          detail="score 60 or higher"
        />
        <MetricCard
          icon={ShieldCheck}
          label="Data quality"
          value={`${Math.round((quality.data?.data_quality_score ?? 0) * 100)}%`}
        />
      </div>
      <div className="content-grid">
        <Panel
          title="Player workload ranking"
          description="Top tracked distance for this match."
        >
          <WorkloadBars players={players.data} />
        </Panel>
        {quality.data && (
          <DataQualityPanel
            score={quality.data.data_quality_score}
            coverage={quality.data.player_metric_coverage}
            limitations={quality.data.limitations}
          />
        )}
      </div>
      <Panel title="Recent processing status">
        <div className="flex items-center justify-between gap-4">
          <div>
            <StatusBadge label={selectedMatch.processing_status} tone="success" />
            <p className="mt-2 text-sm text-[var(--muted)]">
              {selectedMatch.competition}
            </p>
          </div>
          <Link className="button-secondary" to={`/matches/${matchId}`}>
            Explore match
          </Link>
        </div>
      </Panel>
    </div>
  )
}
