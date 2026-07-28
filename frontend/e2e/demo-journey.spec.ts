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
  const analyse = page.getByRole('link', { name: 'Analyse' }).first()
  await expect(analyse).toBeVisible()
  await analyse.focus()
  await page.keyboard.press('Enter')
  await expect(page.getByRole('heading', { name: /Synthetic Player/ })).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Movement heatmap' })).toBeVisible()
  await expect(
    page.getByRole('heading', { name: 'Performance-risk indicator' }),
  ).toBeVisible()
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
