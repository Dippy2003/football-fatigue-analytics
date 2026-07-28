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

test('mobile navigation is keyboard operable', async ({ page }) => {
  await page.goto('/')
  const menu = page.getByRole('button', { name: 'Toggle navigation' })
  await expect(menu).toBeVisible()
  await menu.focus()
  await page.keyboard.press('Enter')
  await expect(
    page.getByRole('navigation', { name: 'Primary navigation' }),
  ).toBeVisible()
  await page.getByRole('link', { name: 'Methodology', exact: true }).click()
  await expect(page.getByRole('heading', { name: 'Methodology' })).toBeVisible()
})

test('authorized local tracking CSV becomes an explorable match', async ({ page }) => {
  const tracking = [
    'match_id,period,frame_id,timestamp_seconds,team_id,player_id,x,y,ball_x,ball_y',
    'browser-import-001,1,0,0.0,Home,Home_1,0.10,0.20,0.50,0.50',
    'browser-import-001,1,1,1.0,Home,Home_1,0.11,0.20,0.50,0.50',
    'browser-import-001,1,0,0.0,Away,Away_1,0.90,0.80,0.50,0.50',
    'browser-import-001,1,1,1.0,Away,Away_1,0.89,0.80,0.50,0.50',
  ].join('\n')

  await page.goto('/data')
  await expect(
    page.getByRole('heading', { name: 'Load data with its rights context intact.' }),
  ).toBeVisible()
  await page.getByLabel('Source match ID').fill('browser-import-001')
  await page.getByLabel('Competition or context').fill('Authorized browser test')
  await page.getByLabel('Tracking CSV (required)').setInputFiles({
    name: 'tracking.csv',
    mimeType: 'text/csv',
    buffer: Buffer.from(tracking),
  })
  await page
    .getByRole('checkbox', { name: /I am authorized to use these files/ })
    .check()
  await page.getByRole('button', { name: 'Process match' }).click()

  await expect(
    page.getByRole('heading', { name: 'Authorized browser test' }),
  ).toBeVisible()
  await expect(page.getByText('Local import').first()).toBeVisible()
  await expect(page.getByRole('cell', { name: 'Home_1' })).toBeVisible()
})
