import { AxiosError } from 'axios'

import { getApiErrorMessage, shouldRetryQuery } from './client'

describe('API failure policy', () => {
  it('does not expose unknown error details', () => {
    expect(getApiErrorMessage(new Error('secret stack'))).toBe(
      'The request could not be completed.',
    )
  })

  it('does not retry client errors and bounds server retries', () => {
    const clientError = new AxiosError('missing', '404', undefined, undefined, {
      status: 404,
    } as never)
    expect(shouldRetryQuery(0, clientError)).toBe(false)
    expect(shouldRetryQuery(0, new Error('network'))).toBe(true)
    expect(shouldRetryQuery(2, new Error('network'))).toBe(false)
  })
})
