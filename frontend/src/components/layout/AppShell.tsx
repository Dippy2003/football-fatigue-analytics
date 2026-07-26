import type { ReactNode } from 'react'
import { Menu, X } from 'lucide-react'
import { useState } from 'react'
import { NavLink } from 'react-router-dom'

import { ThemeToggle } from '../../app/theme'
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
  const [open, setOpen] = useState(false)
  return (
    <div className="min-h-screen text-[var(--text)]">
      <a
        href="#main-content"
        className="fixed left-4 top-3 z-50 -translate-y-20 rounded-md bg-slate-950 px-4 py-2 text-sm font-semibold text-white transition-transform focus:translate-y-0"
      >
        Skip to main content
      </a>
      <header className="app-header">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
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
              <span className="block text-xs text-[var(--muted)]">
                Performance indicators
              </span>
            </span>
          </NavLink>
          <div className="flex items-center gap-2">
            <ThemeToggle />
            <button
              className="icon-button lg:hidden"
              onClick={() => setOpen((value) => !value)}
              type="button"
              aria-expanded={open}
              aria-controls="primary-navigation"
              aria-label="Toggle navigation"
            >
              {open ? <X aria-hidden="true" /> : <Menu aria-hidden="true" />}
            </button>
          </div>
          <nav
            id="primary-navigation"
            className={`${open ? 'flex' : 'hidden'} absolute left-4 right-4 top-20 z-40 rounded-xl border border-[var(--border)] bg-[var(--surface)] p-3 shadow-xl lg:static lg:flex lg:border-0 lg:bg-transparent lg:p-0 lg:shadow-none`}
            aria-label="Primary navigation"
          >
            <ul className="flex w-full flex-col gap-1 lg:flex-row">
              {navigation.map((item) => (
                <li key={item.href}>
                  <NavLink
                    className={({ isActive }) =>
                      `inline-flex rounded-md px-3 py-2 text-sm font-medium hover:bg-[var(--surface-muted)] hover:text-[var(--primary)] ${
                        isActive
                          ? 'bg-[var(--surface-muted)] text-[var(--primary)]'
                          : 'text-[var(--muted)]'
                      }`
                    }
                    to={item.href}
                    onClick={() => setOpen(false)}
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
      <footer className="border-t border-[var(--border)] bg-[var(--surface)]">
        <div className="mx-auto max-w-7xl px-4 py-6 text-sm text-[var(--muted)] sm:px-6 lg:px-8">
          PlayerPulse provides performance-based indicators from available match data.
          It is not a medical diagnostic tool and must not be used as a substitute for
          qualified medical or sports-science assessment.
        </div>
      </footer>
    </div>
  )
}
