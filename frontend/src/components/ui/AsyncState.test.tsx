import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

import { EmptyState, ErrorState, LoadingState } from './AsyncState'

describe('remote data states', () => {
  it('announces loading and explains empty data', () => {
    render(
      <>
        <LoadingState label="Loading players" />
        <EmptyState message="No players match." />
      </>,
    )
    expect(screen.getByRole('status', { name: 'Loading players' })).toBeInTheDocument()
    expect(screen.getByText('No players match.')).toBeInTheDocument()
  })

  it('offers a keyboard-operable retry', async () => {
    const retry = vi.fn()
    const user = userEvent.setup()
    render(<ErrorState retry={retry} />)
    await user.click(screen.getByRole('button', { name: 'Try again' }))
    expect(retry).toHaveBeenCalledOnce()
  })
})
