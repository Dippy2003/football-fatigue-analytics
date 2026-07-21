# PlayerPulse Day 2 report

## 1. Day completed

Day 2 is complete. Its goal was to build a rights-aware football data layer and
a deterministic, explainable analytics pipeline without committing or
redistributing third-party raw data.

## 2. What was built

### Frontend

The Day 1 responsive application shell remains operational and production
buildable. Day 2 deliberately did not invent dashboard results before the API
and persistence work planned for Days 3 and 4.

### Backend

The backend now validates a versioned dataset-rights registry. The Metrica
tracking/event adapters read developer-supplied local long-form CSV only. The
StatsBomb event adapter reads local JSON only after an explicit current-rights
acknowledgement. Clear validation errors protect against absent files, missing
columns, unsafe coordinates, malformed event JSON, and incomplete schemas.

A command-line interface can generate the complete fictional demo pipeline and
write its outputs locally. No upload API was enabled.

### Data science and analytics

The deterministic demo contains two fictional teams, 20 rostered players, two
periods, 10 Hz tracking, substitutions, different workload/decline patterns, a
short cleanable dropout, and passes, pressures, tackles, interceptions, and
possession losses. Every row is marked synthetic.

Canonical tracking and event schemas use seconds and a 105 by 68 metre pitch.
Cleaning sorts timestamps, removes duplicates, interpolates only short gaps
within the same period, and preserves flags. Analytics calculate step/total
distance, active duration, distance per active minute, average/maximum speed,
acceleration, deceleration, plausible-speed flags, centered-median smoothing,
five intensity zones, sprint bouts, continuous 15-minute windows, pass
completion, defensive actions, and possession losses.

The quality report separates coordinate completeness, timestamp monotonicity,
and plausible-speed rate. It explains limitations and never treats data quality
as athlete health evidence.

### Database

Day 2 persists canonical and derived tables as PyArrow Parquet in ignored local
directories. Paths and table names are validated, and pickle input is rejected.
Relational domain persistence intentionally begins on Day 3. The existing
SQLite/PostgreSQL configuration remains valid.

### Testing

Provider adapter tests use tiny fictional fixtures—not provider data. Unit
tests cover rights gates, schemas, coordinate boundaries, determinism,
substitutions, cleaning, interpolation boundaries, formulas, intensity edges,
sprint duration, match windows, event metrics, quality scoring, manifests,
Parquet round trips, and the CLI. An integration test runs the synthetic match
from generation through cleaning, analytics, quality, and Parquet.

### Documentation

Dataset attribution was rechecked against official sources. Methodology now
documents formulas, thresholds, quality weights, ethical limits, synthetic
scope, local-import rules, and provider limitations. Architecture and data
guides explain the implemented flow and exact demo-generation command.

### DevOps and infrastructure

Scientific dependencies and type stubs are locked in `uv.lock`. Existing CI,
Dockerfiles, Compose, Makefile, and frontend lockfile remain valid. The dataset
policy check prevents tracked raw/interim/processed data, unsafe serialized
models, and files above the configured size limit.

## 3. Important files created or changed

- `backend/app/data/registry.py`: validates source rights and default import policy.
- `backend/app/data/schemas.py`: canonical tracking, event, and quality-flag contracts.
- `backend/app/data/synthetic.py`: deterministic fictional match generator.
- `backend/app/data/importers/`: local-only Metrica and gated StatsBomb adapters.
- `backend/app/data/cleaning.py`: ordering, deduplication, and interpolation.
- `backend/app/data/manifest.py`: SHA-256 file provenance and rights snapshots.
- `backend/app/data/quality.py`: transparent bounded data-quality report.
- `backend/app/data/storage.py`: safe Parquet read/write boundary.
- `backend/app/data/processing.py`: complete synthetic processing pipeline.
- `backend/app/analytics/`: movement, intensity, sprint, window, and event metrics.
- `backend/app/cli.py`: local `generate-demo` command.
- `backend/tests/unit/` and `backend/tests/integration/`: formula, adapter, safety,
  determinism, storage, and end-to-end tests.
- `data/sources.yml`: current source evidence and rights statuses.
- `docs/METHODOLOGY.md`: formulas, thresholds, interpretation, and limitations.
- `docs/DATASET_ATTRIBUTION.md`: official Day 2 rights re-verification evidence.
- `docs/ARCHITECTURE.md` and `data/README.md`: current data flow and usage guide.

## 4. How the system currently works

```text
Synthetic demo command
-> fixed-seed fictional tracking and events
-> canonical metre/time tables
-> sort, deduplicate, short-gap interpolation
-> movement, intensity, sprint, window, and event metrics
-> quality score and limitations
-> six ignored local Parquet tables + JSON terminal summary
```

For optional external data:

```text
Developer-supplied local file
-> source registry and explicit rights gate
-> Metrica CSV or StatsBomb JSON adapter
-> coordinate conversion and validation
-> canonical table
```

No browser dashboard consumes these results yet; relational persistence and APIs
are Day 3 work, and the complete data-driven UI is Day 4 work.

## 5. How I can check the work

Use Windows PowerShell. The repository folder for all commands below is:

```powershell
Set-Location 'C:\Users\DIPNA\Pictures\PlayerPulse'
$env:UV_CACHE_DIR="$PWD\.uv-cache"
$env:UV_PYTHON_INSTALL_DIR="$PWD\.uv-python"
```

1. Check the structure:

   ```powershell
   Get-ChildItem
   Get-ChildItem backend\app\data
   Get-ChildItem backend\app\analytics
   ```

   Expect `backend`, `frontend`, `data`, `docs`, and `scripts`, plus the data and
   analytics modules listed in section 3.

2. Install exact dependencies if this is a fresh checkout:

   ```powershell
   uv sync --project backend --all-groups
   npm.cmd --prefix frontend ci
   ```

   Expect uv and npm to finish without an error. Do not create or commit `.env`.

3. Generate synthetic demo analytics:

   ```powershell
   uv run --project backend python -m app.cli generate-demo --output data/processed/demo
   Get-ChildItem data\processed\demo\*.parquet
   ```

   Expect JSON with `"is_synthetic": true`, a quality object, and six paths:
   tracking, events, movement features, sprints, match windows, and event
   metrics. The second command should list six Parquet files. These files are
   ignored and safe to regenerate.

4. Inspect deterministic and adapter checks:

   ```powershell
   uv run --project backend pytest backend/tests/unit/test_synthetic_data.py -q
   uv run --project backend pytest backend/tests/unit/test_metrica_importer.py backend/tests/unit/test_statsbomb_importer.py -q
   uv run --project backend pytest backend/tests/unit/test_canonical_schemas.py backend/tests/unit/test_coordinates.py -q
   ```

   Expect `5 passed`, then `6 passed`, then `8 passed`. The fixtures are generated
   locally and contain no third-party football records.

5. Check cleaning, movement, intensity, sprints, windows, events, and quality:

   ```powershell
   uv run --project backend pytest backend/tests/unit/test_cleaning.py backend/tests/unit/test_movement_distance.py backend/tests/unit/test_movement_speed.py backend/tests/unit/test_movement_acceleration.py backend/tests/unit/test_movement_outliers.py backend/tests/unit/test_movement_smoothing.py -q
   uv run --project backend pytest backend/tests/unit/test_intensity_zones.py backend/tests/unit/test_sprints.py backend/tests/unit/test_match_windows.py backend/tests/unit/test_event_metrics.py backend/tests/unit/test_data_quality.py -q
   ```

   Expect the first group to report 15 passed and the second 12 passed.

6. Check manifests, Parquet, and the full pipeline:

   ```powershell
   uv run --project backend pytest backend/tests/unit/test_import_manifest.py backend/tests/unit/test_parquet_storage.py backend/tests/integration/test_demo_pipeline.py -q
   ```

   Expect `7 passed`.

7. Start the backend:

   ```powershell
   uv run --project backend uvicorn app.main:app --reload
   ```

   Expect `Uvicorn running on http://127.0.0.1:8000`. Open these URLs:

   - `http://127.0.0.1:8000/api/v1/health` -> status `ok`
   - `http://127.0.0.1:8000/api/v1/readiness` -> status `ready`
   - `http://127.0.0.1:8000/api/v1/version` -> version `0.1.0`
   - `http://127.0.0.1:8000/docs` -> FastAPI documentation

   Press `Ctrl+C` in that terminal to stop it.

8. Start the frontend in a second PowerShell terminal from the same root:

   ```powershell
   npm.cmd --prefix frontend run dev
   ```

   Open `http://localhost:5173`. Expect the PlayerPulse shell, navigation,
   non-medical disclaimer, and Day 1 placeholder pages. Press `Ctrl+C` to stop.

9. Run all checks:

   ```powershell
   uv run --project backend ruff format --check .
   uv run --project backend ruff check .
   uv run --project backend mypy
   uv run --project backend pytest --cov=app
   npm.cmd --prefix frontend run format:check
   npm.cmd --prefix frontend run lint
   npm.cmd --prefix frontend run typecheck
   npm.cmd --prefix frontend test -- --run
   npm.cmd --prefix frontend run build
   uv run --project backend python scripts/check_dataset_files.py
   docker compose config
   ```

   Expect every command to exit successfully. Pytest currently prints one
   upstream Starlette TestClient deprecation warning.

10. Check Git and the Day 2 tag:

    ```powershell
    git status
    git tag -n
    git rev-list --count day-1-complete..day-2-complete
    git log --oneline --decorate -n 35
    ```

    Expect a clean tree, `day-1-complete` and `day-2-complete`, and at least 30
    commits between those tags.

## 6. Verification checklist

```text
[ ] Repository includes data, analytics, adapter, test, and methodology modules
[ ] Health, readiness, and version endpoints return successful responses
[ ] Frontend shell opens and navigation still works
[ ] Demo CLI says is_synthetic=true
[ ] Six Parquet outputs are generated under ignored data/processed
[ ] Synthetic generation is deterministic and includes substitutions
[ ] Metrica adapter accepts only a supplied local CSV
[ ] StatsBomb adapter fails closed without rights acknowledgement
[ ] Canonical schemas and coordinate boundaries pass
[ ] Cleaning and short-gap interpolation tests pass
[ ] Distance, speed, acceleration, intensity, sprint, and window tests pass
[ ] Event metrics and data-quality tests pass
[ ] Import manifest and Parquet round-trip tests pass
[ ] Backend and frontend full test/static/build checks pass
[ ] Dataset-file policy finds no prohibited tracked data
[ ] Docker Compose configuration parses
[ ] No secrets, external raw football data, or unsafe models are committed
[ ] day-2-complete exists and the working tree is clean
```

## 7. Tests and checks performed

Passed:

- `uv run ruff format --check .` from `backend`: 62 files already formatted.
- `uv run ruff check .` from `backend`: all checks passed.
- `uv run mypy` from `backend`: 61 source files, no issues.
- `uv run pytest --cov=app --cov-report=term-missing` from `backend`: 71
  passed, 96% total coverage, one upstream deprecation warning.
- `npm.cmd run format:check`, `lint`, `typecheck`, `test -- --run`, and `build`
  from `frontend`: all passed; 1 Vitest test; Vite built 95 modules.
- `uv run --project backend python -m app.cli generate-demo --output
  data/processed/day2-check --period-duration 30`: six Parquet tables, 10,836
  rows, quality 100, high confidence, no limitations.
- `uv run --project backend python scripts/check_dataset_files.py`: passed; no
  prohibited tracked data.
- `uv run --project backend alembic -c backend/alembic.ini upgrade head`:
  passed against the current empty revision baseline.
- `docker compose config`: passed; database/backend/frontend parsed.
- A live hidden Uvicorn smoke check returned health `ok`, readiness `ready`,
  and version `0.1.0`.

Failed and resolved:

- Initial strict mypy runs identified missing `types-PyYAML` and `pandas-stubs`;
  they were added to the dev dependency group through uv and checks then passed.
- Floating-point exact-equality sprint/smoothing tests were corrected to use
  approximate numerical assertions; production calculations were unchanged.
- The first combined migration command reached `downgrade -1` and returned
  `Relative revision -1 didn't produce 1 migrations`. This is expected because
  Day 3 has not created the first domain migration. The successful upgrade was
  retained as the applicable Day 2 check.

Skipped:

- Full `docker compose up --build`: skipped because Day 2 changed no container
  topology and Compose validation passed; full stack runtime is required on Day 5.
- Interactive browser inspection/screenshots: skipped because Day 2 has no
  data-driven UI; the unchanged frontend passed test and production build.
- Real Metrica/StatsBomb files: intentionally skipped to avoid downloading or
  redistributing data without a user-supplied local file and fresh rights check.

## 8. Git summary

- Commits created before final report/ledger commits: 32 substantive commits.
- Starting commit: `ab929e6` (`day-1-complete`).
- Ending checkpoint: annotated tag `day-2-complete` on `main`.
- Latest implementation/handoff commit before this report: `e96df97`.
- Daily tag: `day-2-complete`.
- Branch: `main` (no phase-named branch was created).
- Working tree at handoff: clean after the report, generated ledger, and tag.
- Categories: rights/dependencies; schemas/generation/adapters; cleaning;
  movement/intensity/sprints/windows/events; quality/provenance/Parquet;
  integration/CLI; methodology/architecture/progress.

Useful checkpoint commands:

```text
git status
On branch main
nothing to commit, working tree clean

git log --oneline --decorate -n 35
(The live output contains all Day 2 commits from the checkpoint tag back through
the rights re-verification; use the command in section 5 for exact hashes.)
```

The exact final commit count and tag target are derived from Git after the
report/ledger commits and are shown in the chat copy of this report; Git is the
source of truth and `docs/COMMIT_LOG.md` is generated from it.

## 9. Screenshots to capture

1. Open PowerShell after the demo CLI finishes. Show `is_synthetic: true`, the
   quality score, and six output paths. Filename: `day2-demo-pipeline.png`.
   Caption: “PlayerPulse deterministic fictional match processed into six
   analytics-ready Parquet tables.”
2. Open PowerShell after the 71-test coverage run. Show `71 passed` and `96%`.
   Filename: `day2-backend-tests.png`. Caption: “Rights-aware ingestion and
   analytics test suite with branch coverage.”
3. Open `docs/METHODOLOGY.md` rendered in GitHub or an editor. Show the movement
   methodology and intensity-zone table. Filename: `day2-methodology.png`.
   Caption: “Transparent PlayerPulse workload thresholds and ethical scope.”
4. Open PowerShell after `git log --oneline --decorate -n 35`. Show
   `day-2-complete` and the atomic feature commits. Filename:
   `day2-git-history.png`. Caption: “Auditable Day 2 development history.”

Do not use screenshots of raw third-party data or imply that the current
placeholder frontend displays analytics.

## 10. Known limitations

- The demo uses compressed 180-second periods for fast local and CI execution;
  it is synthetic software evidence, not validation against a 90-minute match.
- The Metrica-compatible adapter expects documented long-form normalized CSV,
  not the provider's wide multi-header sample layout.
- StatsBomb support is event-only; tracking-dependent metrics remain unavailable.
- Relational teams/players/matches/metrics, processing APIs, baselines, and risk
  explanations are Day 3 work.
- The frontend has no live analytics dashboard until Day 4.
- Generated Parquet is local and ignored; it is not a deployed durable store.
- Docker Compose was configuration-validated but the full stack was not started.
- The test suite exposes one upstream Starlette/httpx deprecation warning.

## 11. Problems found and fixed

- Scientific packages lacked typing metadata under strict mypy. Locked type-stub
  packages fixed the issue without weakening strict mode.
- Windows newline behavior changed a temporary fixture's byte size. The manifest
  test now compares against the real filesystem size, which is portable.
- Floating-point arithmetic produced values such as `3.9000000000000004`.
  Numerical tests now use appropriate tolerance rather than brittle equality.
- Intensity boundary arithmetic represented 7.0 slightly below the boundary.
  Classification rounds computed speed to six decimals before applying documented
  bands, making exact boundaries stable.
- The synthetic dropout was initially too long for the documented 0.5-second
  interpolation limit. Tracking was changed to 10 Hz and the dropout to 0.2
  seconds so the full pipeline genuinely exercises safe interpolation.

## 12. Next development day

Day 3 will add real Alembic domain migrations; teams, players, matches, metrics,
processing jobs, and quality persistence; demo/match/player/heatmap APIs;
baseline selection; transparent rule-based performance-risk scores and
explanations; confidence/data-quality handling; minimum-data-gated Isolation
Forest fallback; API docs; and invalid upload protection. No Day 3 work has
started.

## 13. Resume instruction

`Continue to Day 3; first read AGENTS.md, docs/PROGRESS.md, docs/IMPLEMENTATION_PLAN.md, docs/COMMIT_LOG.md, and docs/DAY_2_REPORT.md, then verify clean main and day-2-complete before starting.`
