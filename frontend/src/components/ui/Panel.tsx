import type { ReactNode } from 'react'

type PanelProps = {
  children: ReactNode
  className?: string
  title?: string
  description?: string
}

export function Panel({ children, className = '', title, description }: PanelProps) {
  return (
    <section className={`panel ${className}`}>
      {title && <h2 className="text-lg font-bold text-[var(--text)]">{title}</h2>}
      {description && <p className="mt-1 text-sm text-[var(--muted)]">{description}</p>}
      <div className={title || description ? 'mt-5' : ''}>{children}</div>
    </section>
  )
}
