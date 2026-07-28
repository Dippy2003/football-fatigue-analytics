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
      {(title || description) && (
        <header className="panel-header">
          {title && <h2>{title}</h2>}
          {description && <p>{description}</p>}
        </header>
      )}
      <div className={title || description ? 'mt-5' : ''}>{children}</div>
    </section>
  )
}
