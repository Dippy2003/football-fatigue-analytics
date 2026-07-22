# PlayerPulse Day 3 report

## 1. Day completed

Day 3 is complete. The goal was to persist processed football summaries and
serve matches, players, quality, baselines, explainable performance-risk
indicators, and optional anomaly metadata through a documented API.

## 2. What was built

### Frontend

The existing application shell remains buildable and tested. No dashboard data
was falsely wired into placeholder pages; complete API integration is the next
frontend phase.

### Backend

The API can idempotently create the deterministic fictional demo, list source
rights, validate a disabled-by-default multipart import contract, queue match
processing, inspect jobs, and query matches, teams, players, metrics, timelines,
heatmaps, events, baselines, risk, and comparisons. Errors include a safe code,
message, details, request ID, and UTC timestamp.

### Data science and analytics

Personal, team/position, and match-only baselines have explicit minimum samples
and confidence. `rule-risk-v1` applies documented piecewise thresholds, requires
three physical factors and 60% coverage, refuses quality below 0.50, renormalizes
only available weights, and returns every contribution and limitation. Score is
separate from data/model confidence.

The Isolation Forest pipeline uses scaling, a fixed seed, exact feature schema,
training digest, versions, timestamp, and stability summary. It refuses fewer
than 50 valid rows. Tests train on 200 deterministic fictional feature records;
no user model is loaded and no binary artifact is committed.

### Database

Six reversible Alembic revisions create dataset imports, teams, anonymized
players, matches, typed player-match metrics, explainable assessments, and
processing jobs. UUID keys, UTC timestamps, provider identity constraints,
foreign keys, useful indexes, status/score/progress checks, and idempotent
creation are implemented for SQLite and PostgreSQL-compatible SQLAlchemy.

### Testing

Tests cover clean migrations, relationships, repositories, demo idempotency,
API routes, upload attacks/limits, bounded heatmaps/timelines, standard errors,
OpenAPI, baseline fallback, risk threshold sensitivity and scenarios, anomaly
fallback/reproducibility, jobs, and the live synthetic flow.

### Documentation

The API guide now lists implemented routes and the upload/error contracts. The
model card documents intended use, formulas, confidence, validation evidence,
alternative explanations, anomaly limitations, and non-medical boundaries.

### DevOps and infrastructure

`python-multipart` is locked for explicit form validation. Existing CI,
Dockerfiles, Compose, frontend production build, prohibited-data checks, and
dependency lock workflows remain valid.

## 3. Important files created or changed

- `backend/app/db/models/`: seven typed domain models.
- `backend/alembic/versions/0001...0006`: reversible schema history.
- `backend/app/repositories/`: dataset, identity, match, analytics, and job access.
- `backend/app/services/demo.py`: idempotent synthetic persistence.
- `backend/app/services/processing.py`: persisted in-process orchestration.
- `backend/app/analytics/baselines.py`: baseline fallback and confidence.
- `backend/app/analytics/risk.py`: deterministic score, confidence, factors, disclaimer.
- `backend/app/analytics/anomaly.py`: gated Isolation Forest and metadata.
- `backend/app/api/routes/`: dataset, job, match, player, risk, and comparison routes.
- `backend/app/api/errors.py`: standard error/request-ID handling.
- `backend/tests/`: database, integration, API, security, and scenario coverage.
- `docs/API.md` and `docs/MODEL_CARD.md`: implemented contracts and limitations.

## 4. How the system currently works

```text
POST /api/v1/datasets/demo
-> fixed-seed synthetic pipeline
-> idempotent dataset/team/player/match repositories
-> stored player-match metrics
-> API match/player exploration
-> baseline + rule-risk calculation
-> stored full explanation
-> bounded JSON response with disclaimer
```

```text
POST /api/v1/matches/{id}/process
-> persisted queued job
-> in-process analytics task
-> progress/status update
-> GET /api/v1/jobs/{id}
```

## 5. How I can check the work

Use Windows PowerShell from:

```powershell
Set-Location 'C:\Users\DIPNA\Pictures\PlayerPulse'
$env:UV_CACHE_DIR="$PWD\.uv-cache"
$env:UV_PYTHON_INSTALL_DIR="$PWD\.uv-python"
uv sync --project backend --all-groups
npm.cmd --prefix frontend ci
```

1. Create a clean local database and migrate it:

   ```powershell
   $env:DATABASE_URL="sqlite:///$($PWD.Path.Replace('\','/'))/backend/manual-check.db"
   uv run --project backend alembic -c backend/alembic.ini upgrade head
   uv run --project backend alembic -c backend/alembic.ini current
   ```

   Expect each revision `0001` through `0006` and current
   `0006_processing_jobs (head)`.

2. Start the backend:

   ```powershell
   uv run --project backend uvicorn app.main:app --reload
   ```

   Expect `Uvicorn running on http://127.0.0.1:8000`. Open
   `http://127.0.0.1:8000/docs`; Swagger UI should list datasets, processing,
   matches, players, analytics, risk/comparison, and system sections.

3. In a second root PowerShell terminal, create the demo:

   ```powershell
   $demo = Invoke-RestMethod -Method Post http://127.0.0.1:8000/api/v1/datasets/demo
   $demo | ConvertTo-Json
   $matchId = $demo.match_id
   $players = Invoke-RestMethod "http://127.0.0.1:8000/api/v1/matches/$matchId/players"
   $players.Count
   ```

   Expect `is_synthetic: true`, `created: true` on the first clean run, one
   match ID, and 20 players. Repeat the POST; expect `created: false`.

4. Check match and quality routes:

   ```powershell
   Invoke-RestMethod http://127.0.0.1:8000/api/v1/matches
   Invoke-RestMethod "http://127.0.0.1:8000/api/v1/matches/$matchId/team-summary"
   Invoke-RestMethod "http://127.0.0.1:8000/api/v1/matches/$matchId/quality"
   ```

   Expect one match, two team summaries, 20 covered player metrics, and quality
   score `1.0`.

5. Check player analytics and risk:

   ```powershell
   $playerId = $players[0].id
   Invoke-RestMethod "http://127.0.0.1:8000/api/v1/players/$playerId"
   Invoke-RestMethod "http://127.0.0.1:8000/api/v1/matches/$matchId/players/$playerId/metrics"
   Invoke-RestMethod "http://127.0.0.1:8000/api/v1/matches/$matchId/players/$playerId/timeline"
   Invoke-RestMethod "http://127.0.0.1:8000/api/v1/matches/$matchId/players/$playerId/heatmap"
   Invoke-RestMethod "http://127.0.0.1:8000/api/v1/matches/$matchId/players/$playerId/risk"
   ```

   Expect a profile, `features-v1`, a downsampled timeline, an 8×12 grid, and a
   risk object containing status, score/category when available, confidence,
   factors, explanation, model `rule-risk-v1`, limitations, and disclaimer.

6. Check processing jobs:

   ```powershell
   $job = Invoke-RestMethod -Method Post "http://127.0.0.1:8000/api/v1/matches/$matchId/process"
   Invoke-RestMethod "http://127.0.0.1:8000/api/v1/jobs/$($job.job_id)"
   ```

   Expect status `complete`, progress `1.0`, and the restart/retry limitation.

7. Confirm uploads are disabled:

   ```powershell
   Invoke-WebRequest -Method Post http://127.0.0.1:8000/api/v1/datasets/upload
   ```

   A request without the multipart fields returns validation error; a valid
   multipart request returns 403 while `ENABLE_UPLOADS=false`. Automated tests
   below check both enabled-local validation and all limits without real data.

8. Run all backend checks:

   ```powershell
   uv run --project backend ruff format --check .
   uv run --project backend ruff check .
   uv run --project backend mypy app tests
   uv run --project backend pytest --cov=app
   ```

   Expect 123 or more passing tests, no lint/type errors, and about 96% coverage.

9. Run focused checks:

   ```powershell
   uv run --project backend pytest backend/tests/integration/test_migrations.py -q
   uv run --project backend pytest backend/tests/api -q
   uv run --project backend pytest backend/tests/unit/test_baselines.py backend/tests/unit/test_risk_scoring.py backend/tests/unit/test_risk_scenarios.py backend/tests/unit/test_anomaly_pipeline.py -q
   ```

   Expect all commands to pass. One upstream Starlette TestClient deprecation
   warning is currently visible.

10. Check frontend and infrastructure:

    ```powershell
    npm.cmd --prefix frontend run format:check
    npm.cmd --prefix frontend run lint
    npm.cmd --prefix frontend run typecheck
    npm.cmd --prefix frontend test -- --run
    npm.cmd --prefix frontend run build
    uv run --project backend python scripts/check_dataset_files.py
    docker compose config
    ```

    Expect all to succeed. Start the unchanged frontend with
    `npm.cmd --prefix frontend run dev`, open `http://localhost:5173`, and stop
    both servers with `Ctrl+C` in their terminals.

11. Check Git:

    ```powershell
    git status
    git rev-list --count day-2-complete..day-3-complete
    git log --oneline --decorate -n 35
    ```

    Expect a clean `main`, at least 30 commits, and the annotated checkpoint tag.

## 6. Verification checklist

```text
[ ] Six migrations upgrade on a clean database
[ ] Migrations downgrade to base
[ ] Demo POST creates one synthetic match and 20 players
[ ] Repeating demo POST is idempotent
[ ] Match, team, quality, player, metrics, timeline and heatmap routes work
[ ] Baseline route reports type, confidence and limitation
[ ] Risk route includes status, confidence, factors, version and disclaimer
[ ] Stable/severe/insufficient risk scenarios pass
[ ] Isolation Forest refuses fewer than 50 rows
[ ] Processing job reaches complete and exposes retry limitation
[ ] Uploads are disabled by default
[ ] Invalid manifests, filenames, ZIP/pickle and oversized uploads are rejected
[ ] Swagger UI opens at /docs
[ ] Backend tests, Ruff and mypy pass
[ ] Frontend checks and production build pass
[ ] Dataset policy and Compose validation pass
[ ] No secrets, raw provider data, database or model binary is committed
[ ] Required tag exists and working tree is clean
```

## 7. Tests and checks performed

Passed:

- Backend Ruff format: 114 files formatted.
- Backend Ruff lint: all checks passed.
- mypy: 113 source files, no issues.
- pytest with coverage: 123 passed, 96% total coverage, one upstream warning.
- Clean Alembic upgrade: `0001` through `0006`; current head confirmed.
- Clean Alembic downgrade: all six revisions returned to base.
- Live HTTP: demo created, 1 match, 20 players, available `rule-risk-v1`, docs 200.
- Frontend Prettier, ESLint, TypeScript, Vitest, and production Vite build passed;
  1 test and 95 transformed modules.
- Dataset-file policy passed with no prohibited tracked data.
- `docker compose config --quiet` passed.

Failed and fixed:

- In-memory SQLite initially used separate request-thread connections, hiding
  created tables. `StaticPool` now shares the test database and has a regression test.
- The first live `/docs` PowerShell check used the legacy IE parser and failed;
  rerunning with `-UseBasicParsing` returned HTTP 200. The server was healthy.
- Strict mypy identified untyped scikit-learn imports; a narrow `sklearn.*`
  missing-stub override was added without weakening application typing.
- Synthetic sprint detection was seed-sensitive; amplitude and parameterized
  seed tests now guarantee plausible bouts below 12.5 m/s.

Skipped:

- Real provider upload/import: intentionally skipped; no user-supplied licensed
  local dataset was provided or needed.
- Binary anomaly artifact save/load: intentionally skipped; only trusted build
  artifacts may be loaded and no artifact is required for the API fallback.
- Full Docker stack startup: skipped; Compose syntax passed and full runtime is
  reserved for release hardening.
- Interactive data dashboard: not implemented until the next frontend phase.

## 8. Git summary

- Substantive commits before report/ledger commits: 34.
- Starting commit: `31b7c14` (`day-2-complete`).
- Latest implementation/handoff commit before this report: `6a29178`.
- Ending checkpoint: required annotated tag on `main`.
- Branch: `main`; no phase-named branch was created.
- Working tree: clean after report, ledger, tag, and authorized push.
- Categories: schema/migrations; repositories/services; APIs/security/errors;
  baselines/risk/anomaly; tests; documentation.

Run the exact live commands for authoritative output:

```powershell
git status
git log --oneline --decorate -n 35
```

The chat report records the final tag target and commit count after the report
and generated ledger are committed.

## 9. Screenshots to capture

1. `/docs` with dataset, match, player, processing, and risk sections visible.
   Filename: `api-swagger.png`. Caption: “Versioned PlayerPulse analytics API.”
2. PowerShell showing the live demo JSON and `$players.Count` equal to 20.
   Filename: `stored-demo.png`. Caption: “Idempotent fictional match persistence.”
3. A formatted risk JSON showing category, confidence, top factors, version,
   and disclaimer. Filename: `risk-explanation.png`. Caption: “Transparent
   non-medical performance-risk indicator.”
4. Test terminal showing 123 passed and 96% coverage. Filename:
   `backend-quality-gate.png`. Caption: “Persistence/API/risk verification.”
5. Migration terminal showing `0006_processing_jobs (head)`. Filename:
   `migration-head.png`. Caption: “Reversible relational schema at current head.”
6. Git log with the checkpoint tag and professional feature commits. Filename:
   `git-history.png`. Caption: “Auditable atomic implementation history.”

## 10. Known limitations

- In-process jobs can require retry after restart.
- The synthetic database contains one match and therefore uses match-only
  baseline confidence until more fictional history is stored.
- External uploads are disabled by default and were not tested with provider data.
- Raw tracking is regenerated for timelines/heatmaps rather than stored in SQL.
- The anomaly signal has no labelled fatigue ground truth and reports no accuracy.
- The frontend is not connected to these routes yet.
- Full Docker stack startup was not performed.
- One upstream Starlette/httpx deprecation warning remains.

## 11. Problems found and fixed

Key fixes were shared in-memory SQLite pooling, stable empty sprint schemas,
cross-seed plausible sprint profiles, portable strict typing for third-party ML,
bounded request errors, path/archive/model upload rejection, and correct
PowerShell docs verification.

## 12. Next development day

The next phase connects these verified APIs to the responsive dashboard, match
explorer, player analysis, heatmap, workload/speed charts, risk explanation,
comparison, quality, methodology, ethics, and data-management pages. It will add
loading/empty/error states, keyboard navigation, responsive layouts, and light/
dark modes. No frontend dashboard work has started.

## 13. Resume instruction

`Continue with the frontend dashboard phase; first read AGENTS.md, docs/PROGRESS.md, docs/IMPLEMENTATION_PLAN.md, docs/COMMIT_LOG.md, and docs/DAY_3_REPORT.md, then verify clean main and the latest checkpoint tag.`
