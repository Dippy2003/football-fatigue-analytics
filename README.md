# PlayerPulse

PlayerPulse is an explainable football workload and performance-risk review
application. It combines a FastAPI analytics API with a responsive React
interface, deterministic synthetic demo data, transparent quality/confidence
handling, and conservative dataset-rights controls.

> PlayerPulse provides performance-based indicators from available match data.
> It is not a medical diagnostic tool and must not be used as a substitute for
> qualified medical or sports-science assessment.

## What works

- One-click fictional demo generation and idempotent database persistence
- Rights-acknowledged local tracking CSV import into persisted dashboard
  analytics, with downloadable schemas and uploads disabled by default
- Provider-neutral Metrica/StatsBomb adapters with fail-closed rights gates
- Coordinate cleaning, interpolation, distance, speed, acceleration, intensity,
  sprints, 15-minute windows, event metrics, and quality reporting
- Teams, players, matches, workload metrics, baselines, heatmaps, and timelines
  through a versioned FastAPI API
- Explainable rule-based 0–100 indicators with confidence, factor
  contributions, limitations, and insufficient-data handling
- Dashboard, match explorer, player analysis, comparison, methodology, ethics,
  data management, responsive themes, and accessible async/error states
- SQLite development, PostgreSQL production support, Alembic migrations,
  hardened containers, CI, and desktop/mobile browser tests

The optional Isolation Forest produces a separate anomaly signal only. No score
is an injury probability or medical conclusion.

## Prerequisites

- Git
- uv with Python 3.12
- Node.js 22 and npm 10+
- Docker Desktop only for the container path

## Local quick start (Windows PowerShell)

From the repository root:

```powershell
uv sync --project backend --all-groups
npm.cmd --prefix frontend ci
uv run --project backend alembic -c backend/alembic.ini upgrade head
```

Start the API:

```powershell
uv run --project backend uvicorn app.main:app --app-dir backend --reload
```

In a second root terminal, start the browser app:

```powershell
npm.cmd --prefix frontend run dev
```

Open:

- Application: http://127.0.0.1:5173
- API documentation: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/api/v1/health
- Readiness: http://127.0.0.1:8000/api/v1/readiness
- Version: http://127.0.0.1:8000/api/v1/version

Select **Load demo match**, open the fictional match, and choose **Analyse** for
a player. Stop both servers with `Ctrl+C`.

For a rights-cleared tracking dataset, follow the
[local data import guide](docs/LOCAL_DATA_IMPORT.md). The workflow requires
`ENABLE_UPLOADS=true`, a Metrica-compatible long-form tracking CSV, and an
explicit rights acknowledgement.

## Quality gate

```powershell
uv run --project backend ruff format --check backend scripts
uv run --project backend ruff check backend scripts
uv run --project backend mypy --config-file backend/pyproject.toml backend/app backend/tests scripts
uv run --project backend pytest
npm.cmd --prefix frontend run format:check
npm.cmd --prefix frontend run lint
npm.cmd --prefix frontend run typecheck
npm.cmd --prefix frontend test -- --run
npm.cmd --prefix frontend run build
npm.cmd --prefix frontend run test:e2e
uv run --project backend python scripts/check_dataset_files.py
uv run --project backend python scripts/check_secrets.py
uv run --project backend python scripts/verify_release.py
docker compose config --quiet
```

## Containers

```powershell
docker compose up --build
```

Open http://127.0.0.1:5173. The stack runs PostgreSQL, migrations, the API, and
an unprivileged Nginx frontend. Stop it with:

```powershell
docker compose down
```

## Data and security boundary

Only project-owned synthetic data is used for public demos, CI, tests, and
screenshots. Raw/interim/processed provider files, local databases, secrets, and
generated models are ignored. Metrica input is local-only; StatsBomb input is
verification-gated. Current source terms and hashes are recorded in
`data/sources.yml` and `docs/DATASET_ATTRIBUTION.md`.

Uploads are disabled by default. When deliberately enabled, the local workflow
accepts bounded CSV files, deletes temporary raw uploads after processing, and
stores derived Parquet only in the ignored local data workspace. Production
CORS permits explicit HTTPS origins only. Never load user-supplied pickle or
Joblib files.

## Documentation

- [User guide](docs/USER_GUIDE.md)
- [Local data import](docs/LOCAL_DATA_IMPORT.md)
- [Architecture](docs/ARCHITECTURE.md)
- [API](docs/API.md)
- [Methodology](docs/METHODOLOGY.md)
- [Data dictionary](docs/DATA_DICTIONARY.md)
- [Synthetic data card](docs/DATA_CARD.md)
- [Model card](docs/MODEL_CARD.md)
- [Ethics and limitations](docs/ETHICS_AND_LIMITATIONS.md)
- [Deployment](docs/DEPLOYMENT.md)
- [Testing](docs/TESTING.md)
- [Security policy](SECURITY.md)

Original PlayerPulse code and documentation are MIT licensed. Third-party data
and marks remain governed by their owners' terms.
