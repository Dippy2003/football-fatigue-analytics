import type { LucideIcon } from 'lucide-react'

type MetricCardProps = {
  label: string
  value: string
  detail?: string
  icon: LucideIcon
}

export function MetricCard({ label, value, detail, icon: Icon }: MetricCardProps) {
  return (
    <article className="metric-card">
      <div className="metric-card-topline">
        <div className="metric-icon">
          <Icon aria-hidden="true" size={19} />
        </div>
        <span className="metric-spark" aria-hidden="true" />
      </div>
      <p>{label}</p>
      <strong>{value}</strong>
      {detail && <span>{detail}</span>}
    </article>
  )
}
