import { ShieldCheck } from 'lucide-react'

import { formatPercent } from '../../lib/format'
import { Panel } from './Panel'
import { StatusBadge } from './StatusBadge'

export function DataQualityPanel({
  score,
  coverage,
  limitations = [],
}: {
  score: number
  coverage?: number
  limitations?: string[]
}) {
  const tone = score >= 0.8 ? 'success' : score >= 0.5 ? 'warning' : 'neutral'
  return (
    <Panel
      title="Data quality"
      description="Completeness and reliability are separate from risk."
    >
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-3xl font-bold">{formatPercent(score)}</p>
          {coverage != null && (
            <p className="text-sm text-[var(--muted)]">{coverage} player summaries</p>
          )}
        </div>
        <StatusBadge
          label={score >= 0.8 ? 'Strong coverage' : 'Review quality'}
          tone={tone}
        />
      </div>
      <div className="quality-track mt-4">
        <div
          className="quality-fill"
          style={{ width: `${Math.max(0, Math.min(100, score * 100))}%` }}
        />
      </div>
      {limitations.length > 0 && (
        <ul className="mt-4 space-y-2 text-sm text-[var(--muted)]">
          {limitations.map((item) => (
            <li className="flex gap-2" key={item}>
              <ShieldCheck aria-hidden="true" size={16} />
              {item}
            </li>
          ))}
        </ul>
      )}
    </Panel>
  )
}
