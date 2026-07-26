import { AlertTriangle, Eye, ShieldCheck } from 'lucide-react'

import { Panel } from '../components/ui/Panel'
import { RISK_DISCLAIMER } from '../types/domain'

export function EthicsPage() {
  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <p className="eyebrow">Responsible interpretation</p>
          <h1>Ethics and limitations</h1>
          <p>Performance signals require human context and qualified review.</p>
        </div>
      </header>
      <div className="grid gap-4 md:grid-cols-3">
        <Panel title="Not medical">
          <AlertTriangle aria-hidden="true" />
          <p className="mt-3 text-sm text-[var(--muted)]">
            No diagnosis, injury prediction, treatment, or return-to-play instruction.
          </p>
        </Panel>
        <Panel title="Human review">
          <Eye aria-hidden="true" />
          <p className="mt-3 text-sm text-[var(--muted)]">
            Consider tactics, role, substitution, match state, environment, and sensor
            limitations.
          </p>
        </Panel>
        <Panel title="Data minimisation">
          <ShieldCheck aria-hidden="true" />
          <p className="mt-3 text-sm text-[var(--muted)]">
            The public demo contains fictional identities and no real health or
            biometric records.
          </p>
        </Panel>
      </div>
      <aside className="disclaimer">{RISK_DISCLAIMER}</aside>
    </div>
  )
}
