import { formatDistance, formatNumber, formatPercent, titleCase } from './format'

describe('safe presentation formatting', () => {
  it('never exposes undefined, NaN, or unexplained null values', () => {
    expect(formatNumber(Number.NaN)).toBe('Unavailable')
    expect(formatDistance(undefined)).toBe('Unavailable')
    expect(formatPercent(null)).toBe('Unavailable')
    expect(titleCase(undefined)).toBe('Unavailable')
  })

  it('adds readable units and labels', () => {
    expect(formatDistance(12_345)).toBe('12.35 km')
    expect(formatPercent(0.84)).toBe('84%')
    expect(titleCase('match_only')).toBe('Match Only')
  })
})
