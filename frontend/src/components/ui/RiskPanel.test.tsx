import { render, screen } from '@testing-library/react'

import type { RiskAssessment } from '../../types/domain'
import { RiskPanel } from './RiskPanel'

const risk: RiskAssessment = {
  assessment_status: 'available',
  score: 62,
  category: 'High indicator level',
  confidence: 0.72,
  data_quality: 1,
  feature_coverage: 0.8,
  baseline_type: 'match_only',
  factors: [
    {
      factor: 'speed_decline',
      raw_value: 18,
      normalized_score: 60,
      effective_weight: 0.35,
      contribution: 21,
    },
  ],
  top_contributing_factors: ['speed_decline'],
  explanation: 'Review workload context.',
  limitations: [],
  disclaimer:
    'PlayerPulse provides performance-based indicators from available match data. It is not a medical diagnostic tool and must not be used as a substitute for qualified medical or sports-science assessment.',
  model_version: 'rule-risk-v1',
  calculated_at: '2026-07-26T00:00:00Z',
}

describe('RiskPanel', () => {
  it('shows score, label, confidence, factors, and disclaimer', () => {
    render(<RiskPanel risk={risk} />)
    expect(screen.getByText('62')).toBeInTheDocument()
    expect(screen.getByText('High Indicator Level')).toBeInTheDocument()
    expect(screen.getByText('Confidence 72%')).toBeInTheDocument()
    expect(screen.getByText('Speed Decline')).toBeInTheDocument()
    expect(
      screen.getByRole('progressbar', { name: 'Speed Decline normalized score' }),
    ).toHaveAttribute('aria-valuenow', '60')
    expect(screen.getByText('Input 18.0% · effective weight 35%')).toBeInTheDocument()
    expect(screen.getByText(/not a medical diagnostic tool/i)).toBeInTheDocument()
  })

  it('explains why an indicator was withheld', () => {
    render(
      <RiskPanel
        risk={{
          ...risk,
          assessment_status: 'insufficient_data',
          score: null,
          category: null,
          feature_coverage: 0.4,
          factors: [],
          top_contributing_factors: [],
          limitations: [
            'Fewer than three core physical factors are available.',
            'Feature coverage is below 60%.',
          ],
          explanation: 'A numeric performance-risk indicator was not issued.',
        }}
      />,
    )

    expect(screen.getByText('Insufficient data')).toBeInTheDocument()
    expect(screen.getByText('Feature coverage')).toBeInTheDocument()
    expect(screen.getByText('40%')).toBeInTheDocument()
    expect(
      screen.getByText('Fewer than three core physical factors are available.'),
    ).toBeInTheDocument()
  })
})
