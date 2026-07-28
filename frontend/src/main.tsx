import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import App from './App'
import { AppProviders } from './app/providers'
import { AppErrorBoundary } from './components/ui/AppErrorBoundary'
import './styles.css'

const root = document.getElementById('root')

if (!root) {
  throw new Error('PlayerPulse root element was not found')
}

createRoot(root).render(
  <StrictMode>
    <AppProviders>
      <AppErrorBoundary>
        <App />
      </AppErrorBoundary>
    </AppProviders>
  </StrictMode>,
)
