import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { beforeEach, vi } from 'vitest'

import { DataPage } from './DataPage'
import {
  createDemo,
  getImportCapabilities,
  getSources,
  importLocalDataset,
} from '../services/api/datasets'

vi.mock('../services/api/datasets', () => ({
  createDemo: vi.fn(),
  getImportCapabilities: vi.fn(),
  getSources: vi.fn(),
  importLocalDataset: vi.fn(),
}))

const capabilities = {
  uploads_enabled: true,
  provider: 'metrica_sample_data' as const,
  tracking_required: true,
  events_optional: true,
  accepted_extensions: ['.csv'],
  max_upload_mb: 25,
  max_import_rows: 1_000_000,
}

function renderPage() {
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  })
  return render(
    <QueryClientProvider client={client}>
      <MemoryRouter>
        <DataPage />
      </MemoryRouter>
    </QueryClientProvider>,
  )
}

beforeEach(() => {
  vi.mocked(getSources).mockResolvedValue([])
  vi.mocked(getImportCapabilities).mockResolvedValue(capabilities)
  vi.mocked(createDemo).mockReset()
  vi.mocked(importLocalDataset).mockReset()
})

describe('authorized local import', () => {
  it('explains how to enable uploads when the server has disabled them', async () => {
    vi.mocked(getImportCapabilities).mockResolvedValue({
      ...capabilities,
      uploads_enabled: false,
    })

    renderPage()

    expect(await screen.findByText('Disabled by server')).toBeInTheDocument()
    expect(screen.getByText(/ENABLE_UPLOADS=true/)).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Process match' })).toBeNull()
  })

  it('submits rights-acknowledged tracking and optional event files', async () => {
    const user = userEvent.setup()
    vi.mocked(importLocalDataset).mockResolvedValue({
      dataset_import_id: 'dataset-1',
      match_id: 'match-1',
      player_count: 2,
      quality_score: 100,
      quality_confidence: 'high',
      limitations: [],
      is_synthetic: false,
      created: true,
    })
    renderPage()

    await user.type(
      await screen.findByLabelText('Source match ID'),
      'authorized-match-001',
    )
    await user.type(
      screen.getByLabelText('Competition or context'),
      'Training analysis',
    )
    const tracking = new File(['tracking'], 'tracking.csv', { type: 'text/csv' })
    const events = new File(['events'], 'events.csv', { type: 'text/csv' })
    await user.upload(screen.getByLabelText('Tracking CSV (required)'), tracking)
    await user.upload(screen.getByLabelText('Event CSV (optional)'), events)
    await user.click(
      screen.getByRole('checkbox', {
        name: /I am authorized to use these files/,
      }),
    )
    const submit = screen.getByRole('button', { name: 'Process match' })
    fireEvent.submit(submit.closest('form')!)

    await waitFor(() => expect(importLocalDataset).toHaveBeenCalledOnce())
    expect(vi.mocked(importLocalDataset).mock.calls[0]?.[0]).toEqual({
      sourceMatchId: 'authorized-match-001',
      competition: 'Training analysis',
      tracking,
      events,
    })
  })
})
