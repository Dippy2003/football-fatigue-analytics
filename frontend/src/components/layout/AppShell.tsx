import type { ReactNode } from 'react'
import { NavLink } from 'react-router-dom'

import { BrandMark } from './BrandMark'

const navigation = [
  { href: '/', label: 'Home' },
  { href: '/dashboard', label: 'Dashboard' },
  { href: '/matches', label: 'Matches' },
  { href: '/data', label: 'Data' },
  { href: '/methodology', label: 'Methodology' },
  { href: '/about', label: 'About' },
]

type AppShellProps = {
  children: ReactNode
}

export function AppShell({ children }: AppShellProps) {
  return (
    <div className="min-h-screen text-slate-900">
      <a
        href="#main-content"
        className="fixed left-4 top-3 z-50 -translate-y-20 rounded-md bg-slate-950 px-4 py-2 text-sm font-semibold text-white transition-transform focus:translate-y-0"
      >
        Skip to main content
      </a>
      <header className="border-b border-[var(--border)] bg-white/95">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-4 sm:px-6 lg:flex-row lg:items-center lg:justify-between lg:px-8">
          <NavLink
            className="flex w-fit items-center gap-3"
            to="/"
            aria-label="PlayerPulse home"
          >
            <BrandMark />
            <span>
              <span className="block text-lg font-bold tracking-tight">
                PlayerPulse
              </span>
              <span className="block text-xs text-slate-500">
                Performance indicators
              </span>
            </span>
          </NavLink>
          <nav aria-label="Primary navigation">
            <ul className="flex flex-wrap gap-1">
              {navigation.map((item) => (
                <li key={item.href}>
                  <NavLink
                    className={({ isActive }) =>
                      `inline-flex rounded-md px-3 py-2 text-sm font-medium hover:bg-emerald-50 hover:text-emerald-800 ${
                        isActive ? 'bg-emerald-50 text-emerald-800' : 'text-slate-600'
                      }`
                    }
                    to={item.href}
                  >
                    {item.label}
                  </NavLink>
                </li>
              ))}
            </ul>
          </nav>
        </div>
      </header>
      <main
        id="main-content"
        className="mx-auto w-full max-w-7xl px-4 py-10 sm:px-6 lg:px-8"
      >
        {children}
      </main>
      <footer className="border-t border-[var(--border)] bg-white">
        <div className="mx-auto max-w-7xl px-4 py-6 text-sm text-slate-600 sm:px-6 lg:px-8">
          PlayerPulse provides performance-based indicators from available match data.
          It is not a medical diagnostic tool and must not replace qualified medical or
          sports-science assessment.
        </div>
      </footer>
    </div>
  )
}
