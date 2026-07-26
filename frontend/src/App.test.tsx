import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

import App from './App'
import { AppProviders } from './app/providers'

describe('PlayerPulse application shell', () => {
  it('renders the landing page and navigates without a page reload', async () => {
    const user = userEvent.setup()
    render(
      <AppProviders>
        <App />
      </AppProviders>,
    )

    expect(
      screen.getByRole('heading', {
        name: 'Turn match movement into decisions you can explain.',
      }),
    ).toBeInTheDocument()
    expect(screen.getAllByText(/not a medical diagnostic tool/i)).not.toHaveLength(0)

    await user.click(screen.getByRole('link', { name: 'Methodology' }))

    expect(
      await screen.findByRole('heading', { name: 'Methodology' }),
    ).toBeInTheDocument()
  })

  it('supports a keyboard-accessible theme toggle', async () => {
    const user = userEvent.setup()
    render(
      <AppProviders>
        <App />
      </AppProviders>,
    )

    const toggle = screen.getByRole('button', { name: 'Switch to dark mode' })
    toggle.focus()
    await user.keyboard('{Enter}')

    expect(document.documentElement).toHaveAttribute('data-theme', 'dark')
    expect(
      screen.getByRole('button', { name: 'Switch to light mode' }),
    ).toBeInTheDocument()
  })
})
