import { AlertTriangle, CheckCircle2, Database, Info } from 'lucide-react'

type StatusBadgeProps = {
  label: string
  tone?: 'success' | 'warning' | 'info' | 'neutral'
}

export function StatusBadge({ label, tone = 'neutral' }: StatusBadgeProps) {
  const Icon =
    tone === 'success'
      ? CheckCircle2
      : tone === 'warning'
        ? AlertTriangle
        : tone === 'info'
          ? Info
          : Database
  return (
    <span className={`status-badge status-${tone}`}>
      <Icon aria-hidden="true" size={14} />
      {label}
    </span>
  )
}
