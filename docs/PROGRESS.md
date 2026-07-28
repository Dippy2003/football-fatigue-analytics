# PlayerPulse progress

## Current checkpoint

- Development phase: post-1.0 local tracking import feature
- Branch: `main` (no phase-named branch)
- Runtime version: `1.0.0`
- Starting release tag: `v1.0.0` at `8cd4861`
- Feature commits: `87fcfbd`, `f9ca181`, and `169b0a9`
- Remote state: local `main` contains unpushed work; no push or deployment was
  performed
- Next exact action: update the generated commit ledger, commit the verified
  checkpoint, and report the local enablement/import steps

## Local tracking import completed

- Added a capability endpoint and a disabled-by-default, rights-acknowledged
  multipart CSV workflow for Metrica-compatible long-form tracking.
- Validates declared files, basename, media type, byte and row limits, canonical
  columns, coordinate bounds, source match identity, exactly two teams, and
  player membership.
- Removes raw temporary uploads after processing; stores checksummed provenance,
  relational summaries, and ignored derived Parquet.
- Serves imported timelines, heatmaps, event rows, workload metrics, quality,
  baseline context, and explainable performance-risk results through existing
  APIs.
- Added an accessible Data-page form, downloadable tracking/event templates,
  server-disabled guidance, local-import labels, and automatic navigation to
  the processed match.
- Added downloadable deterministic fictional tracking and event samples with
  20 players, two periods, explicit synthetic markers, and a reproducible
  generator; the files process directly through the local-import form.
- Added API security/idempotency tests, an API-to-analytics integration test,
  frontend form tests, and desktop/mobile browser import coverage.
- The local workflow does not accept StatsBomb event-only files because the
  system requires tracking for movement and workload indicators.

## Feature verification evidence

| Check | Result | Evidence |
| --- | --- | --- |
| Backend format/lint/types | Passed | Ruff 126 files; mypy 125 source files |
| Backend full suite | Passed | 139 tests; 2 non-failing framework/cache warnings |
| Frontend format/lint/types | Passed | Prettier, ESLint, TypeScript clean |
| Frontend unit suite | Passed | 8 files, 14 tests |
| Frontend production build | Passed | 2,366 modules |
| Browser journeys | Passed | 8 desktop/mobile tests, including local import |
| Dataset and secret checks | Passed | No prohibited tracked data or secrets |
| Docker Compose syntax | Passed | Configuration parsed quietly |
| Docker runtime | Skipped | Docker Desktop engine was unavailable |

## Release hardening completed

- Added defensive API/Nginx headers, strict production CORS validation,
  streamed upload limits/media checks, safe frontend errors, bounded retries,
  and a render error boundary.
- Serialized demo persistence under concurrent requests and cached synthetic
  generation with copy isolation.
- Split analytical routes into production chunks and kept mobile table actions
  reachable.
- Added integration/edge/security tests plus desktop/mobile Playwright demo,
  Axe accessibility, and keyboard-navigation coverage.
- Hardened unprivileged containers and reduced Compose privileges.
- Expanded CI for browser tests, PostgreSQL migration cycles, rights/secret
  scans, dependency checks, and diagnostic artifacts.
- Added Dependabot, tracked-secret and release invariant verifiers.
- Re-verified official Metrica and StatsBomb terms/commits/hashes without
  importing raw data or provider marks.
- Finalized README, architecture, deployment, testing, data dictionary, data
  card, ethics, model/methodology, security, release checklist, and changelog.

## Latest verified evidence

| Check | Result | Evidence |
| --- | --- | --- |
| Backend format/lint/types | Passed | Ruff 124 files; mypy 123 source files |
| Backend full suite | Passed | 135 tests; 97% coverage; 2 non-failing framework/cache warnings |
| Frontend format/lint/types | Passed | Prettier, ESLint, TypeScript clean |
| Frontend unit suite | Passed | 7 files, 11 tests |
| Frontend production build | Passed | 2,366 modules; route chunks emitted |
| Browser journey | Passed | 6 desktop/mobile journey, Axe, keyboard checks |
| Clean SQLite migrations | Passed | upgrade, downgrade to base, upgrade |
| Clean-clone gate | Passed | locked install, 135 backend tests, 11 frontend tests, build |
| Python dependency audit | Passed | no known vulnerabilities |
| npm critical audit | Passed | no critical issue; scoped high RSC advisory documented |
| Rights/secret/release checks | Passed | all three project verifiers |
| Docker Compose syntax | Passed | configuration parsed quietly |
| Docker build/runtime | Skipped | Docker Desktop engine unavailable |
| Synthetic pipeline profile | Passed | cold 1.556 s; warm 0.413/0.432 s |

## Known limitations

- Docker images/stack were not runtime-tested because the installed Docker CLI
  could not connect to Docker Desktop's Linux engine.
- PostgreSQL migration behavior is configured in CI but was not locally
  executed because no local PostgreSQL service was available.
- npm reports a high React Router advisory limited to RSC/server-action mode.
  PlayerPulse is a client-only SPA with no RSC, SSR, actions, or route actions;
  this accepted residual remains under dependency review.
- FastAPI's synchronous test client emits an upstream future-`httpx2` warning.
- A local pytest cache warning reflects denied cache writes, not test failure.
- Authentication, tenancy, rate limiting, durable workers/audit logs, and
  real-athlete governance remain outside the portfolio MVP.
- No external deployment was performed or claimed.

## Resume protocol

This is the final planned development phase. If release tags or push are
missing, read `AGENTS.md`, this file, `IMPLEMENTATION_PLAN.md`, `COMMIT_LOG.md`,
and `DAY_5_REPORT.md`; verify clean `main`, rerun `scripts/verify_release.py`,
and inspect local tags. Do not push, deploy, publish a release, or enable
uploads without explicit owner authorization.
