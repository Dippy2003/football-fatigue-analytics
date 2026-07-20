import { AppShell } from './components/layout/AppShell'

export default function App() {
  return (
    <AppShell>
      <section className="grid gap-8 rounded-2xl border border-[var(--border)] bg-white p-6 shadow-sm md:grid-cols-[1.4fr_1fr] md:p-10">
        <div>
          <p className="mb-3 text-sm font-semibold uppercase tracking-[0.18em] text-emerald-700">
            Explainable football analytics
          </p>
          <h1 className="max-w-3xl text-4xl font-bold tracking-tight text-slate-950 sm:text-5xl">
            See workload and performance changes in context.
          </h1>
          <p className="mt-5 max-w-2xl text-lg leading-8 text-slate-600">
            PlayerPulse turns match tracking and event data into movement, workload,
            quality, and non-medical performance indicators that analysts can inspect.
          </p>
        </div>
        <aside
          className="rounded-xl bg-slate-950 p-6 text-slate-100"
          aria-label="Day 1 status"
        >
          <p className="text-sm font-semibold text-emerald-300">
            Foundation checkpoint
          </p>
          <p className="mt-3 text-2xl font-bold">Application shell ready</p>
          <p className="mt-3 leading-7 text-slate-300">
            The deterministic demo and football analytics pipeline arrive in later
            tagged development phases.
          </p>
        </aside>
      </section>
    </AppShell>
  )
}
