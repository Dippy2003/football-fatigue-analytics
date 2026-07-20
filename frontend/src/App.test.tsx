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
        name: 'See workload and performance changes in context.',
      }),
    ).toBeInTheDocument()
    expect(screen.getByText(/not a medical diagnostic tool/i)).toBeInTheDocument()

    await user.click(screen.getByRole('link', { name: 'Dashboard' }))

    expect(
      await screen.findByRole('heading', { name: 'Dashboard' }),
    ).toBeInTheDocument()
  })
})
