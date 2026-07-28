import { AlertTriangle, Gauge } from 'lucide-react'

import { formatNumber, formatPercent, titleCase } from '../../lib/format'
import type { RiskAssessment } from '../../types/domain'
import { Panel } from './Panel'
import { StatusBadge } from './StatusBadge'

const factorInput = (factor: RiskAssessment['factors'][number]) =>
  factor.factor === 'workload_vs_baseline'
    ? `${formatNumber(factor.raw_value, 1)} z-score`
    : `${formatNumber(factor.raw_value, 1)}%`

export function RiskPanel({ risk }: { risk: RiskAssessment }) {
  if (risk.assessment_status !== 'available' || risk.score == null) {
    return (
      <Panel title="Performance-risk indicator">
        <StatusBadge label="Insufficient data" tone="warning" />
        <p className="mt-4 text-sm text-[var(--muted)]">{risk.explanation}</p>
        <dl className="stat-list mt-4">
          <div>
            <dt>Data quality</dt>
            <dd>{formatPercent(risk.data_quality)}</dd>
          </div>
          <div>
            <dt>Feature coverage</dt>
            <dd>{formatPercent(risk.feature_coverage)}</dd>
          </div>
          <div>
            <dt>Baseline</dt>
            <dd>{titleCase(risk.baseline_type)}</dd>
          </div>
        </dl>
        {risk.limitations.length > 0 && (
          <div className="mt-4">
            <h3 className="text-sm font-bold">Why no score was issued</h3>
            <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-[var(--muted)]">
              {risk.limitations.map((limitation) => (
                <li key={limitation}>{limitation}</li>
              ))}
            </ul>
          </div>
        )}
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
          <div key={factor.factor}>
            <div className="flex justify-between gap-4 text-sm">
              <span>{titleCase(factor.factor)}</span>
              <strong>+{formatNumber(factor.contribution, 1)}</strong>
            </div>
            <div
              aria-label={`${titleCase(factor.factor)} normalized score`}
              aria-valuemax={100}
              aria-valuemin={0}
              aria-valuenow={factor.normalized_score}
              className="mt-1 h-2 overflow-hidden rounded-full bg-[var(--surface-muted)]"
              role="progressbar"
            >
              <div
                className="h-full bg-amber-500"
                style={{
                  width: `${Math.min(100, Math.max(0, factor.normalized_score))}%`,
                }}
              />
            </div>
            <p className="mt-1 text-xs text-[var(--muted)]">
              Input {factorInput(factor)} · effective weight{' '}
              {formatPercent(factor.effective_weight)}
            </p>
          </div>
        ))}
      </div>
      {risk.explanation && (
        <p className="mt-5 text-sm text-[var(--muted)]">{risk.explanation}</p>
      )}
      <p className="disclaimer mt-5">
        <AlertTriangle aria-hidden="true" size={16} />
        {risk.disclaimer}
      </p>
    </Panel>
  )
}
