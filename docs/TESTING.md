# Testing and quality guide

Run all commands from the repository root.

## Backend

```powershell
uv run --project backend ruff format --check backend scripts
uv run --project backend ruff check backend scripts
uv run --project backend mypy --config-file backend/pyproject.toml backend/app backend/tests scripts
uv run --project backend pytest
uv run --project backend pytest --cov=app --cov-report=term-missing
```

The suite covers canonical schemas, adapters, cleaning, movement/event
analytics, data quality, Parquet, persistence, migrations, APIs, baselines,
risk, anomaly fallback, upload attacks, settings, safe errors, and the complete
synthetic API flow.

## Frontend

```powershell
npm.cmd --prefix frontend run format:check
npm.cmd --prefix frontend run lint
npm.cmd --prefix frontend run typecheck
npm.cmd --prefix frontend test -- --run
npm.cmd --prefix frontend run build
```

Component tests cover routing, charts, risk presentation, formatting, error
boundaries, API retry/error behavior, and loading/failure states.

## Browser journey and accessibility

Install the browser once:

```powershell
npx.cmd --prefix frontend playwright install chromium
```

Then run:

```powershell
npm.cmd --prefix frontend run test:e2e
```

Playwright starts a migrated SQLite API and Vite automatically. It runs the
demo-to-player journey in desktop Chrome and a Pixel 7 viewport, checks keyboard
navigation, and fails on serious/critical Axe violations. Failure traces and
screenshots are ignored locally and uploaded by CI.

## Database and containers

```powershell
uv run --project backend alembic -c backend/alembic.ini upgrade head
uv run --project backend alembic -c backend/alembic.ini downgrade base
uv run --project backend alembic -c backend/alembic.ini upgrade head
docker compose config --quiet
docker compose up --build
```

CI repeats the migration cycle on PostgreSQL 17. Local Compose runtime checks
require a running Docker Desktop engine.

## Release controls

```powershell
uv run --project backend python scripts/check_dataset_files.py
uv run --project backend python scripts/check_secrets.py
uv run --project backend python scripts/verify_release.py
uvx pip-audit --path backend\.venv\Lib\site-packages
npm.cmd --prefix frontend audit --omit=dev --audit-level=critical
```

`npm audit` currently also reports the published React Router RSC-mode advisory
at high severity. PlayerPulse is a client-only SPA and does not use RSC, server
actions, route actions, or server-side rendering; the issue is documented as a
scoped accepted residual until an upstream non-vulnerable compatible release is
published. Critical production advisories remain release-blocking.

## Framework warning

FastAPI's synchronous test client emits a framework-owned warning about future
`httpx2` migration. It is not hidden. Tests must still exit successfully, and
the framework compatibility should be rechecked during dependency updates.
