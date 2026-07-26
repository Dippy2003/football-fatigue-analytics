import { createBrowserRouter, Outlet } from 'react-router-dom'

import { AppShell } from '../components/layout/AppShell'
import { AboutPage } from '../pages/AboutPage'
import { ComparisonPage } from '../pages/ComparisonPage'
import { DashboardPage } from '../pages/DashboardPage'
import { DataPage } from '../pages/DataPage'
import { EthicsPage } from '../pages/EthicsPage'
import { LandingPage } from '../pages/LandingPage'
import { MatchesPage } from '../pages/MatchesPage'
import { MatchExplorerPage } from '../pages/MatchExplorerPage'
import { MethodologyPage } from '../pages/MethodologyPage'
import { NotFoundPage } from '../pages/NotFoundPage'
import { PlayerPage } from '../pages/PlayerPage'

export const router = createBrowserRouter([
  {
    element: (
      <AppShell>
        <Outlet />
      </AppShell>
    ),
    children: [
      { path: '/', element: <LandingPage /> },
      { path: '/dashboard', element: <DashboardPage /> },
      { path: '/matches', element: <MatchesPage /> },
      { path: '/matches/:matchId', element: <MatchExplorerPage /> },
      { path: '/matches/:matchId/players/:playerId', element: <PlayerPage /> },
      { path: '/matches/:matchId/compare', element: <ComparisonPage /> },
      { path: '/data', element: <DataPage /> },
      { path: '/methodology', element: <MethodologyPage /> },
      { path: '/ethics', element: <EthicsPage /> },
      { path: '/about', element: <AboutPage /> },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
])
