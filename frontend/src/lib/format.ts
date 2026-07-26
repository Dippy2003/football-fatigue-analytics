export const formatNumber = (value: number | null | undefined, digits = 0) =>
  value == null || !Number.isFinite(value)
    ? 'Unavailable'
    : new Intl.NumberFormat('en', {
        maximumFractionDigits: digits,
        minimumFractionDigits: digits,
      }).format(value)

export const formatDistance = (metres: number | null | undefined) =>
  metres == null ? 'Unavailable' : `${formatNumber(metres / 1000, 2)} km`

export const formatPercent = (value: number | null | undefined) =>
  value == null ? 'Unavailable' : `${formatNumber(value * 100, 0)}%`

export const titleCase = (value: string | null | undefined) =>
  value
    ? value.replaceAll('_', ' ').replace(/\b\w/g, (letter) => letter.toUpperCase())
    : 'Unavailable'
