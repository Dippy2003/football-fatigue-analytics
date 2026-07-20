# PlayerPulse Day 1 report

## 1. Day completed

Day 1 is complete. Its goal was to create a reproducible, secure foundation
with a runnable FastAPI system API, a runnable React application shell,
SQLite/PostgreSQL configuration, tests, containers, CI, rights controls, and
continuation documentation. No Day 2 analytics work has started.

## 2. What was built

### Frontend

The React/TypeScript application opens as a professional PlayerPulse shell with
an original pitch/pulse mark, responsive navigation, keyboard skip link,
visible non-medical disclaimer, and a clear foundation-status panel. React
Router provides working Home, Dashboard, Matches, match, player, comparison,
Data, Methodology, About, and not-found routes. Pages that depend on future data
are honestly labelled placeholders rather than showing invented metrics.

TanStack Query and a small typed Axios layer are ready to call the versioned API.
Tailwind design tokens, focus styles, semantic headings, ESLint, Prettier,
TypeScript checks, Vitest, and Testing Library provide the UI foundation.

### Backend

FastAPI exposes live `/api/v1/health`, `/api/v1/readiness`, and
`/api/v1/version` endpoints plus OpenAPI, Swagger UI, and ReDoc. Typed Pydantic
Settings validate the environment, keep uploads disabled by default, constrain
resource limits, and restrict CORS to an explicit allowlist. Structured JSON
logging redacts credential-shaped fields. The application factory supports
isolated tests and configuration.

### Data science and analytics

No football analytics were implemented because they belong to Day 2. The
foundation does define the deterministic seed, synthetic-public-demo rule,
ignored processing workspaces, and a rights gate so later analytics cannot
silently depend on unlicensed data.

### Database

SQLAlchemy supports a zero-configuration SQLite fallback and normalized psycopg
PostgreSQL URLs. Request-scoped session infrastructure, UUID primary keys,
timezone-aware UTC Python defaults, naming conventions, and an Alembic migration
environment are working. A disposable SQLite database successfully completed
the Alembic `upgrade head` and `current` checks.

### Testing

Ten backend tests cover system endpoints, OpenAPI, safe settings, log redaction,
SQLite connectivity, PostgreSQL URL selection, UUIDs, and UTC defaults. One
frontend interaction test renders the shell, confirms the disclaimer, and
navigates to Dashboard without reloading. Ruff, strict mypy, Prettier, ESLint,
TypeScript, and the production Vite build all pass.

### Documentation

The repository now explains setup, environment variables, architecture, API,
testing, deployment preparation, security, threat boundaries, dataset rights,
licence separation, contributor rules, decisions, progress, and the five-day
plan. Metrica Sports and StatsBomb records include official URLs, checked
commits, access date, status, and terms-file SHA-256 evidence.

### DevOps and infrastructure

uv locks Python 3.12 dependencies and npm locks frontend dependencies.
Dockerfiles define the backend and frontend images; Compose defines PostgreSQL,
the API, migrations-before-start, health checks, and the web app. GitHub Actions
defines backend, frontend, and Compose quality jobs. A PowerShell quality script
and Makefile provide repeatable commands. Compose syntax was validated, but
container builds could not run because Docker Desktop's engine was not running.

## 3. Important files created or changed

- `AGENTS.md`: ethical, security, data, testing, Git, and continuation rules.
- `README.md`: current feature scope and Windows/Docker quick start.
- `backend/app/main.py`: FastAPI application factory and middleware assembly.
- `backend/app/api/routes/system.py`: typed health, readiness, and version routes.
- `backend/app/core/config.py`: validated environment settings and safe defaults.
- `backend/app/core/logging.py`: structured output and sensitive-field redaction.
- `backend/app/db/session.py`: SQLite/PostgreSQL engine and session lifecycle.
- `backend/app/db/base.py`: UUID, UTC, metadata, and naming conventions.
- `backend/alembic/`: database migration environment.
- `backend/pyproject.toml` and `backend/uv.lock`: Python project and resolved lock.
- `frontend/src/app/router.tsx`: required route map.
- `frontend/src/components/layout/AppShell.tsx`: responsive accessible shell.
- `frontend/src/services/api/`: typed Axios system client.
- `frontend/package.json` and `frontend/package-lock.json`: npm project and lock.
- `docker-compose.yml`: PostgreSQL, backend, and frontend development stack.
- `.github/workflows/ci.yml`: initial automated quality workflow.
- `data/sources.yml`: machine-readable source-rights evidence.
- `docs/DATASET_ATTRIBUTION.md`: human-readable rights and attribution record.
- `scripts/check_day1.ps1`: complete Windows quality gate.
- `scripts/check_dataset_files.py`: prohibited tracked-data check.
- `scripts/export_commit_log.py`: ledger generation from real Git history.
- `docs/PROGRESS.md`: exact safe continuation state.

## 4. How the system currently works

System API flow:

```text
Browser or API client
→ GET /api/v1/health, /readiness, or /version
→ FastAPI route
→ typed Pydantic response
→ JSON result
```

Frontend flow:

```text
User opens http://127.0.0.1:5173
→ Vite serves the React application
→ React Router selects the page
→ AppShell renders navigation, content, and disclaimer
→ navigation changes the client route without a full reload
```

The typed Axios/TanStack Query layer exists but placeholder pages do not yet
call match APIs. The backend does not query the database for system endpoints.
SQLite and PostgreSQL behavior is currently verified through database tests and
Alembic, not through unimplemented match endpoints.

## 5. How I can check the work

All commands below start from:

```text
C:\Users\DIPNA\Pictures\PlayerPulse
```

### A. Inspect the repository

1. Open PowerShell.
2. Run:

   ```powershell
   Set-Location 'C:\Users\DIPNA\Pictures\PlayerPulse'
   Get-ChildItem -Force
   Get-ChildItem backend,frontend,docs,data,scripts
   ```

3. Expect root files such as `README.md`, `AGENTS.md`, `docker-compose.yml`,
   `backend`, `frontend`, `data`, `docs`, and `scripts`.

### B. Install dependencies

1. From the repository root, run:

   ```powershell
   uv sync --project backend --all-groups
   npm.cmd --prefix frontend ci
   ```

2. Expect uv to select Python 3.12 and report resolved/installed packages.
3. Expect npm to finish with an audit summary. Do not edit either lockfile.

### C. Start and inspect the backend

1. From the repository root, run:

   ```powershell
   uv run --project backend uvicorn app.main:app --app-dir backend --reload
   ```

2. Expect a line containing `Uvicorn running on http://127.0.0.1:8000`.
3. Open these browser URLs:

   - http://127.0.0.1:8000/api/v1/health — expect `{"status":"ok"}`.
   - http://127.0.0.1:8000/api/v1/readiness — expect `status` to be `ready`.
   - http://127.0.0.1:8000/api/v1/version — expect version `0.1.0`.
   - http://127.0.0.1:8000/docs — expect Swagger UI with three system routes.

4. Return to the terminal and press `Ctrl+C` to stop the backend.

### D. Start and inspect the frontend

1. In a new PowerShell window, run:

   ```powershell
   Set-Location 'C:\Users\DIPNA\Pictures\PlayerPulse'
   npm.cmd --prefix frontend run dev
   ```

2. Expect `Local: http://127.0.0.1:5173/`.
3. Open http://127.0.0.1:5173.
4. Expect the PlayerPulse mark, “See workload and performance changes in
   context.” heading, foundation panel, navigation, and disclaimer.
5. Click Dashboard, Matches, Data, Methodology, and About. Each URL and page
   heading should change without a full page reload.
6. Open http://127.0.0.1:5173/not-a-page and expect the accessible 404 page.
7. Return to the terminal and press `Ctrl+C`.

### E. Check database configuration and migrations

1. Read safe settings:

   ```powershell
   Get-Content .env.example
   ```

2. To use local SQLite defaults, no `.env` is required.
3. Test the database layer:

   ```powershell
   Push-Location backend
   uv run pytest tests/unit/test_database.py tests/unit/test_database_base.py
   Pop-Location
   ```

4. Expect `3 passed`.
5. Run current migrations against the ignored local SQLite database:

   ```powershell
   uv run --project backend alembic -c backend/alembic.ini upgrade head
   uv run --project backend alembic -c backend/alembic.ini current
   ```

6. These commands should exit without an Alembic error. The generated
   `playerpulse.db` is ignored and may be removed after checking.

### F. Run all Day 1 checks

1. From the repository root, run:

   ```powershell
   powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/check_day1.ps1
   ```

2. Expect sections for backend and frontend checks, then:

   ```text
   PlayerPulse dataset-file check passed: no prohibited tracked data found.
   Day 1 quality checks passed.
   ```

### G. Check Docker configuration

1. Start Docker Desktop and wait until its engine says it is running.
2. From the repository root, run:

   ```powershell
   docker compose config
   ```

3. Expect services named `database`, `backend`, and `frontend` with no error.
4. Optional runtime check (not executed during this session):

   ```powershell
   docker compose up --build
   ```

5. When healthy, open frontend http://127.0.0.1:5173 and backend health
   http://127.0.0.1:8000/api/v1/health.
6. Stop and remove the containers with:

   ```powershell
   docker compose down
   ```

### H. Check Git history and tag

```powershell
git status
git log --oneline --decorate -n 35
git tag -n
git rev-list --count day-1-complete
```

Expect branch `main`, a clean working tree, at least 30 commits, and annotated
tag `day-1-complete`. No phase-named branch is created.

## 6. Verification checklist

- [ ] Repository contains backend, frontend, docs, data, models, and scripts.
- [ ] Backend starts without errors.
- [ ] Health returns `status: ok`.
- [ ] Readiness returns `status: ready`.
- [ ] Version returns `0.1.0`.
- [ ] `/docs` lists the three system endpoints.
- [ ] Frontend opens with the PlayerPulse shell and disclaimer.
- [ ] Navigation and the 404 route work.
- [ ] Backend tests report 10 passed.
- [ ] Frontend tests report 1 passed.
- [ ] Ruff, mypy, Prettier, ESLint, and TypeScript pass.
- [ ] Frontend production build succeeds.
- [ ] SQLite tests and Alembic complete.
- [ ] `docker compose config` succeeds.
- [ ] Data-file policy finds no prohibited tracked data.
- [ ] `.env` and local database files are not tracked.
- [ ] Branch is `main`; no phase branch exists.
- [ ] At least 30 commits and `day-1-complete` exist.

## 7. Tests and checks performed

### Passed

- `powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/check_day1.ps1`
  - Ruff format: 18 backend files already formatted.
  - Ruff lint: all checks passed.
  - mypy: no issues in 17 source files.
  - pytest: 10 passed in 0.56 seconds; one visible upstream deprecation warning.
  - Prettier: all matched files use Prettier style.
  - ESLint: zero warnings/errors.
  - TypeScript: project type check passed.
  - Vitest: 1 file and 1 interaction test passed.
  - Vite production build: 95 modules transformed; completed successfully.
  - prohibited-data check: passed.
  - `docker compose config --quiet`: passed.
- Alembic `upgrade head` and `current` ran successfully against a disposable
  SQLite database, which was removed afterward.
- A live Uvicorn process returned the expected health, readiness, and version
  JSON; it was then stopped and temporary logs removed.
- A live Vite process returned HTTP 200 with the correct PlayerPulse document
  title; it was then stopped and temporary logs removed.
- The GitHub Actions YAML was parsed and its backend/frontend/Compose jobs were
  confirmed.
- `data/sources.yml` was parsed and its three registry records confirmed.

### Failed and fixed

- Initial pytest collection failed because the console runner lacked the backend
  source path. Adding explicit pytest `pythonpath` fixed it; 10 tests now pass.
- Initial settings static checks found import ordering and a typed constructor
  mismatch. Both were corrected; Ruff and mypy pass.
- Structured logging initially returned an inferred `Any`; an explicit safe
  cast fixed strict mypy.
- Ruff identified Python 3.12's `UTC` alias, Alembic import ordering, and long
  ledger-script lines; all were corrected.
- ESLint rejected a router/component hot-reload mix; the route element was
  restructured and the zero-warning gate now passes.

### Skipped or unavailable

- `docker compose up --build`: skipped because Docker Desktop's Linux engine was
  not running. Docker CLI and Compose were installed and configuration parsed.
- Interactive rendered-browser inspection and automated screenshots: unavailable
  because this session exposed no supported browser backend. The Vite HTTP
  runtime, jsdom render/navigation test, type checks, and production build passed.
- GitHub-hosted CI execution: not claimed in this report; workflow configuration
  was checked locally and is triggered after the authorized push.
- PostgreSQL runtime integration: scheduled for the later persistence/CI phase;
  PostgreSQL configuration and URL handling are implemented and unit-tested.

## 8. Git summary

- Meaningful Day 1 commits: **at least 38 at checkpoint finalization**.
- Starting commit: `d9c92b2` (`chore: initialize PlayerPulse repository`).
- Ending checkpoint: annotated tag `day-1-complete` on `main`.
- Latest hash: resolve with `git rev-list -n 1 day-1-complete`; the exact resolved
  value is supplied in the accompanying Codex chat because a committed report
  cannot contain its own not-yet-known commit hash.
- Daily tag: `day-1-complete`.
- Current branch: `main` (no Day 1 branch).
- Working tree at handoff: clean after final ledger/report commit.
- Authorized remote: `https://github.com/Dippy2003/football-fatigue-analytics.git`.

Commit categories include repository governance and rights; backend application,
configuration, database, migrations, and tests; frontend environment, styling,
routing, API foundation, and tests; containers and Compose; CI and safety tools;
and setup, architecture, security, testing, deployment, progress, and report
documentation.

Useful commands executed at the final checkpoint:

```powershell
git status
git log --oneline --decorate -n 35
```

Their exact final output is included in the accompanying chat after the tag and
push, avoiding fabricated hashes or pre-tag state in this committed file.

## 9. Screenshots to capture

1. Landing page
   - Open: http://127.0.0.1:5173
   - Show: full header, PlayerPulse mark, main heading, foundation panel, and disclaimer.
   - Filename: `day-1-playerpulse-landing.png`
   - Caption: “PlayerPulse Day 1 responsive application shell and ethical scope.”
2. Dashboard route
   - Open: http://127.0.0.1:5173/dashboard
   - Show: active Dashboard navigation, Dashboard heading, and honest placeholder state.
   - Filename: `day-1-dashboard-route.png`
   - Caption: “Working client-side navigation prepared for later analytics data.”
3. System APIs
   - Open: http://127.0.0.1:8000/docs
   - Show: Swagger UI with health, readiness, and version routes.
   - Filename: `day-1-fastapi-docs.png`
   - Caption: “Versioned PlayerPulse operational API documented by OpenAPI.”
4. Quality terminal
   - Run the full PowerShell Day 1 check.
   - Show: the final backend/frontend/data/Compose success lines.
   - Filename: `day-1-quality-gates.png`
   - Caption: “PlayerPulse Day 1 automated quality gates passing.”
5. Git checkpoint
   - Run `git log --oneline --decorate -n 35`.
   - Show: `main`, `day-1-complete`, and the meaningful commit sequence.
   - Filename: `day-1-git-history.png`
   - Caption: “Atomic Day 1 development history and checkpoint tag.”

Only synthetic or no-data views should be used. Do not add provider logos or
third-party raw data to screenshots.

## 10. Known limitations

- The demo generator and football analytics pipeline begin in Day 2.
- No teams, players, matches, metrics, risk assessments, or jobs are persisted.
- No match/player/dashboard API exists beyond system endpoints.
- Frontend analytics pages are working routes with honest placeholders.
- Readiness does not yet query a domain database.
- Production uploads remain disabled; no importer exists yet.
- Docker runtime and PostgreSQL service startup were not tested locally.
- No supported interactive browser or screenshot capture was available.
- The synchronous FastAPI test client emits one upstream deprecation warning.
- The application is prepared for deployment but is not deployed.

## 11. Problems found and fixed

Git ownership protection initially blocked commits under the sandbox account;
only this exact workspace was added to Git's safe-directory list. uv initially
could not use its default cache and network access was restricted, so ignored
workspace-local provisioning and approved dependency downloads were used.
PowerShell blocked `npm.ps1`, so documented Windows commands use `npm.cmd`.

The quality process then found real source issues: backend test imports, strict
settings typing, structured logger typing, UTC idioms, Alembic import order,
router hot-reload boundaries, and ledger formatting. These were fixed in
separate meaningful commits and all relevant gates rerun successfully.

## 12. Next development day

Day 2 will build the rights-gated data and analytics pipeline: validate the
source registry, define canonical tracking/event schemas, generate the fixed-seed
fictional match, implement local-only Metrica and optional StatsBomb adapters,
validate manifests, normalize coordinates, clean/interpolate tracking, compute
distance/speed/acceleration/intensity/sprints/windows/event metrics and quality,
and write reproducible Parquet outputs. It must not start until explicitly
authorized.

## 13. Resume instruction

> Continue to Day 2. Resume PlayerPulse from `main`: read `AGENTS.md`, `docs/IMPLEMENTATION_PLAN.md`, `docs/PROGRESS.md`, `docs/COMMIT_LOG.md`, and `docs/DAY_1_REPORT.md`; verify `day-1-complete`, the clean working tree, and the smallest health checks; then begin Day 2 Task 1 without repeating Day 1 or redistributing third-party data.
