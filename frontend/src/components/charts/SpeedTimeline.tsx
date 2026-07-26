import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

import type { TimelinePoint } from '../../types/domain'

export function SpeedTimeline({ points }: { points: TimelinePoint[] }) {
  const data = points.slice(1).map((point, index) => {
    const previous = points[index]!
    const elapsed = point.timestamp_seconds - previous.timestamp_seconds
    const distance = Math.hypot(point.x - previous.x, point.y - previous.y)
    return {
      minute: point.timestamp_seconds / 60 + (point.period - 1) * 45,
      speed: elapsed > 0 ? Math.min(12.5, distance / elapsed) : 0,
      period: point.period,
    }
  })
  return (
    <div>
      <div className="h-72" aria-label="Sampled speed timeline in metres per second">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
            <XAxis dataKey="minute" unit=" min" tick={{ fill: 'var(--muted)' }} />
            <YAxis unit=" m/s" domain={[0, 'auto']} tick={{ fill: 'var(--muted)' }} />
            <Tooltip
              formatter={(value) => [
                `${Number(value).toFixed(2)} m/s`,
                'Estimated speed',
              ]}
            />
            <Line
              type="monotone"
              dataKey="speed"
              stroke="#0d9488"
              dot={false}
              strokeWidth={2}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <p className="text-xs text-[var(--muted)]">
        Accessible summary: sampled movement speed over match minutes, split by period.
      </p>
    </div>
  )
}
