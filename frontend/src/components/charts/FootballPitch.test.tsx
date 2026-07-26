import { render, screen } from '@testing-library/react'

import { FootballPitch } from './FootballPitch'

describe('FootballPitch', () => {
  it('provides an accessible description for heatmap and trajectory layers', () => {
    render(
      <FootballPitch
        playerName="Synthetic Player 02"
        heatmap={{ rows: 1, columns: 2, max_count: 4, grid: [[2, 4]] }}
        trajectory={[
          { period: 1, timestamp_seconds: 0, x: 20, y: 30 },
          { period: 1, timestamp_seconds: 1, x: 21, y: 31 },
        ]}
      />,
    )
    expect(
      screen.getByRole('img', {
        name: /Synthetic Player 02 movement pitch/,
      }),
    ).toBeInTheDocument()
    expect(screen.getAllByText(/average position/i)).not.toHaveLength(0)
  })
})
