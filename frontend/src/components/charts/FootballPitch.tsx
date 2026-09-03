import type { Heatmap, TimelinePoint } from '../../types/domain'

type FootballPitchProps = {
  heatmap?: Heatmap
  trajectory?: TimelinePoint[]
  playerName?: string
}

export function FootballPitch({
  heatmap,
  trajectory = [],
  playerName = 'Player',
}: FootballPitchProps) {
  const cells =
    heatmap?.grid.flatMap((row, rowIndex) =>
      row.map((count, columnIndex) => ({ rowIndex, columnIndex, count })),
    ) ?? []
  const path = trajectory.map((point) => `${point.x},${point.y}`).join(' ')
  const average = trajectory.length
    ? {
        x: trajectory.reduce((sum, point) => sum + point.x, 0) / trajectory.length,
        y: trajectory.reduce((sum, point) => sum + point.y, 0) / trajectory.length,
      }
    : null
  return (
    <div>
      <svg
        className="pitch"
        viewBox="0 0 105 68"
        role="img"
        aria-labelledby="pitch-title pitch-description"
      >
        <title id="pitch-title">{playerName} movement pitch</title>
        <desc id="pitch-description">
          A standard football pitch with an occupancy heatmap, sampled trajectory, and
          average position.
        </desc>
        <rect width="105" height="68" fill="var(--pitch)" />
        {cells.map((cell) => (
          <rect
            key={`${cell.rowIndex}-${cell.columnIndex}`}
            x={cell.columnIndex * (105 / 12)}
            y={cell.rowIndex * (68 / 8)}
            width={105 / 12}
            height={68 / 8}
            fill="#f59e0b"
            opacity={
              heatmap?.max_count ? 0.05 + (0.72 * cell.count) / heatmap.max_count : 0
            }
          />
        ))}
        <g fill="none" stroke="var(--pitch-line)" strokeWidth=".45">
          <rect x="1" y="1" width="103" height="66" />
          <line x1="52.5" y1="1" x2="52.5" y2="67" />
          <circle cx="52.5" cy="34" r="9.15" />
          <rect x="1" y="13.84" width="16.5" height="40.32" />
          <rect x="87.5" y="13.84" width="16.5" height="40.32" />
          <rect x="1" y="24.84" width="5.5" height="18.32" />
          <rect x="98.5" y="24.84" width="5.5" height="18.32" />
        </g>
        {path && (
          <polyline
            points={path}
            fill="none"
            stroke="var(--trajectory)"
            strokeWidth=".65"
            opacity=".68"
            className="trajectory-line"
          />
        )}
        {average && (
          <circle
            cx={average.x}
            cy={average.y}
            r="1.8"
            fill="#fff"
            stroke="#0f766e"
            strokeWidth="1"
          />
        )}
      </svg>
      <p className="mt-2 text-xs text-[var(--muted)]">
        Heat intensity shows occupancy; the outlined marker shows average position.
      </p>
    </div>
  )
}
