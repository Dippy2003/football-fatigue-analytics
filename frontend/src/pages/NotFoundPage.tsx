import { Link } from 'react-router-dom'

export function NotFoundPage() {
  return (
    <section className="rounded-2xl border border-[var(--border)] bg-white p-8 text-center shadow-sm">
      <p className="text-sm font-semibold text-emerald-700">404</p>
      <h1 className="mt-2 text-3xl font-bold text-slate-950">Page not found</h1>
      <p className="mt-3 text-slate-600">
        The PlayerPulse page you requested does not exist.
      </p>
      <Link
        to="/"
        className="mt-6 inline-flex rounded-lg bg-emerald-700 px-4 py-2 font-semibold text-white hover:bg-emerald-800"
      >
        Return home
      </Link>
    </section>
  )
}
