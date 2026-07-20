import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import App from './App'
import { AppProviders } from './app/providers'
import './styles.css'

const root = document.getElementById('root')

if (!root) {
  throw new Error('PlayerPulse root element was not found')
}

createRoot(root).render(
  <StrictMode>
    <AppProviders>
      <App />
    </AppProviders>
  </StrictMode>,
)
