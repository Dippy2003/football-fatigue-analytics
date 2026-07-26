import { useMutation, useQueryClient } from '@tanstack/react-query'
import { Activity, ArrowRight, BarChart3, ShieldCheck } from 'lucide-react'
import type { LucideIcon } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'

import { createDemo } from '../services/api/datasets'
import { RISK_DISCLAIMER } from '../types/domain'

export function LandingPage() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const demo = useMutation({
    mutationFn: () => createDemo(),
    onSuccess: async (result) => {
      await queryClient.invalidateQueries()
      void navigate(`/matches/${result.match_id}`)
    },
  })
  return (
    <div className="space-y-8">
      <section className="hero">
        <div>
          <p className="eyebrow">Explainable football analytics</p>
          <h1>Turn match movement into decisions you can explain.</h1>
          <p className="hero-copy">
            Explore workload, speed changes, match context, data quality, and
            transparent performance-risk indicators using a deterministic fictional
            match.
          </p>
          <div className="mt-7 flex flex-wrap gap-3">
            <button
              className="button-primary"
              disabled={demo.isPending}
              onClick={() => demo.mutate()}
              type="button"
            >
              {demo.isPending ? 'Loading demo…' : 'Load demo match'}{' '}
              <ArrowRight aria-hidden="true" size={18} />
            </button>
            <Link className="button-secondary" to="/methodology">
              Review methodology
            </Link>
          </div>
          {demo.isError && (
            <p className="mt-3 text-sm text-red-700" role="alert">
              The API is unavailable. Start the backend and try again.
            </p>
          )}
        </div>
        <div className="hero-visual" aria-label="PlayerPulse analysis summary">
          <Activity aria-hidden="true" size={38} />
          <strong>Synthetic demo</strong>
          <p>20 fictional players · two teams · transparent calculations</p>
        </div>
      </section>
      <section className="grid gap-4 md:grid-cols-3" aria-label="Supported analysis">
        {(
          [
            [
              'Workload context',
              'Distance, speed, intensity, sprints, and match windows.',
              BarChart3,
            ],
            [
              'Explainable indicators',
              'Factors, confidence, limitations, and alternative explanations.',
              Activity,
            ],
            [
              'Quality first',
              'Missing support is shown instead of silently invented.',
              ShieldCheck,
            ],
          ] satisfies Array<[string, string, LucideIcon]>
        ).map(([title, copy, Icon]) => (
          <article className="feature-card" key={String(title)}>
            <Icon aria-hidden="true" />
            <h2>{String(title)}</h2>
            <p>{String(copy)}</p>
          </article>
        ))}
      </section>
      <aside className="disclaimer">
        <ShieldCheck aria-hidden="true" size={18} />
        {RISK_DISCLAIMER}
      </aside>
      <p className="text-sm text-[var(--muted)]">
        Public demonstrations use project-owned synthetic data. See{' '}
        <Link className="text-link" to="/data">
          data sources and rights
        </Link>
        .
      </p>
    </div>
  )
}
