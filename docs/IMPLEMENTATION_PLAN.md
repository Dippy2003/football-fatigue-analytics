# PlayerPulse implementation plan

## Phase status

- Day 1: completed locally; checkpoint report/tag finalized at the end of this phase
- Days 2-5: not started

This plan follows the authoritative audited master prompt. A "day" is a tagged
development phase, not necessarily a calendar day. Each day ends with at least
30 meaningful atomic commits, a complete quality gate, a report, and an
annotated tag. Work never begins on the next day without explicit approval.

## Day 1: foundation and reproducibility

Goal: a working FastAPI system API, React application shell, SQLite/PostgreSQL
configuration, Alembic foundation, tests, lint/type/build checks, containers,
CI, security boundaries, rights documentation, and reproducible lockfiles.

Acceptance: system endpoints and frontend shell run; tests, static checks, and
frontend build pass; Compose validates; no secrets or restricted data exist;
30 or more meaningful commits and `day-1-complete` exist.

## Day 2: ingestion and football analytics

Goal: rights-gated provider adapters plus a deterministic synthetic match flow
through canonical schemas, validation, cleaning, coordinate conversion,
movement calculations, intensity, sprints, windows, event metrics, quality
scores, provenance, and Parquet output.

Acceptance: deterministic pipeline and analytics tests pass, external raw data
is neither required nor redistributed, and `day-2-complete` exists.

## Day 3: persistence, API, baseline, and risk

Goal: persist imports, teams, players, matches, metrics, jobs, and explainable
risk assessments; expose the versioned API; implement baseline selection,
transparent rule scoring, confidence, explanations, and a minimum-data-gated
Isolation Forest fallback.

Acceptance: clean migrations, demo processing, complete API tests, logical
synthetic risk scenarios, and `day-3-complete`.

## Day 4: complete reviewer interface

Goal: connect the real API to polished responsive pages for demo loading,
dashboard, match exploration, player analysis, heatmaps, charts, risk
explanation, comparison, quality, methodology, ethics, and data management.

Acceptance: the UI demo journey works with accessible light/dark layouts,
states and tests, and `day-4-complete` exists.

## Day 5: integration and portfolio release

Goal: harden security, accessibility, performance, containers, CI, deployment
configuration, full test coverage, documentation, screenshots, case study,
release checks, and clean-clone guidance.

Acceptance: end-to-end demo, all quality gates, migrations, Docker validation,
rights audit, at least 150 total meaningful commits, all daily tags,
`day-5-complete`, and `v1.0.0`.

## Cross-cutting controls

- Public examples use deterministic fictional data only.
- Risk language remains non-medical and explicitly limited.
- Data quality and missing support are visible, never silently invented.
- Lockfiles are generated, committed, and never edited manually.
- Progress and decisions are persisted after substantial work.
- External deployment, remote creation, pushes, and releases require explicit
  user authorization.
