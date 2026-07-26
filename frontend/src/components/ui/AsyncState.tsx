import { AlertCircle, Inbox } from 'lucide-react'

export function LoadingState({ label = 'Loading analysis' }: { label?: string }) {
  return (
    <div className="grid gap-3" role="status" aria-label={label}>
      <span className="sr-only">{label}</span>
      {[1, 2, 3].map((item) => (
        <div
          key={item}
          className="h-20 animate-pulse rounded-xl bg-[var(--surface-muted)]"
        />
      ))}
    </div>
  )
}

export function EmptyState({
  title = 'No data available',
  message,
}: {
  title?: string
  message: string
}) {
  return (
    <div className="state-card">
      <Inbox aria-hidden="true" />
      <h2>{title}</h2>
      <p>{message}</p>
    </div>
  )
}

export function ErrorState({
  message = 'The requested data could not be loaded.',
  retry,
}: {
  message?: string
  retry?: () => void
}) {
  return (
    <div className="state-card state-error" role="alert">
      <AlertCircle aria-hidden="true" />
      <h2>Unable to load data</h2>
      <p>{message}</p>
      {retry && (
        <button className="button-secondary mt-3" onClick={retry} type="button">
          Try again
        </button>
      )}
    </div>
  )
}
