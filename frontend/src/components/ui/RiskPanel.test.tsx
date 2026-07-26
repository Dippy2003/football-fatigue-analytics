import { render, screen } from '@testing-library/react'

import type { RiskAssessment } from '../../types/domain'
import { RiskPanel } from './RiskPanel'

const risk: RiskAssessment = {
  assessment_status: 'available',
  score: 62,
  category: 'elevated',
  confidence: 0.72,
  factors: [
    {
      name: 'speed_decline',
      raw_value: 18,
      normalized_value: 0.6,
      configured_weight: 0.35,
      effective_weight: 0.35,
      contribution: 21,
      explanation: 'Late speed was lower than early speed.',
    },
  ],
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
    expect(screen.getByText('Elevated')).toBeInTheDocument()
    expect(screen.getByText('Confidence 72%')).toBeInTheDocument()
    expect(screen.getByText('Speed Decline')).toBeInTheDocument()
    expect(screen.getByText(/not a medical diagnostic tool/i)).toBeInTheDocument()
  })
})
