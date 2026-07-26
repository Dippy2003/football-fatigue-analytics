import { Link } from 'react-router-dom'

import { Panel } from '../components/ui/Panel'
import { RISK_DISCLAIMER } from '../types/domain'

const sections = [
  [
    'Coordinates and movement',
    'Provider coordinates are normalized to a 105 × 68 metre pitch. Ordered positions produce step distance, speed and acceleration after quality-aware cleaning.',
  ],
  [
    'Sprints and windows',
    'The configurable portfolio default identifies sustained high-speed movement and summarises workload in transparent fifteen-minute windows.',
  ],
  [
    'Baseline selection',
    'Personal history is preferred, then team/position context, then match-only context. Every result exposes sample size, confidence and limitations.',
  ],
  [
    'Performance-risk indicator',
    'rule-risk-v1 combines normalized speed decline, sprint-frequency decline, workload deviation and supported event change. Available weights are renormalized; insufficient coverage is refused.',
  ],
  [
    'Anomaly signal',
    'Isolation Forest is optional, separate, deterministic and disabled below its minimum valid-row gate. It has no labelled medical ground truth.',
  ],
  [
    'Confidence and limitations',
    'Confidence reflects data quality, baseline support and feature coverage. It is never presented as injury probability or diagnostic certainty.',
  ],
]

export function MethodologyPage() {
  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <p className="eyebrow">Transparent by design</p>
          <h1>Methodology</h1>
          <p>How PlayerPulse processes, compares and limits its football analytics.</p>
        </div>
      </header>
      <div className="grid gap-4 md:grid-cols-2">
        {sections.map(([title, copy]) => (
          <Panel key={title} title={title}>
            <p className="text-sm leading-6 text-[var(--muted)]">{copy}</p>
          </Panel>
        ))}
      </div>
      <Panel title="Data sources and rights">
        <p className="text-sm text-[var(--muted)]">
          The public demo uses PlayerPulse synthetic data. External adapters are local
          and rights-gated.
        </p>
        <ul className="mt-4 space-y-2 text-sm">
          <li>
            <a
              className="text-link"
              href="https://github.com/metrica-sports/sample-data"
            >
              Official Metrica Sports sample repository
            </a>
          </li>
          <li>
            <a className="text-link" href="https://github.com/hudl/open-data">
              Official Hudl StatsBomb Open Data repository
            </a>
          </li>
        </ul>
      </Panel>
      <aside className="disclaimer">{RISK_DISCLAIMER}</aside>
      <p>
        <Link className="text-link" to="/ethics">
          Read the full ethics and limitations summary
        </Link>
        .
      </p>
    </div>
  )
}
