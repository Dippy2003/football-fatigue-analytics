import AxeBuilder from '@axe-core/playwright'
import { expect, test } from '@playwright/test'

test('reviewer loads demo and reaches an explained player indicator', async ({
  page,
}) => {
  await page.goto('/')
  await expect(
    page.getByRole('heading', {
      name: 'Turn match movement into decisions you can explain.',
    }),
  ).toBeVisible()

  await page.getByRole('button', { name: /load demo match/i }).click()
  await expect(
    page.getByRole('heading', { name: 'Fictional Demonstration' }),
  ).toBeVisible()
  await expect(page.getByText('Synthetic demo').first()).toBeVisible()
  const analyse = page
    .getByRole('row')
    .filter({ hasText: 'Synthetic Player 01' })
    .getByRole('link', { name: 'Analyse' })
    .first()
  await expect(analyse).toBeVisible()
  await analyse.focus()
  await page.keyboard.press('Enter')
  await expect(page.getByRole('heading', { name: /Synthetic Player/ })).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Movement heatmap' })).toBeVisible()
  await expect(
    page.getByRole('heading', { name: 'Performance-risk indicator' }),
  ).toBeVisible()
  await expect(
    page.getByText('Sprint Frequency Decline', { exact: true }),
  ).toBeVisible()
  await expect(
    page.getByRole('progressbar', {
      name: 'Sprint Frequency Decline normalized score',
    }),
  ).toHaveAttribute('aria-valuenow', '100')
  await expect(page.getByText(/not a medical diagnostic tool/i).first()).toBeVisible()
})

test('landing page has no serious automated accessibility violations', async ({
  page,
}) => {
  await page.goto('/')
  const results = await new AxeBuilder({ page }).analyze()
  const serious = results.violations.filter(
    (violation) => violation.impact === 'serious' || violation.impact === 'critical',
  )
  expect(serious).toEqual([])
})

test('navigation is keyboard operable', async ({ page }, testInfo) => {
  await page.goto('/')
  if (testInfo.project.name === 'mobile-chromium') {
    const menu = page.getByRole('button', { name: 'Toggle navigation' })
    await expect(menu).toBeVisible()
    await menu.focus()
    await page.keyboard.press('Enter')
  }
  await expect(
    page.getByRole('navigation', { name: 'Primary navigation' }),
  ).toBeVisible()
  await page.getByRole('link', { name: 'Methodology', exact: true }).click()
  await expect(page.getByRole('heading', { name: 'Methodology' })).toBeVisible()
})

test('authorized local tracking CSV becomes an explorable match', async ({ page }) => {
  await page.goto('/data')
  await expect(
    page.getByRole('heading', { name: 'Load data with its rights context intact.' }),
  ).toBeVisible()
  await page.getByLabel('Source match ID').fill('fictional-upload-003')
  await page.getByLabel('Competition or context').fill('Fictional upload sample')
  await page
    .getByLabel('Tracking CSV (required)')
    .setInputFiles('public/samples/playerpulse-fictional-tracking.csv')
  await page
    .getByLabel('Event CSV (optional)')
    .setInputFiles('public/samples/playerpulse-fictional-events.csv')
  await page
    .getByRole('checkbox', { name: /I am authorized to use these files/ })
    .check()
  await page.getByRole('button', { name: 'Process match' }).click()

  await expect(
    page.getByRole('heading', { name: 'Fictional upload sample' }),
  ).toBeVisible()
  await expect(page.getByText('Local import').first()).toBeVisible()
  const analyse = page
    .getByRole('row')
    .filter({ hasText: 'home-06' })
    .getByRole('link', { name: 'Analyse' })
  await analyse.click()
  await expect(page.getByRole('heading', { name: 'home-06' })).toBeVisible()
  await expect(
    page.getByRole('heading', { name: 'Performance-risk indicator' }),
  ).toBeVisible()
  await expect(page.getByText('out of 100')).toBeVisible()
})
