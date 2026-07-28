import { lazy, Suspense } from 'react'
import type { ComponentType } from 'react'
import { createBrowserRouter, Outlet } from 'react-router-dom'

import { AppShell } from '../components/layout/AppShell'
import { LandingPage } from '../pages/LandingPage'
import { NotFoundPage } from '../pages/NotFoundPage'
import { LoadingState } from '../components/ui/AsyncState'

const loadPage = <T extends Record<string, ComponentType>>(
  importer: () => Promise<T>,
  exportName: keyof T,
) =>
  lazy(async () => {
    const module = await importer()
    return { default: module[exportName] }
  })

const DashboardPage = loadPage(() => import('../pages/DashboardPage'), 'DashboardPage')
const MatchesPage = loadPage(() => import('../pages/MatchesPage'), 'MatchesPage')
const MatchExplorerPage = loadPage(
  () => import('../pages/MatchExplorerPage'),
  'MatchExplorerPage',
)
const PlayerPage = loadPage(() => import('../pages/PlayerPage'), 'PlayerPage')
const ComparisonPage = loadPage(
  () => import('../pages/ComparisonPage'),
  'ComparisonPage',
)
const DataPage = loadPage(() => import('../pages/DataPage'), 'DataPage')
const MethodologyPage = loadPage(
  () => import('../pages/MethodologyPage'),
  'MethodologyPage',
)
const EthicsPage = loadPage(() => import('../pages/EthicsPage'), 'EthicsPage')
const AboutPage = loadPage(() => import('../pages/AboutPage'), 'AboutPage')

const deferred = (Page: ComponentType) => (
  <Suspense fallback={<LoadingState label="Loading page" />}>
    <Page />
  </Suspense>
)

export const router = createBrowserRouter([
  {
    element: (
      <AppShell>
        <Outlet />
      </AppShell>
    ),
    children: [
      { path: '/', element: <LandingPage /> },
      { path: '/dashboard', element: deferred(DashboardPage) },
      { path: '/matches', element: deferred(MatchesPage) },
      { path: '/matches/:matchId', element: deferred(MatchExplorerPage) },
      { path: '/matches/:matchId/players/:playerId', element: deferred(PlayerPage) },
      { path: '/matches/:matchId/compare', element: deferred(ComparisonPage) },
      { path: '/data', element: deferred(DataPage) },
      { path: '/methodology', element: deferred(MethodologyPage) },
      { path: '/ethics', element: deferred(EthicsPage) },
      { path: '/about', element: deferred(AboutPage) },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
])
