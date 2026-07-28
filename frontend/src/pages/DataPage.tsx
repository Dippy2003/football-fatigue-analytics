import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Database, ExternalLink, UploadCloud } from 'lucide-react'
import { useState } from 'react'
import type { FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { ErrorState, LoadingState } from '../components/ui/AsyncState'
import { Panel } from '../components/ui/Panel'
import { StatusBadge } from '../components/ui/StatusBadge'
import {
  createDemo,
  getImportCapabilities,
  getSources,
  importLocalDataset,
} from '../services/api/datasets'
import { getApiErrorMessage } from '../services/api/client'

export function DataPage() {
  const navigate = useNavigate()
  const client = useQueryClient()
  const [formError, setFormError] = useState<string | null>(null)
  const sources = useQuery({
    queryKey: ['sources'],
    queryFn: ({ signal }) => getSources(signal),
  })
  const capabilities = useQuery({
    queryKey: ['import-capabilities'],
    queryFn: ({ signal }) => getImportCapabilities(signal),
  })
  const demo = useMutation({
    mutationFn: () => createDemo(),
    onSuccess: async (result) => {
      await client.invalidateQueries()
      void navigate(`/matches/${result.match_id}`)
    },
  })
  const localImport = useMutation({
    mutationFn: importLocalDataset,
    onSuccess: async (result) => {
      await client.invalidateQueries()
      void navigate(`/matches/${result.match_id}`)
    },
  })

  const submitImport = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setFormError(null)
    const fields = event.currentTarget.elements
    const sourceMatchId = (
      fields.namedItem('source_match_id') as HTMLInputElement
    ).value.trim()
    const competition = (
      fields.namedItem('competition') as HTMLInputElement
    ).value.trim()
    const tracking = (fields.namedItem('tracking') as HTMLInputElement).files?.[0]
    const events = (fields.namedItem('events') as HTMLInputElement).files?.[0]
    if (!tracking || tracking.size === 0) {
      setFormError('Choose a tracking CSV before processing.')
      return
    }
    localImport.mutate({
      sourceMatchId,
      competition: competition || 'Local authorized import',
      tracking,
      events: events && events.size > 0 ? events : undefined,
    })
  }

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <p className="eyebrow">Data management</p>
          <h1>Load data with its rights context intact.</h1>
          <p>Use the fictional demo or process an authorized local tracking export.</p>
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
              {getApiErrorMessage(demo.error)}
            </p>
          )}
        </Panel>

        <Panel
          title="Authorized local import"
          description="Metrica-compatible long-form tracking CSV; events are optional."
        >
          <UploadCloud aria-hidden="true" className="text-slate-500" />
          {capabilities.isPending ? (
            <LoadingState label="Checking local import availability" />
          ) : capabilities.isError ? (
            <ErrorState retry={() => void capabilities.refetch()} />
          ) : !capabilities.data.uploads_enabled ? (
            <div className="mt-4">
              <StatusBadge label="Disabled by server" tone="warning" />
              <p className="mt-3 text-sm text-[var(--muted)]">
                The public demo cannot accept third-party files. For an authorized local
                analysis, set <code>ENABLE_UPLOADS=true</code> and restart the API.
              </p>
            </div>
          ) : (
            <form className="import-form mt-4" onSubmit={submitImport}>
              <label>
                <span>Source match ID</span>
                <input
                  maxLength={100}
                  name="source_match_id"
                  pattern="[A-Za-z0-9._-]+"
                  placeholder="club-match-001"
                  required
                />
              </label>
              <label>
                <span>Competition or context</span>
                <input
                  maxLength={160}
                  name="competition"
                  placeholder="Authorized local analysis"
                />
              </label>
              <label>
                <span>Tracking CSV (required)</span>
                <input accept=".csv,text/csv" name="tracking" required type="file" />
              </label>
              <label>
                <span>Event CSV (optional)</span>
                <input accept=".csv,text/csv" name="events" type="file" />
              </label>
              <label className="rights-check">
                <input required type="checkbox" />
                <span>
                  I am authorized to use these files and have checked the current
                  provider terms.
                </span>
              </label>
              <button
                className="button-primary"
                disabled={localImport.isPending}
                type="submit"
              >
                {localImport.isPending ? 'Validating and processing…' : 'Process match'}
              </button>
              {(formError || localImport.isError) && (
                <p className="text-sm text-red-700" role="alert">
                  {formError ?? getApiErrorMessage(localImport.error)}
                </p>
              )}
              <p className="text-xs text-[var(--muted)]">
                Maximum {capabilities.data.max_upload_mb} MB per file and{' '}
                {capabilities.data.max_import_rows.toLocaleString()} combined rows. Raw
                uploads are deleted after processing; local derived Parquet stays in the
                ignored data workspace.
              </p>
            </form>
          )}
          <div className="mt-4 flex flex-wrap gap-3 text-sm">
            <a
              className="text-link"
              download
              href="/samples/playerpulse-fictional-tracking.csv"
            >
              Fictional tracking sample
            </a>
            <a
              className="text-link"
              download
              href="/samples/playerpulse-fictional-events.csv"
            >
              Fictional events sample
            </a>
            <a
              className="text-link"
              download
              href="/templates/metrica-tracking-template.csv"
            >
              Tracking template
            </a>
            <a
              className="text-link"
              download
              href="/templates/metrica-events-template.csv"
            >
              Events template
            </a>
          </div>
          <p className="mt-3 text-xs text-[var(--muted)]">
            To try the fictional samples, download both and use Source match ID{' '}
            <code>fictional-upload-003</code>.
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
