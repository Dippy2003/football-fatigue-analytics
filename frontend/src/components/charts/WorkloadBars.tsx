import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

import type { MatchPlayer } from '../../types/domain'

export function WorkloadBars({ players }: { players: MatchPlayer[] }) {
  const data = [...players]
    .sort((a, b) => b.total_distance_m - a.total_distance_m)
    .slice(0, 10)
    .map((player) => ({
      name: player.name.replace('Synthetic ', ''),
      distance: Math.round(player.total_distance_m),
    }))
  return (
    <div>
      <div className="h-72" aria-label="Top player workload ranking">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ left: 38 }}>
            <defs>
              <linearGradient id="workloadBar" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stopColor="var(--primary)" />
                <stop offset="100%" stopColor="var(--accent)" />
              </linearGradient>
            </defs>
            <CartesianGrid
              horizontal={false}
              strokeDasharray="3 6"
              stroke="var(--border)"
            />
            <XAxis type="number" unit=" m" tick={{ fill: 'var(--muted)' }} />
            <YAxis
              type="category"
              dataKey="name"
              width={76}
              tick={{ fill: 'var(--muted)', fontSize: 11 }}
            />
            <Tooltip
              formatter={(value) => [`${Number(value).toLocaleString()} m`, 'Distance']}
            />
            <Bar
              dataKey="distance"
              fill="url(#workloadBar)"
              radius={[0, 8, 8, 0]}
              animationDuration={900}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <p className="text-xs text-[var(--muted)]">
        Players ranked by total tracked distance in metres.
      </p>
    </div>
  )
}
