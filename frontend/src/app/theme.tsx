import { Moon, Sun } from 'lucide-react'
import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import type { ReactNode } from 'react'

type Theme = 'light' | 'dark'
const ThemeContext = createContext<{ theme: Theme; toggle: () => void } | null>(null)

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>(() => {
    const stored = localStorage.getItem('playerpulse-theme')
    return stored === 'dark' ? 'dark' : 'light'
  })
  useEffect(() => {
    document.documentElement.dataset.theme = theme
    localStorage.setItem('playerpulse-theme', theme)
  }, [theme])
  const value = useMemo(
    () => ({
      theme,
      toggle: () => setTheme((current) => (current === 'light' ? 'dark' : 'light')),
    }),
    [theme],
  )
  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
}

export function ThemeToggle() {
  const context = useContext(ThemeContext)
  if (!context) return null
  return (
    <button
      className="icon-button"
      onClick={context.toggle}
      type="button"
      aria-label={`Switch to ${context.theme === 'light' ? 'dark' : 'light'} mode`}
    >
      {context.theme === 'light' ? (
        <Moon aria-hidden="true" />
      ) : (
        <Sun aria-hidden="true" />
      )}
    </button>
  )
}
