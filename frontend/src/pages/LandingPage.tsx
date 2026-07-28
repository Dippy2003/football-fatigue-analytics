import { useMutation, useQueryClient } from '@tanstack/react-query'
import {
  Activity,
  ArrowRight,
  ArrowUpRight,
  BarChart3,
  Gauge,
  ShieldCheck,
  Sparkles,
  Zap,
} from 'lucide-react'
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
    <div className="landing-page">
      <section className="hero">
        <div className="hero-copy-wrap">
          <div className="hero-kicker">
            <span className="hero-kicker-dot" />
            Explainable football analytics
          </div>
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
            <Link className="button-secondary" to="/dashboard">
              Open dashboard
              <ArrowUpRight aria-hidden="true" size={17} />
            </Link>
          </div>
          {demo.isError && (
            <p className="mt-3 text-sm text-red-700" role="alert">
              The API is unavailable. Start the backend and try again.
            </p>
          )}
          <div className="hero-trust-row" aria-label="Analysis principles">
            <span>
              <ShieldCheck aria-hidden="true" size={15} />
              Quality gated
            </span>
            <span>
              <Sparkles aria-hidden="true" size={15} />
              Fully explainable
            </span>
            <span>
              <Zap aria-hidden="true" size={15} />
              Deterministic
            </span>
          </div>
        </div>
        <div className="hero-visual" aria-label="PlayerPulse analysis summary">
          <div className="visual-topline">
            <span>
              <span className="live-dot" />
              Analysis live
            </span>
            <span>90:00</span>
          </div>
          <div className="radar-stage" aria-hidden="true">
            <span className="radar-ring radar-ring-one" />
            <span className="radar-ring radar-ring-two" />
            <span className="radar-ring radar-ring-three" />
            <span className="radar-sweep" />
            <span className="radar-player radar-player-one" />
            <span className="radar-player radar-player-two" />
            <span className="radar-player radar-player-three" />
            <Activity className="radar-core" size={25} />
          </div>
          <div className="visual-metrics">
            <div>
              <span>Players</span>
              <strong>20</strong>
            </div>
            <div>
              <span>Quality</span>
              <strong>97%</strong>
            </div>
            <div>
              <span>Signals</span>
              <strong>Live</strong>
            </div>
          </div>
          <div className="visual-caption">
            <Gauge aria-hidden="true" size={18} />
            <span>
              <strong>Synthetic demo</strong>
              <small>Transparent calculations, no black box</small>
            </span>
          </div>
        </div>
      </section>
      <section className="feature-grid" aria-label="Supported analysis">
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
        ).map(([title, copy, Icon], index) => (
          <article className="feature-card" key={String(title)}>
            <div className="feature-card-topline">
              <span>0{index + 1}</span>
              <Icon aria-hidden="true" />
            </div>
            <h2>{String(title)}</h2>
            <p>{String(copy)}</p>
            <span className="feature-card-line" aria-hidden="true" />
          </article>
        ))}
      </section>
      <section className="landing-integrity">
        <div>
          <p className="eyebrow">Built for responsible review</p>
          <h2>Useful signals. Honest limits.</h2>
          <p>{RISK_DISCLAIMER}</p>
        </div>
        <Link className="button-secondary" to="/methodology">
          Review methodology
          <ArrowRight aria-hidden="true" size={17} />
        </Link>
      </section>
      <p className="landing-source-note">
        Public demonstrations use project-owned synthetic data.{' '}
        <Link className="text-link" to="/data">
          Review data sources and rights
        </Link>
        .
      </p>
    </div>
  )
}
