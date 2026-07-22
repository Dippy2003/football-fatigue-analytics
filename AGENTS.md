# PlayerPulse repository instructions

## Purpose and boundaries

PlayerPulse analyses football match data for workload, movement,
fatigue-indicator, and explainable performance-risk decision support. It never
diagnoses fatigue, predicts confirmed injury, recommends treatment, or replaces
qualified medical or sports-science assessment. Use neutral terms such as
`fatigue indicator`, `performance-risk score`, `workload warning`, and
`recovery review recommended`.

Every visible risk result must include this disclaimer:

> PlayerPulse provides performance-based indicators from available match data.
> It is not a medical diagnostic tool and must not be used as a substitute for
> qualified medical or sports-science assessment.

## Repository map

- `backend/`: FastAPI, settings, database, analytics, services, migrations, tests.
- `frontend/`: React, TypeScript, Vite, Tailwind, UI features, tests.
- `data/`: source registry and ignored raw/interim/processed workspaces.
- `models/`: documentation and ignored trusted build artifacts.
- `docs/`: architecture, methodology, decisions, progress, testing, and guides.
- `scripts/`: rights, release, and Git-history verification helpers.
- `.github/`: CI and collaboration templates.

## Standard commands

Run commands from the repository root unless a section says otherwise.

```powershell
# Full setup
uv sync --project backend --all-groups
npm.cmd --prefix frontend ci

# Development (separate terminals)
uv run --project backend uvicorn app.main:app --reload
npm.cmd --prefix frontend run dev

# Quality
uv run --project backend ruff format --check .
uv run --project backend ruff check .
uv run --project backend mypy app tests
uv run --project backend pytest
npm.cmd --prefix frontend run format:check
npm.cmd --prefix frontend run lint
npm.cmd --prefix frontend run typecheck
npm.cmd --prefix frontend test -- --run
npm.cmd --prefix frontend run build

# Database
uv run --project backend alembic -c backend/alembic.ini upgrade head
uv run --project backend alembic -c backend/alembic.ini downgrade -1

# Containers
docker compose config
docker compose up --build
docker compose down
```

On macOS/Linux use `npm` instead of `npm.cmd`. Root `Makefile` targets mirror
these commands where GNU Make is available.

## Dataset handling

- Synthetic demo data is deterministic, fictional, visibly marked
  `is_synthetic=true`, and is the only default for tests, CI, screenshots, and
  the public demo.
- Never commit or redistribute third-party raw football data unless the current
  licence explicitly allows the exact use.
- Metrica Sports sample files are local-import-only by default. StatsBomb Open
  Data is rights-gated and must retain current official attribution.
- Keep local files under ignored `data/raw/`, `data/interim/`, and
  `data/processed/`; store provenance and checksums for imports.
- Never imply PlayerPulse owns external data or protected marks. Do not bundle
  provider logos, club badges, player photos, or competition marks without
  verified permission.
- Re-check official source terms before enabling an adapter or making a release.

## Security rules

- Never commit secrets, `.env`, local databases, caches, large generated data,
  untrusted model files, or raw external datasets.
- Never load a user-uploaded Joblib or pickle model. Repository training output
  is the only trusted source of model artifacts.
- Production uploads remain disabled unless explicitly configured.
- Preserve user changes. Do not delete or overwrite unrelated work.
- Do not push, force-push, create remotes, open pull requests, publish releases,
  or deploy externally without explicit user authorization.

## Change discipline

- Use npm and commit `package-lock.json`; use uv and commit `uv.lock`.
- Never manually edit generated lockfiles.
- Update tests whenever behavior changes.
- Update documentation when APIs, schemas, architecture, setup, security, data
  rights, or methodology changes.
- Before a commit, inspect status and diff, check for secrets/prohibited data,
  run the smallest relevant check, and stage only coherent files.
- Before a phase ends, run format, lint, types, tests, builds, Docker Compose
  validation, rights checks, and relevant migrations/pipelines.
- Use Conventional Commits such as `feat(backend):`, `feat(frontend):`, `test:`,
  `docs:`, `build:`, `ci:`, `security:`, `fix:`, and `chore:`.

## Progress persistence

Continuously maintain `docs/PROGRESS.md`, `docs/DECISIONS.md`,
`docs/IMPLEMENTATION_PLAN.md`, and `docs/COMMIT_LOG.md`. Record the current day,
task, validation, blockers, and next exact action in progress notes.

Generate `docs/COMMIT_LOG.md` from real Git history at each checkpoint with
`scripts/export_commit_log.py`; never try to put a commit's own hash inside that
same commit. At least 30 substantive atomic commits and an annotated checkpoint
tag are required per development day.

## Current handoff

Persistence/API/risk implementation and its full quality gate are complete on
`main`. Continue without phase-named branches or completion-style commit
messages. Only checkpoint documentation, ledger generation, the required tag,
and the already-authorized push remain. Do not begin frontend dashboard work
until the user explicitly authorizes the next development phase.
