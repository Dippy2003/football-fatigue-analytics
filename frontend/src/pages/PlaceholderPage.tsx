type PlaceholderPageProps = {
  eyebrow: string
  title: string
  description: string
}

export function PlaceholderPage({ eyebrow, title, description }: PlaceholderPageProps) {
  return (
    <section className="rounded-2xl border border-[var(--border)] bg-white p-6 shadow-sm sm:p-10">
      <p className="text-sm font-semibold uppercase tracking-[0.16em] text-emerald-700">
        {eyebrow}
      </p>
      <h1 className="mt-3 text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
        {title}
      </h1>
      <p className="mt-4 max-w-2xl text-lg leading-8 text-slate-600">{description}</p>
      <div className="mt-8 rounded-xl border border-dashed border-slate-300 bg-slate-50 p-5 text-sm text-slate-600">
        This route is active. Its data-driven experience is scheduled for the documented
        development phase.
      </div>
    </section>
  )
}
