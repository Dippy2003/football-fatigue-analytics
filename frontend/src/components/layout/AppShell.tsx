import type { ReactNode } from 'react'
import {
  BarChart3,
  Database,
  FileSearch,
  Home,
  Info,
  Menu,
  Radio,
  Trophy,
  X,
} from 'lucide-react'
import type { LucideIcon } from 'lucide-react'
import { useState } from 'react'
import { NavLink } from 'react-router-dom'

import { ThemeToggle } from '../../app/theme'
import { BrandMark } from './BrandMark'

const navigation = [
  { href: '/', label: 'Home', icon: Home },
  { href: '/dashboard', label: 'Dashboard', icon: BarChart3 },
  { href: '/matches', label: 'Matches', icon: Trophy },
  { href: '/data', label: 'Data', icon: Database },
  { href: '/methodology', label: 'Methodology', icon: FileSearch },
  { href: '/about', label: 'About', icon: Info },
] satisfies Array<{ href: string; label: string; icon: LucideIcon }>

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
        <div className="header-inner">
          <NavLink className="brand-link" to="/" aria-label="PlayerPulse home">
            <BrandMark />
            <span className="brand-copy">
              <span>PlayerPulse</span>
              <small>Football intelligence</small>
            </span>
          </NavLink>
          <nav
            id="primary-navigation"
            className={`primary-navigation ${open ? 'nav-open' : ''}`}
            aria-label="Primary navigation"
          >
            <ul>
              {navigation.map((item) => (
                <li key={item.href}>
                  <NavLink
                    className={({ isActive }) =>
                      `nav-link ${isActive ? 'nav-link-active' : ''}`
                    }
                    to={item.href}
                    onClick={() => setOpen(false)}
                  >
                    <item.icon aria-hidden="true" size={15} />
                    {item.label}
                  </NavLink>
                </li>
              ))}
            </ul>
          </nav>
          <div className="header-actions">
            <span className="system-status">
              <Radio aria-hidden="true" size={13} />
              Live
            </span>
            <ThemeToggle />
            <button
              className="icon-button menu-button"
              onClick={() => setOpen((value) => !value)}
              type="button"
              aria-expanded={open}
              aria-controls="primary-navigation"
              aria-label="Toggle navigation"
            >
              {open ? <X aria-hidden="true" /> : <Menu aria-hidden="true" />}
            </button>
          </div>
        </div>
      </header>
      <main id="main-content" className="app-main">
        {children}
      </main>
      <footer className="app-footer">
        <div className="footer-inner">
          <div className="footer-brand">
            <BrandMark />
            <span>
              <strong>PlayerPulse</strong>
              <small>Evidence-led football analytics</small>
            </span>
          </div>
          <p>
            PlayerPulse provides performance-based indicators from available match data.
            It is not a medical diagnostic tool and must not be used as a substitute for
            qualified medical or sports-science assessment.
          </p>
        </div>
      </footer>
    </div>
  )
}
