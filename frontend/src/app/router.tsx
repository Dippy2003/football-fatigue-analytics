import { createBrowserRouter, Outlet } from 'react-router-dom'

import { AppShell } from '../components/layout/AppShell'
import { LandingPage } from '../pages/LandingPage'
import { NotFoundPage } from '../pages/NotFoundPage'
import { PlaceholderPage } from '../pages/PlaceholderPage'

export const router = createBrowserRouter([
  {
    element: (
      <AppShell>
        <Outlet />
      </AppShell>
    ),
    children: [
      { path: '/', element: <LandingPage /> },
      {
        path: '/dashboard',
        element: (
          <PlaceholderPage
            eyebrow="Overview"
            title="Dashboard"
            description="Team workload, intensity, quality, and indicator summaries will appear here."
          />
        ),
      },
      {
        path: '/matches',
        element: (
          <PlaceholderPage
            eyebrow="Explore"
            title="Matches"
            description="Select a processed match and inspect its teams, players, source, and quality."
          />
        ),
      },
      {
        path: '/matches/:matchId',
        element: (
          <PlaceholderPage
            eyebrow="Match"
            title="Match explorer"
            description="The player table, team filters, quality panel, and comparison workflow will live here."
          />
        ),
      },
      {
        path: '/matches/:matchId/players/:playerId',
        element: (
          <PlaceholderPage
            eyebrow="Player"
            title="Player analysis"
            description="Movement, workload, timelines, baseline, confidence, and explainable indicators will live here."
          />
        ),
      },
      {
        path: '/matches/:matchId/compare',
        element: (
          <PlaceholderPage
            eyebrow="Compare"
            title="Player comparison"
            description="Compare two to four players with role-aware warnings and normalized metrics."
          />
        ),
      },
      {
        path: '/data',
        element: (
          <PlaceholderPage
            eyebrow="Manage"
            title="Data management"
            description="Load the deterministic demo or validate rights-gated local imports from this page."
          />
        ),
      },
      {
        path: '/methodology',
        element: (
          <PlaceholderPage
            eyebrow="Understand"
            title="Methodology"
            description="Review calculation defaults, data rights, confidence, limitations, and model behavior."
          />
        ),
      },
      {
        path: '/about',
        element: (
          <PlaceholderPage
            eyebrow="Project"
            title="About PlayerPulse"
            description="Read the product purpose, technology choices, ethical scope, and source acknowledgements."
          />
        ),
      },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
])
