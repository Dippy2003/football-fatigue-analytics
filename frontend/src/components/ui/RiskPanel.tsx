import { AlertTriangle, Gauge } from 'lucide-react'

import { formatNumber, formatPercent, titleCase } from '../../lib/format'
import type { RiskAssessment } from '../../types/domain'
import { Panel } from './Panel'
import { StatusBadge } from './StatusBadge'

export function RiskPanel({ risk }: { risk: RiskAssessment }) {
  if (risk.assessment_status !== 'available' || risk.score == null) {
    return (
      <Panel title="Performance-risk indicator">
        <StatusBadge label="Insufficient data" tone="warning" />
        <p className="mt-4 text-sm text-[var(--muted)]">{risk.explanation}</p>
        <p className="disclaimer mt-4">{risk.disclaimer}</p>
      </Panel>
    )
  }
  return (
    <Panel
      title="Performance-risk indicator"
      description="Decision support, not a diagnosis."
    >
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="text-4xl font-bold">{formatNumber(risk.score)}</p>
          <p className="text-sm text-[var(--muted)]">out of 100</p>
        </div>
        <StatusBadge
          label={titleCase(risk.category)}
          tone={risk.score >= 60 ? 'warning' : 'success'}
        />
      </div>
      <p className="mt-4 flex items-center gap-2 text-sm">
        <Gauge aria-hidden="true" size={17} />
        Confidence {formatPercent(risk.confidence)}
      </p>
      <div className="mt-5 space-y-4">
        {risk.factors.map((factor) => (
          <div key={factor.name}>
            <div className="flex justify-between gap-4 text-sm">
              <span>{titleCase(factor.name)}</span>
              <strong>+{formatNumber(factor.contribution, 1)}</strong>
            </div>
            <div className="mt-1 h-2 overflow-hidden rounded-full bg-[var(--surface-muted)]">
              <div
                className="h-full bg-amber-500"
                style={{ width: `${Math.min(100, factor.normalized_value * 100)}%` }}
              />
            </div>
            <p className="mt-1 text-xs text-[var(--muted)]">{factor.explanation}</p>
          </div>
        ))}
      </div>
      <p className="disclaimer mt-5">
        <AlertTriangle aria-hidden="true" size={16} />
        {risk.disclaimer}
      </p>
    </Panel>
  )
}
