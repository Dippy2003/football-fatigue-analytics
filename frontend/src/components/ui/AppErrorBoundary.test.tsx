import { render, screen } from '@testing-library/react'

import { AppErrorBoundary } from './AppErrorBoundary'

function BrokenView(): never {
  throw new Error('private failure detail')
}

describe('AppErrorBoundary', () => {
  it('shows a safe recovery message without exception detail', () => {
    const consoleError = vi.spyOn(console, 'error').mockImplementation(() => undefined)
    render(
      <AppErrorBoundary>
        <BrokenView />
      </AppErrorBoundary>,
    )

    expect(screen.getByRole('alert')).toHaveTextContent('could not render')
    expect(screen.queryByText('private failure detail')).not.toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Return home' })).toHaveAttribute(
      'href',
      '/',
    )
    consoleError.mockRestore()
  })
})
