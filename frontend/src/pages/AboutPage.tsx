import { Code2, Database, LineChart } from 'lucide-react'

import { Panel } from '../components/ui/Panel'
import { RISK_DISCLAIMER } from '../types/domain'

export function AboutPage() {
  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <p className="eyebrow">Portfolio project</p>
          <h1>About PlayerPulse</h1>
          <p>
            An end-to-end football analytics system focused on explainability, data
            quality, and responsible presentation.
          </p>
        </div>
      </header>
      <div className="grid gap-4 md:grid-cols-3">
        <Panel title="Product">
          <LineChart aria-hidden="true" />
          <p className="mt-3 text-sm text-[var(--muted)]">
            Reviewer-friendly exploration from synthetic match loading to player-level
            context.
          </p>
        </Panel>
        <Panel title="Engineering">
          <Code2 aria-hidden="true" />
          <p className="mt-3 text-sm text-[var(--muted)]">
            React, TypeScript, TanStack Query, Recharts, FastAPI, SQLAlchemy, Alembic
            and tested analytics.
          </p>
        </Panel>
        <Panel title="Data practice">
          <Database aria-hidden="true" />
          <p className="mt-3 text-sm text-[var(--muted)]">
            Deterministic synthetic defaults, provenance, rights gating and no bundled
            provider raw data.
          </p>
        </Panel>
      </div>
      <Panel title="Acknowledgements">
        <p className="text-sm text-[var(--muted)]">
          External adapter research references official Metrica Sports and Hudl
          StatsBomb repositories. No provider logo, player photograph, club badge or
          competition mark is bundled.
        </p>
        <a
          className="button-secondary mt-4"
          href="https://github.com/Dippy2003/football-fatigue-analytics"
        >
          View source code
        </a>
      </Panel>
      <aside className="disclaimer">{RISK_DISCLAIMER}</aside>
    </div>
  )
}
