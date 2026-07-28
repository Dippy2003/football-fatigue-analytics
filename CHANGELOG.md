# Changelog

All notable changes to PlayerPulse will be documented here. The project uses
semantic versioning after the five development checkpoints.

## 1.0.0 - 2026-07-28

### Added

- Deterministic synthetic tracking/events, provider adapters, canonical
  schemas, cleaning, quality reports, Parquet output, and movement/event
  analytics.
- Complete persistence/API layer for datasets, matches, players, metrics,
  baselines, heatmaps, risk explanations, jobs, and safe uploads.
- Responsive reviewer interface with dashboard, exploration, analysis,
  comparison, data, methodology, ethics, themes, and accessible states.
- Desktop/mobile end-to-end and accessibility tests, PostgreSQL migration CI,
  dependency/secret/rights controls, and release verification.

### Changed

- Production origins, upload handling, API/browser errors, containers, Nginx,
  dependency versions, and route loading were hardened for release.

### Security

- Public demos remain synthetic; uploads remain disabled by default; no
  external raw data, untrusted models, credentials, or real athlete health data
  are distributed.

## 0.1.0 - Day 1 foundation

### Added

- FastAPI system endpoints, typed configuration, structured logging, database
  sessions, SQLAlchemy base fields, and Alembic foundation.
- Responsive React/TypeScript application shell, routes, typed API/query layer,
  Tailwind identity, tests, lint, type checking, and production build.
- Dockerfiles, Docker Compose, CI, rights registry, security controls, setup
  documentation, and reproducible Python/npm lockfiles.
