import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Database, ExternalLink, UploadCloud } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'

import { ErrorState, LoadingState } from '../components/ui/AsyncState'
import { Panel } from '../components/ui/Panel'
import { StatusBadge } from '../components/ui/StatusBadge'
import { createDemo, getSources } from '../services/api/datasets'

export function DataPage() {
  const navigate = useNavigate()
  const client = useQueryClient()
  const sources = useQuery({
    queryKey: ['sources'],
    queryFn: ({ signal }) => getSources(signal),
  })
  const demo = useMutation({
    mutationFn: () => createDemo(),
    onSuccess: async (result) => {
      await client.invalidateQueries()
      void navigate(`/matches/${result.match_id}`)
    },
  })
  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <p className="eyebrow">Data management</p>
          <h1>Load data with its rights context intact.</h1>
          <p>The public workflow defaults to deterministic fictional data.</p>
        </div>
      </header>
      <div className="content-grid">
        <Panel
          title="Deterministic demo"
          description="Project-owned synthetic tracking and events."
        >
          <Database aria-hidden="true" className="text-teal-700" />
          <button
            className="button-primary mt-5"
            disabled={demo.isPending}
            onClick={() => demo.mutate()}
            type="button"
          >
            {demo.isPending ? 'Processing…' : 'Load synthetic demo'}
          </button>
          {demo.isSuccess && (
            <p className="mt-3 text-sm" role="status">
              {demo.data.created ? 'Demo created.' : 'Existing demo loaded.'}
            </p>
          )}
          {demo.isError && (
            <p className="mt-3 text-sm text-red-700" role="alert">
              Backend unavailable. Start the API and retry.
            </p>
          )}
        </Panel>
        <Panel
          title="Local import"
          description="Uploads are disabled by default and validated by the backend."
        >
          <UploadCloud aria-hidden="true" className="text-slate-500" />
          <StatusBadge label="Unavailable in public demo" tone="warning" />
          <p className="mt-4 text-sm text-[var(--muted)]">
            CSV/JSON only; no archives, pickle, Joblib, secrets, health records, or
            unverified provider data.
          </p>
        </Panel>
      </div>
      <Panel title="Dataset sources and attribution">
        {sources.isPending ? (
          <LoadingState />
        ) : sources.isError ? (
          <ErrorState retry={() => void sources.refetch()} />
        ) : (
          <div className="grid gap-3">
            {sources.data.map((source) => (
              <article className="source-card" key={source.id}>
                <div>
                  <h2>{source.provider}</h2>
                  <p>{source.attribution}</p>
                </div>
                <StatusBadge
                  label={source.usage_status.replaceAll('_', ' ')}
                  tone={source.id === 'synthetic_playerpulse' ? 'success' : 'warning'}
                />
              </article>
            ))}
          </div>
        )}
        <p className="mt-5 text-sm text-[var(--muted)]">
          Review official terms through the links on the{' '}
          <Link className="text-link" to="/methodology">
            methodology page
          </Link>
          . <ExternalLink className="inline" aria-hidden="true" size={14} />
        </p>
      </Panel>
    </div>
  )
}
