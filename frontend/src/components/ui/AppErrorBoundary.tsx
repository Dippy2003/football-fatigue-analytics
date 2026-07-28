import { Component } from 'react'
import type { ErrorInfo, ReactNode } from 'react'

type Props = { children: ReactNode }
type State = { failed: boolean }

export class AppErrorBoundary extends Component<Props, State> {
  state: State = { failed: false }

  static getDerivedStateFromError(): State {
    return { failed: true }
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    if (import.meta.env.DEV) {
      console.error('PlayerPulse render failure', error.name, info.componentStack)
    }
  }

  render() {
    if (this.state.failed) {
      return (
        <main className="mx-auto max-w-2xl p-8" role="alert">
          <h1 className="text-2xl font-bold">PlayerPulse could not render this page</h1>
          <p className="mt-3 text-[var(--muted)]">
            No analytical result was changed. Reload the page or return home.
          </p>
          <a className="button-primary mt-5" href="/">
            Return home
          </a>
        </main>
      )
    }
    return this.props.children
  }
}
