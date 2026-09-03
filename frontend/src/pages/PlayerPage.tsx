import { useQuery } from '@tanstack/react-query'
import { Activity, Clock, Gauge, Route, TimerReset, Zap } from 'lucide-react'
import { useParams } from 'react-router-dom'

import { FootballPitch } from '../components/charts/FootballPitch'
import { SpeedTimeline } from '../components/charts/SpeedTimeline'
import { ErrorState, LoadingState } from '../components/ui/AsyncState'
import { DataQualityPanel } from '../components/ui/DataQualityPanel'
import { MetricCard } from '../components/ui/MetricCard'
import { Panel } from '../components/ui/Panel'
import { RiskPanel } from '../components/ui/RiskPanel'
import { StatusBadge } from '../components/ui/StatusBadge'
import { formatDistance, formatNumber, formatPercent, titleCase } from '../lib/format'
import { getMatch } from '../services/api/matches'
import {
  getPlayerBaseline,
  getPlayerEvents,
  getPlayerHeatmap,
  getPlayerMetrics,
  getPlayerTimeline,
  getPlayer,
} from '../services/api/players'
import { getPlayerRisk } from '../services/api/risk'

export function PlayerPage() {
  const { matchId = '', playerId = '' } = useParams()
  const options = { enabled: Boolean(matchId && playerId) }
  const match = useQuery({
    queryKey: ['match', matchId],
    queryFn: ({ signal }) => getMatch(matchId, signal),
    enabled: Boolean(matchId),
  })
  const profile = useQuery({
    queryKey: ['player', playerId],
    queryFn: ({ signal }) => getPlayer(playerId, signal),
    enabled: Boolean(playerId),
  })
  const metrics = useQuery({
    queryKey: ['metrics', matchId, playerId],
    queryFn: ({ signal }) => getPlayerMetrics(matchId, playerId, signal),
    ...options,
  })
  const timeline = useQuery({
    queryKey: ['timeline', matchId, playerId],
    queryFn: ({ signal }) => getPlayerTimeline(matchId, playerId, signal),
    ...options,
  })
  const heatmap = useQuery({
    queryKey: ['heatmap', matchId, playerId],
    queryFn: ({ signal }) => getPlayerHeatmap(matchId, playerId, signal),
    ...options,
  })
  const risk = useQuery({
    queryKey: ['risk', matchId, playerId],
    queryFn: ({ signal }) => getPlayerRisk(matchId, playerId, signal),
    ...options,
  })
  const baseline = useQuery({
    queryKey: ['baseline', playerId],
    queryFn: ({ signal }) => getPlayerBaseline(playerId, signal),
    enabled: Boolean(playerId),
  })
  const events = useQuery({
    queryKey: ['events', matchId, playerId],
    queryFn: ({ signal }) => getPlayerEvents(matchId, playerId, signal),
    ...options,
  })
  if (profile.isPending || metrics.isPending)
    return <LoadingState label="Loading player analysis" />
  if (profile.isError || metrics.isError || !metrics.data)
    return <ErrorState retry={() => void profile.refetch()} />
  const item = metrics.data
  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <p className="eyebrow">Player analysis</p>
          <h1>{profile.data?.name}</h1>
          <p>
            {profile.data?.position ?? 'Role unavailable'} ·{' '}
            {formatNumber(item.playing_minutes, 1)} playing minutes
          </p>
        </div>
        <StatusBadge
          label={match.data?.is_synthetic ? 'Synthetic demo' : 'Local import'}
          tone={match.data?.is_synthetic ? 'info' : 'success'}
        />
      </header>
      <div className="metric-grid">
        <MetricCard
          icon={Route}
          label="Total distance"
          value={formatDistance(item.total_distance_m)}
        />
        <MetricCard
          icon={TimerReset}
          label="Distance / minute"
          value={`${formatNumber(item.distance_per_minute, 1)} m`}
        />
        <MetricCard
          icon={Activity}
          label="Average speed"
          value={`${formatNumber(item.average_speed_mps, 2)} m/s`}
        />
        <MetricCard
          icon={Zap}
          label="Maximum speed"
          value={`${formatNumber(item.max_speed_mps, 2)} m/s`}
        />
        <MetricCard
          icon={Gauge}
          label="Sprints"
          value={String(item.sprint_count)}
          detail={formatDistance(item.sprint_distance_m)}
        />
        <MetricCard
          icon={Clock}
          label="Median recovery"
          value={
            item.median_sprint_recovery_seconds == null
              ? 'Insufficient data'
              : `${formatNumber(item.median_sprint_recovery_seconds)} s`
          }
        />
      </div>
      <div className="content-grid">
        <Panel
          title="Movement heatmap"
          description="Processed tracking observations for this match."
        >
          <FootballPitch
            heatmap={heatmap.data}
            trajectory={timeline.data?.points}
            playerName={profile.data?.name}
          />
        </Panel>
        {risk.data ? (
          <RiskPanel risk={risk.data} />
        ) : (
          <LoadingState label="Loading risk explanation" />
        )}
      </div>
      <Panel
        title="Speed timeline"
        description="Downsampled movement-derived speed with units and match-minute labels."
      >
        {timeline.data ? (
          <SpeedTimeline points={timeline.data.points} />
        ) : (
          <LoadingState />
        )}
      </Panel>
      <div className="content-grid">
        <Panel title="Half and late-match comparison">
          <dl className="stat-list">
            <div>
              <dt>Second-half speed</dt>
              <dd>
                {item.second_half_speed_change_pct == null
                  ? 'Insufficient data'
                  : `${formatNumber(item.second_half_speed_change_pct, 1)}%`}
              </dd>
            </div>
            <div>
              <dt>Late sprint frequency</dt>
              <dd>
                {item.late_match_sprint_change_pct == null
                  ? 'Insufficient data'
                  : `${formatNumber(item.late_match_sprint_change_pct, 1)}%`}
              </dd>
            </div>
            <div>
              <dt>15-minute distance comparison</dt>
              <dd>
                {item.late_match_distance_change_pct == null
                  ? 'Insufficient data'
                  : `${formatNumber(item.late_match_distance_change_pct, 1)}%`}
              </dd>
            </div>
          </dl>
        </Panel>
        <Panel title="Baseline and confidence">
          <dl className="stat-list">
            <div>
              <dt>Baseline</dt>
              <dd>{titleCase(baseline.data?.baseline_type)}</dd>
            </div>
            <div>
              <dt>Confidence</dt>
              <dd>{formatPercent(baseline.data?.baseline_confidence)}</dd>
            </div>
            <div>
              <dt>Sample size</dt>
              <dd>{baseline.data?.sample_size ?? 'Unavailable'}</dd>
            </div>
          </dl>
          <p className="mt-4 text-sm text-[var(--muted)]">
            {baseline.data?.limitation}
          </p>
        </Panel>
      </div>
      <div className="content-grid">
        <Panel title="Event performance">
          <p className="text-sm text-[var(--muted)]">
            {events.data?.supported
              ? `${events.data.events.length} supported events are available. Change metrics are shown only when calculable.`
              : 'Insufficient data: event metrics are not supported.'}
          </p>
        </Panel>
        <DataQualityPanel
          score={item.data_quality_score}
          limitations={
            item.data_quality_score < 1
              ? ['Review missing or interpolated tracking before decisions.']
              : []
          }
        />
      </div>
    </div>
  )
}
