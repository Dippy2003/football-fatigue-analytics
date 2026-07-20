# PLAYERPULSE — MASTER CODEX BUILD PROMPT

**Audited edition:** FINAL v4, reviewed on 2026-07-20 - includes dataset-rights controls, explicit analytics defaults, reproducibility gates, production-security rules, deployment constraints, and corrected Git-history procedures.

## 0. Your role

Act as the lead software architect, senior full-stack engineer, data scientist, machine-learning engineer, QA engineer, DevOps engineer, security reviewer, technical writer, and Git maintainer for this repository.

Your mission is to build **PlayerPulse**, a portfolio-quality football player workload, fatigue-indicator, and performance-risk analytics platform, from an empty or partially completed repository to a tested, documented, deployable application.

The project must be completed through five controlled development phases called **Day 1** through **Day 5**. “Day” means a development phase bounded by Git checkpoint tags, not necessarily a single uninterrupted Codex session or literal calendar day. Each phase must finish with a working, testable checkpoint. Maintain at least **30 meaningful atomic Git commits per day**, for a minimum of **150 meaningful commits overall**.

Do not create empty commits, fake commits, duplicate commits, or commits that only change whitespace to increase the count. Every commit must represent a coherent, reviewable improvement. Never sacrifice correctness, testing, security, or documentation merely to reach the commit target.

---

# 1. Product definition

## Product name

**PlayerPulse**

## Full title

**PlayerPulse: An Explainable Football Player Workload, Fatigue-Indicator and Performance-Risk Analytics Platform**

## One-line description

PlayerPulse analyses football tracking and event data to calculate player workload, detect unusual performance decline, visualize movement, and generate explainable fatigue-indicator risk scores for coaches and analysts.

## Intended users

- Football coaches
- Performance analysts
- Sports-science students
- Data analysts
- Team staff
- Portfolio reviewers and recruiters

## Required reviewer journey

A clean-clone reviewer must be able to:

1. Start the backend and frontend using documented commands or Docker Compose.
2. Load the deterministic synthetic demo without credentials or external downloads.
3. Open the generated match and see its synthetic/source status.
4. Select a player and view movement, workload, sprint, time-window, quality, baseline, and risk-indicator results.
5. Read the factor explanation, confidence, limitations, and non-medical disclaimer.
6. Compare multiple players.
7. Open the methodology, data-rights, model-card, and project case-study pages.
8. Run tests and reproduce the demo processing pipeline.

## MVP non-goals

Do not expand the five-day MVP into:

- medical diagnosis or confirmed injury prediction
- live GPS or wearable-device ingestion
- computer vision from match video
- live match streaming or real-time alerts
- a mobile application
- multi-club tenancy
- complex authentication and role management
- payment, subscription, or commercial licensing features
- a durable distributed job queue
- deep-learning models
- scraping protected football websites
- storage of real athlete health or biometric records

Document these as future-work possibilities only when appropriate.

## Ethical positioning

This is a performance analytics and decision-support platform.

It must never claim to:

- Diagnose fatigue medically
- Predict a confirmed injury
- Replace a doctor, physiotherapist, sports scientist, or medical assessment
- Recommend medical treatment
- Prove that a player is injured

Use terms such as:

- Fatigue indicators
- Performance-risk score
- Workload warning
- Possible performance decline
- Recovery review recommended
- Decision-support insight

Display a visible disclaimer wherever risk results appear:

> PlayerPulse provides performance-based indicators from available match data. It is not a medical diagnostic tool and must not be used as a substitute for qualified medical or sports-science assessment.

---

# 2. Working method and autonomy rules

1. First inspect the repository, current branch, Git status, existing files, installed tools, and environment.
2. Preserve all valid user work. Never overwrite or delete user-created work without a clear technical reason.
3. If the repository is empty, initialize the complete project.
4. If it is partially built, compare it with this specification and continue from the current state.
5. Do not wait for the user after every minor decision. Use sound engineering judgement.
6. Ask the user only when truly blocked by unavailable credentials, an inaccessible external service, or a destructive decision that cannot safely be inferred.
7. Prefer a working vertical slice over disconnected mock components.
8. Run relevant checks before every major checkpoint and before declaring a task complete.
9. Never claim a command, test, deployment, migration, or feature succeeded unless it was actually run and verified.
10. When something cannot be completed, document the blocker precisely and implement the safest local fallback.
11. Never expose secrets, tokens, passwords, private keys, or connection strings.
12. Never commit `.env`, downloaded private data, generated caches, database files, model binaries larger than reasonable repository limits, or build artifacts.
13. Use current stable package releases that are mutually compatible. Record resolved versions in lockfiles.
14. Keep architecture intentionally manageable for a five-day student portfolio build.
15. Avoid unnecessary microservices, Redux, Kubernetes, Kafka, distributed training, deep learning, or premature optimization.
16. Prefer clear, typed, tested code over clever code.
17. Keep functions focused and modules cohesive.
18. Add comments only where intent is not obvious.
19. Record major technical decisions in `docs/DECISIONS.md`.
20. Update progress documents continuously rather than reconstructing progress at the end.

---

# 3. Mandatory project stack

## Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui accessible component primitives
- React Router
- TanStack Query for server-state fetching and caching
- Axios through a small typed API-client layer
- Recharts for interactive dashboard charts
- Custom responsive SVG football pitch for pitch-based visualizations
- Vitest
- React Testing Library
- ESLint
- Prettier

## Backend

- Python 3.12 as the primary backend runtime
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- Alembic
- PostgreSQL for the production-ready configuration
- SQLite fallback for quick local/demo execution when PostgreSQL is unavailable
- Pytest
- Ruff
- mypy
- Pydantic Settings for typed environment configuration

## Data science and analytics

- Pandas
- NumPy
- SciPy
- scikit-learn
- Joblib
- PyArrow for Parquet
- mplsoccer where helpful
- Kloppy where it improves dataset interoperability
- XGBoost only after the baseline system works and only if it provides measurable value
- SHAP only if compatible and useful; otherwise implement transparent factor contributions without forcing SHAP

## Development and deployment

- Git and GitHub-ready repository
- Docker
- Docker Compose
- GitHub Actions
- Vercel-ready frontend configuration
- Render-ready or equivalent backend configuration
- PostgreSQL-ready environment variables

## Fixed implementation choices for this five-day build

Use these choices unless the existing repository already contains a compatible alternative that is working and documented:

- Use **npm** as the frontend package manager and commit `package-lock.json`.
- Use **Python 3.12** as the primary backend runtime for ecosystem stability; record it in `.python-version`. A newer installed Python may be used only after all required libraries and tests are confirmed compatible.
- Use **uv** with `pyproject.toml` and `uv.lock` for Python dependency management. If `uv` cannot be installed in the environment, use `python -m venv` plus a fully pinned requirements export and document the fallback.
- Use **Recharts** for standard dashboard charts and a custom accessible SVG component for the football pitch and heatmap. Do not add Plotly unless a required visualization cannot be implemented cleanly with this choice.
- Use **TanStack Query** and a small typed Axios client. Do not add Redux.
- Use **UUIDs** for internal database identifiers and keep provider identifiers in separate `external_id` fields.
- Store timestamps in **UTC** and serialize them as ISO 8601 strings.
- Use **SQLite** for the zero-configuration demo and fast local tests, and **PostgreSQL** for production and PostgreSQL integration tests.
- Use an **in-process background job service** for the MVP processing-job API. Do not add Celery, Redis, RabbitMQ, or another queue in the five-day build. Document that in-process jobs are not durable across backend restarts.
- Use deterministic seeds for synthetic data, model training, tests, and screenshots.
- Commit generated dependency lockfiles, but never edit lockfiles manually.

---

# 4. Required repository structure

Create or evolve toward this structure:

```text
playerpulse/
├── AGENTS.md
├── README.md
├── LICENSE
├── THIRD_PARTY_NOTICES.md
├── SECURITY.md
├── CHANGELOG.md
├── .gitignore
├── .editorconfig
├── .env.example
├── .python-version
├── .nvmrc
├── docker-compose.yml
├── Makefile
├── scripts/
│   ├── export_commit_log.py
│   ├── check_dataset_files.py
│   └── verify_release.py
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── charts/
│   │   │   ├── common/
│   │   │   ├── layout/
│   │   │   └── pitch/
│   │   ├── features/
│   │   │   ├── dashboard/
│   │   │   ├── matches/
│   │   │   ├── players/
│   │   │   ├── risk/
│   │   │   └── methodology/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── test/
│   │   ├── types/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/
│   ├── tests/
│   ├── Dockerfile
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.ts
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   └── dependencies.py
│   │   ├── analytics/
│   │   │   ├── coordinates.py
│   │   │   ├── cleaning.py
│   │   │   ├── movement.py
│   │   │   ├── intensity.py
│   │   │   ├── sprints.py
│   │   │   ├── windows.py
│   │   │   ├── workload.py
│   │   │   ├── event_metrics.py
│   │   │   ├── baselines.py
│   │   │   ├── risk.py
│   │   │   └── explanations.py
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── ml/
│   │   │   ├── features.py
│   │   │   ├── train.py
│   │   │   ├── inference.py
│   │   │   ├── evaluation.py
│   │   │   └── registry.py
│   │   └── main.py
│   ├── scripts/
│   ├── tests/
│   │   ├── fixtures/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── api/
│   ├── alembic/
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── uv.lock
│   └── alembic.ini
├── data/
│   ├── README.md
│   ├── sources.yml
│   ├── raw/.gitkeep
│   ├── interim/.gitkeep
│   ├── processed/.gitkeep
│   └── samples/
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_tracking_quality.ipynb
│   ├── 03_feature_engineering.ipynb
│   └── 04_model_evaluation.ipynb
├── models/
│   ├── README.md
│   └── .gitkeep
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API.md
│   ├── CASE_STUDY.md
│   ├── DATA_CARD.md
│   ├── DATA_DICTIONARY.md
│   ├── DATA_PIPELINE.md
│   ├── DATASET_ATTRIBUTION.md
│   ├── DECISIONS.md
│   ├── DEPLOYMENT.md
│   ├── ETHICS_AND_LIMITATIONS.md
│   ├── IMPLEMENTATION_PLAN.md
│   ├── METHODOLOGY.md
│   ├── MODEL_CARD.md
│   ├── PROGRESS.md
│   ├── COMMIT_LOG.md
│   ├── TESTING.md
│   ├── THREAT_MODEL.md
│   ├── USER_GUIDE.md
│   └── screenshots/
└── .github/
    ├── workflows/
    │   ├── ci.yml
│   └── dependency-review.yml
    ├── ISSUE_TEMPLATE/
    └── pull_request_template.md
```

Adjust names only when there is a strong reason. Document deviations.

---

# 5. Codex repository instructions

Create `AGENTS.md` during the first phase. It must state:

- Product purpose and ethical boundaries
- Repository map
- Standard setup commands
- Backend commands
- Frontend commands
- Test commands
- Lint and type-check commands
- Migration commands
- Docker commands
- Rules for dataset handling
- Rules for risk terminology
- Required checks before committing
- Required checks before ending a phase
- Commit-message convention
- Progress-document update rules
- Never edit generated lockfiles manually
- Never commit secrets or large raw datasets
- Preserve user changes
- Update tests when behavior changes
- Update documentation when APIs, schemas, architecture, setup, or methodology changes
- Use npm and commit `package-lock.json`
- Use uv and commit `uv.lock`, or document the approved fallback
- Never load a user-uploaded Joblib or pickle model
- Keep production uploads disabled unless explicitly configured
- Keep third-party source attribution visible and never imply PlayerPulse owns external data
- Do not push, force-push, create a remote repository, open a pull request, or publish a release unless the user explicitly authorizes that external action
- Generate `docs/COMMIT_LOG.md` from Git history at checkpoints instead of trying to place a commit's own hash inside that same commit

---

# 6. Data-source strategy, rights and attribution

Treat dataset rights as a release-blocking requirement. Public availability on GitHub does not automatically permit unrestricted copying, redistribution, modification, commercial use, or hosting. This section is an engineering compliance rule, not legal advice.

## 6.1 Approved source registry

Record these exact official source URLs in `docs/DATASET_ATTRIBUTION.md`, the README, and the Methodology/About UI where the corresponding data is used.

### Metrica Sports sample tracking and event data

- Official repository: `https://github.com/metrica-sports/sample-data`
- Repository legal/usage statement: read the **Legal stuff** section of the repository README before use.
- Intended project use: optional local development and analytics validation for tracking coordinates and synchronized events.
- Required attribution name: **Metrica Sports**
- Rights caution: the repository README says the sample data is provided for the football analytics community and asks users to acknowledge the source for public use, but the repository does not present a separate standard open-data license file in its root. Therefore, do not assume unrestricted redistribution rights.
- Repository policy:
  - Do not commit copies of Metrica raw match files to this repository.
  - Do not package Metrica raw data into Docker images, frontend assets, releases, or deployed databases.
  - Provide an importer that reads data supplied locally by the developer.
  - Provide instructions linking users to the official source.
  - Keep the public hosted demo functional using deterministic synthetic tracking data.
  - Before any broader redistribution or commercial use, obtain explicit permission or independently verify applicable rights.

### Hudl StatsBomb Open Data

- Official repository: `https://github.com/hudl/open-data`
- License file: `https://github.com/hudl/open-data/blob/master/LICENSE.pdf`
- Repository terms and getting-started information: read the repository README and current license before use.
- Intended project use: optional event-data analysis for passes, shots, pressures, tackles, interceptions, possession losses, lineups, and supported 360 data.
- Required attribution name: **StatsBomb**
- Attribution requirement: when publishing, sharing, or distributing research, analysis, or insights based on the data, identify StatsBomb as the source and follow the current logo/branding requirement stated by the official repository.
- Repository policy:
  - Do not remove attribution.
  - Include the required attribution in `README.md`, `docs/DATASET_ATTRIBUTION.md`, the About page, the Methodology page, and any exported report based on the data.
  - Link to the official repository rather than mirroring the full dataset in this repository.
  - Do not claim ownership of the data.
  - Re-check the current license before public deployment or release because terms may change.

## 6.2 Default development and demo data

Use **deterministic synthetic tracking and event data generated by this project** as the default dataset for:

- Automated tests
- CI
- Public screenshots
- Public hosted demo
- Docker demo environment
- End-to-end tests
- Portfolio walkthroughs

Synthetic data must:

- Be generated by project code.
- Use a fixed random seed.
- Be visibly marked with `is_synthetic=true`.
- Use fictional teams and anonymized player labels.
- Not reproduce or closely copy a real match.
- Never be described as real tracking or event data.

The public application must remain fully functional even when no third-party dataset has been downloaded.

## 6.3 Dataset rights gate

Before implementing or enabling any external dataset adapter, Codex must:

1. Open the official source page and current license/terms.
2. Record:
   - dataset name
   - provider
   - official source URL
   - license/terms URL
   - access date
   - allowed uses
   - attribution requirements
   - redistribution restrictions
   - commercial-use restrictions
   - modification/derivative-data restrictions
   - hosting restrictions
   - uncertainty or missing-license warning
   - repository owner and canonical repository URL
   - checked branch, tag, or commit SHA
   - exact verification timestamp in UTC
   - SHA-256 of the retrieved licence/terms file when technically available
3. Add the record to `docs/DATASET_ATTRIBUTION.md`.
4. Add a machine-readable entry to `data/sources.yml`.
5. Mark the adapter as one of:
   - `project_owned_synthetic`
   - `verification_required`
   - `local_import_only`
   - `public_use_with_conditions`
   - `permission_required`
   - `disabled_due_to_unclear_rights`
6. Do not download, copy, commit, publish, or deploy the dataset when the relevant permission is unclear.
7. Prefer a local user-supplied import flow when redistribution is not clearly permitted.
8. Fail safely with an explanatory message rather than silently downloading restricted data.

## 6.4 Required machine-readable source registry

Create `data/sources.yml` with fields similar to:

```yaml
sources:
  - id: synthetic_playerpulse
    provider: PlayerPulse
    source_url: null
    terms_url: null
    access_date: YYYY-MM-DD
    verified_commit: null
    terms_sha256: null
    usage_status: project_owned_synthetic
    redistribution: allowed
    attribution: "Generated by PlayerPulse"
    notes: "Deterministic fictional data; never present as real."

  - id: metrica_sample_data
    provider: Metrica Sports
    source_url: "https://github.com/metrica-sports/sample-data"
    terms_url: "https://github.com/metrica-sports/sample-data#legal-stuff"
    access_date: YYYY-MM-DD
    verified_commit: null
    terms_sha256: null
    usage_status: local_import_only
    redistribution: "Do not redistribute from this repository without explicit permission or a clear licence grant."
    attribution: "Data source: Metrica Sports"
    notes: "Re-check the current repository terms before use."

  - id: statsbomb_open_data
    provider: StatsBomb
    source_url: "https://github.com/hudl/open-data"
    terms_url: "https://github.com/hudl/open-data/blob/master/LICENSE.pdf"
    access_date: YYYY-MM-DD
    verified_commit: null
    terms_sha256: null
    usage_status: verification_required
    redistribution: "Read the current README and licence before use; do not mirror the complete dataset by default."
    attribution: "Data source: StatsBomb; follow current official logo requirement."
    notes: "Re-check current terms before public release."
```

Populate `access_date` with the actual date Codex verifies the terms. Do not copy this example blindly without checking the current official pages.

## 6.5 Dataset implementation rules

1. Add required attribution to:
   - `README.md`
   - `docs/DATASET_ATTRIBUTION.md`
   - About page
   - Methodology page
   - Exported reports based on external data
2. Never commit large downloaded datasets.
3. Never commit third-party raw data unless the source registry explicitly confirms repository redistribution is permitted.
4. Provide reproducible import scripts, not unlicensed dataset mirrors.
5. Include synthetic fixtures sufficient for tests and public demo fallback.
6. Add checksums and source metadata for locally imported external files where practical.
7. Store:
   - locally supplied raw files under ignored `data/raw/`
   - normalized files under ignored `data/interim/`
   - analytics-ready Parquet files under ignored `data/processed/`
8. Make ignored directories reproducible using `.gitkeep` and documentation.
9. Save provider, source URL, access date, license-status label, and synthetic/real status with imported match metadata.
10. Show the dataset source and synthetic/real status in the UI.
11. Never present synthetic data as real match data.
12. Never present third-party data as owned by PlayerPulse.
13. Do not use club badges, league marks, provider logos, player photographs, or other protected media unless their use is clearly permitted. Where StatsBomb’s terms require a logo, link to or include it only according to the current official media-pack instructions.
14. Add a CI check that fails when prohibited raw-data file patterns or oversized dataset files are staged.
15. Add a release-checklist item requiring re-verification of external dataset terms.

## 6.6 Code licence, data licence and trademark separation

- The root `LICENSE` applies only to original PlayerPulse source code and original project documentation, unless it explicitly states otherwise.
- Do not state or imply that the root code licence relicenses Metrica, StatsBomb, club, competition, player, logo, photograph, or other third-party material.
- Create `THIRD_PARTY_NOTICES.md` listing every external dataset, library, icon set, font, logo, and other third-party asset used by the project.
- Use the MIT licence for original PlayerPulse code only if the repository does not already contain a different licence. Use `PlayerPulse contributors` as the copyright holder rather than inventing a person's legal name.
- Add a prominent notice that external datasets remain subject to their providers' separate terms.
- Treat provider names and logos as trademarks. Text attribution is the default; use a provider logo only when the current provider terms require or clearly permit it.
- Do not copy third-party licence text into the repository unless redistribution of that licence document is permitted. A verified official URL, access date, commit reference, and digest are sufficient when copying is uncertain.
- Do not place third-party raw data, provider logos, club badges, league badges, or player photographs under the project's code licence.

---

# 7. Core data pipeline

Implement the pipeline as independently testable stages.

## 7.1 Ingestion

Support:

- Metrica tracking CSV files
- Metrica event CSV files
- Optional StatsBomb JSON adapter
- Deterministic synthetic demo data

Validate:

- Required columns
- Match identifiers
- Team identifiers
- Player identifiers
- Frame or timestamp values
- Period values
- Coordinate ranges
- Duplicate rows
- Missing data
- Impossible values

Return actionable validation errors.

### Import manifest and provider-specific upload contract

The upload/import workflow must use an explicit manifest instead of guessing silently.

For a Metrica import, support the expected related files as separate multipart files or local paths supplied by the developer, such as home tracking, away tracking, events, and optional metadata. Validate that match IDs, periods, timestamps, and frame ranges are compatible before processing.

For a StatsBomb import, support selected official JSON files such as competition/match metadata, lineups, events, and optional 360 data. Clearly report which analyses are unavailable when full tracking is absent.

The import request and stored metadata must include:

- provider
- dataset source registry ID
- expected file role for each file
- original filename
- SHA-256 checksum
- file size
- detected MIME type
- source match identifier
- is_synthetic
- rights-status snapshot
- import timestamp

Never infer a provider solely from a filename when the content is ambiguous.

## 7.2 Canonical schema

Normalize all providers into canonical internal schemas.

### Tracking record

Include fields similar to:

- match_id
- period
- frame_id
- timestamp_seconds
- team_id
- player_id
- x
- y
- ball_x
- ball_y
- source
- is_synthetic

### Event record

Include fields similar to:

- event_id
- match_id
- period
- timestamp_seconds
- team_id
- player_id
- event_type
- outcome
- start_x
- start_y
- end_x
- end_y
- source
- is_synthetic

## 7.3 Coordinate conversion

Use one canonical coordinate convention throughout the backend, database, API, tests, and frontend:

- metres as the unit
- `x=0` at the left touchline end and `x=pitch_length_m` at the right touchline end
- `y=0` at the top touchline and `y=pitch_width_m` at the bottom touchline when displayed in the standard top-down orientation
- preserve the original provider coordinates and transformation metadata for auditability

- Convert normalized source coordinates to metric pitch coordinates.
- Default configurable pitch dimensions: 105 m × 68 m.
- Preserve source-coordinate fields when useful for auditing.
- Correct team direction so attacking-direction comparisons are consistent when appropriate.
- Unit-test coordinate boundaries and conversions.

## 7.4 Tracking-data cleaning

Implement:

- Sorting by player and timestamp
- Duplicate removal
- Missing-frame detection
- Short-gap interpolation with configurable maximum gap
- No interpolation across halftime or long gaps
- Coordinate clipping only when justified and logged
- Impossible teleport/jump detection
- Speed outlier detection
- Optional smoothing using a documented, configurable method
- Data-quality flags
- Quality summary per player and match

Never hide cleaning decisions.

## 7.5 Movement metrics

Calculate:

- Step distance
- Total distance
- Active distance
- Distance per minute
- Instantaneous speed
- Smoothed speed
- Maximum credible speed
- Average speed
- Acceleration
- Deceleration
- Playing duration

Handle:

- Missing frames
- Substitutions
- Halftime
- Different sampling frequencies
- Players not visible in all frames
- Goalkeepers separately where appropriate

## 7.6 Intensity zones

Create configurable defaults, clearly labelled as analytical thresholds rather than universal medical standards.

Suggested initial zones:

- Standing/walking
- Jogging
- Running
- High-speed running
- Sprinting

Keep thresholds in configuration, not hard-coded throughout the application.

## 7.7 Sprint detection

Define a sprint as a configurable sequence above the sprint-speed threshold for a minimum duration or minimum number of frames.

Calculate:

- Sprint count
- Sprint distance
- Sprint duration
- Peak sprint speed
- Time between sprints
- Median recovery interval
- High-intensity effort count
- Sprint frequency per minute

Avoid counting one continuous sprint as multiple sprints because of single-frame noise.

## 7.8 Match windows

Calculate metrics for:

- First half
- Second half
- 15-minute windows
- Last 30 minutes
- Last 15 minutes
- User-selected interval where practical

Handle stoppage time consistently and document the choice.

## 7.9 Event metrics

Where event data is available, calculate:

- Passes attempted
- Pass completion
- Progressive passes if feasible
- Shots
- Pressures
- Tackles
- Interceptions
- Recoveries
- Possession losses
- Defensive actions
- Actions per minute

Do not invent event metrics when event data is absent. Return a supported-data indicator.

## 7.10 Player baseline

Create a baseline from available previous matches or comparable match periods.

Support:

- Personal historical baseline when enough matches exist
- Team/position baseline as fallback
- Match-only early-versus-late comparison for demo data
- Minimum sample-size checks

Store baseline type and confidence.

## 7.11 Feature table

Generate a player-match feature table including, where available:

- playing_minutes
- total_distance_m
- distance_per_minute
- average_speed_mps
- max_speed_mps
- high_speed_distance_m
- sprint_count
- sprint_distance_m
- median_sprint_recovery_seconds
- acceleration_count
- deceleration_count
- second_half_speed_change_pct
- late_match_sprint_change_pct
- late_match_distance_change_pct
- pass_accuracy_change_pct
- pressure_change_pct
- possession_loss_change
- workload_vs_baseline_zscore
- data_quality_score
- baseline_confidence
- supported_event_metrics

Persist processed features to Parquet and summarized records to the database.

## 7.12 Initial analytical configuration

Put these values in typed configuration so they can be changed without rewriting analytics code. They are engineering defaults for the portfolio demo, not universal sports-science or medical standards.

- pitch length: `105.0 m`
- pitch width: `68.0 m`
- maximum short-gap interpolation: `0.5 s`
- maximum credible player speed for quality checks: `12.5 m/s`
- smoothing: centred rolling median over approximately `0.20 s`, adjusted to the detected sample rate and never crossing a period boundary
- standing/walking: `< 2.0 m/s`
- jogging: `2.0 to < 4.0 m/s`
- running: `4.0 to < 5.5 m/s`
- high-speed running: `5.5 to < 7.0 m/s`
- sprinting: `>= 7.0 m/s`
- minimum sprint duration: `0.5 s`
- merge sub-threshold sprint gaps shorter than: `0.2 s`
- event/tracking synchronization tolerance: start at `0.10 s`, make configurable, and report unmatched events

Infer sample rate from trustworthy timestamps or provider metadata. Do not assume a fixed frame rate silently. Add a methodology note and tests for every default.

---

# 8. Risk-scoring methodology

## 8.1 Phase-one rule-based model

The first production-capable model must be transparent, deterministic, versioned, and fully tested. It is an engineering indicator model, not a clinically validated fatigue model.

Create these normalized factor scores using configurable piecewise-linear scaling and clamp each factor to `0..100`:

- **Speed-decline factor:** 0 at a decline of 5% or less; 100 at a decline of 35% or more.
- **Sprint-frequency-decline factor:** 0 at a decline of 10% or less; 100 at a decline of 60% or more.
- **Sprint-recovery-increase factor:** 0 at an increase of 10% or less; 100 at an increase of 80% or more.
- **Workload-versus-baseline factor:** 0 at a z-score of 1.0 or lower; 100 at a z-score of 3.0 or higher. Negative workload z-scores must not increase risk.
- **Event-performance-decline factor:** combine supported event-rate changes such as pass completion, defensive actions, pressures, and possession losses; 0 at negligible decline and 100 at the documented severe-demo threshold. Do not calculate this factor when suitable event data is unavailable.

Use these initial weights:

- speed decline: `25%`
- sprint-frequency decline: `25%`
- recovery-time increase: `20%`
- workload versus baseline: `20%`
- event-performance decline: `10%`

Rules:

1. Re-normalize weights only across available factors.
2. Require at least three core physical factors and at least 60% total metric coverage before issuing a numeric score.
3. If data quality is below 0.50, return `insufficient_data` instead of a numeric risk category.
4. Do not use data quality to artificially lower or raise the indicator score; use it to control confidence and availability.
5. Keep score and confidence separate.
6. Store every raw input, normalized factor, weight, threshold set, and formula version used for the assessment.
7. Add sensitivity tests around every threshold boundary.

Suggested categories:

- 0-30: Low indicator level
- 31-60: Moderate indicator level
- 61-80: High indicator level
- 81-100: Very high indicator level

Use neutral wording. Do not use “safe,” “injured,” “injury probability,” or “medically fatigued.”

### Baseline confidence defaults

Use transparent initial confidence values:

- personal baseline with at least 5 prior comparable matches: `1.00`
- personal baseline with 3-4 prior comparable matches: `0.80`
- position/team baseline with at least 10 comparable player-match records: `0.65`
- match-only early-versus-late comparison: `0.40`
- insufficient comparison data: no score

Calculate displayed confidence from:

- data quality: `50%`
- baseline confidence: `35%`
- feature coverage: `15%`

Document the formula and label confidence as data/model confidence, not medical certainty.

The risk response must include:

- assessment status (`available` or `insufficient_data`)
- overall score when available
- category when available
- confidence
- baseline type
- data-quality score
- feature coverage
- top contributing factors
- all factor contributions
- human-readable explanation
- missing-data limitations
- disclaimer
- formula/model version
- calculation timestamp

## 8.2 Anomaly-detection model

After the deterministic baseline is working:

- Train an Isolation Forest or another justified unsupervised anomaly detector.
- Use only well-defined numeric features.
- Fit preprocessing inside a scikit-learn Pipeline.
- Prevent train/test leakage.
- Store the training feature list.
- Save model metadata.
- Version the model artifact.
- Evaluate anomaly stability and inspect examples.
- Do not treat anomaly score as confirmed fatigue.
- Do not train the model with fewer than 50 valid player-match feature rows; prefer at least 100. If this threshold is not met, expose the rule-based model only and report `model_not_trained_insufficient_data`.
- The single demo match is not sufficient for anomaly-model training. Create a separate deterministic synthetic feature-level training corpus with at least 200 fictional player-match records, or use legally imported historical features.
- Never load a model artifact uploaded by a user. Joblib/pickle artifacts are trusted build artifacts produced only by this repository's training pipeline.
- Set and store `random_state`, library versions, training-data digest, training timestamp, feature schema version, and evaluation summary.

## 8.3 Model combination

If justified, combine:

- Rule-based score
- Anomaly score
- Confidence and data-quality information

Keep the combined score explainable. If combination harms clarity, retain the rule-based score as the primary displayed result and show anomaly detection as a separate signal.

## 8.4 Evaluation

Because confirmed fatigue labels may not exist:

- Do not report misleading accuracy.
- Evaluate data validity, feature stability, sensitivity, consistency, anomaly inspection, and deterministic test scenarios.
- Create synthetic scenarios:
  - Stable performance
  - Gradual late-match decline
  - Sudden tracking corruption
  - High workload without decline
  - Low workload with event decline
- Confirm the model responds logically.
- Document that these are validation scenarios, not clinical validation.
- Evaluate results separately by position where sample size permits; do not compare goalkeepers directly with outfield players without a visible warning.
- Document tactical context, score state, substitutions, role changes, match tempo, and data coverage as possible alternative explanations for late-match decline.
- Never use terms such as accuracy, sensitivity, specificity, or injury probability unless valid labelled ground truth and an appropriate evaluation design actually exist.

---

# 9. Database design

Create SQLAlchemy models and Alembic migrations for at least. Use UUID primary keys, UTC timestamps, explicit foreign keys, unique constraints for provider/external-ID pairs, and indexes for common filters.

## DatasetImport

- id
- provider
- source_registry_id
- source_url
- rights_status_snapshot
- is_synthetic
- original_filename_manifest_json
- aggregate_checksum
- import_status
- imported_at


## Team

- id
- external_id
- name
- source
- created_at

## Player

- id
- external_id
- team_id
- name or anonymized label
- position
- source
- created_at

## Match

- id
- external_id
- home_team_id
- away_team_id
- competition
- match_date
- pitch_length_m
- pitch_width_m
- source
- dataset_import_id
- is_synthetic
- processing_status
- created_at

## PlayerMatchMetric

- id
- match_id
- player_id
- playing_minutes
- metric fields
- data_quality_score
- baseline_type
- baseline_confidence
- feature_version
- created_at

## RiskAssessment

- id
- match_id
- player_id
- score
- category
- confidence
- rule_score
- anomaly_score
- explanation_json
- model_version
- created_at

## ProcessingJob

- id
- match_id
- status
- stage
- progress
- error_message
- started_at
- finished_at

Add constraints, relationships, useful indexes, and timestamp conventions. Use JSON columns only for genuinely variable metadata and explanations; keep commonly queried metrics in typed columns. Make demo-data creation idempotent so repeated requests do not create uncontrolled duplicates.

---

# 10. Backend API

Use versioned routes under `/api/v1`.

Implement at least:

## System

- `GET /api/v1/health`
- `GET /api/v1/readiness`
- `GET /api/v1/version`

## Data and processing

- `POST /api/v1/datasets/demo`
- `POST /api/v1/datasets/upload`
- `GET /api/v1/datasets/sources`
- `POST /api/v1/matches/{match_id}/process`
- `GET /api/v1/jobs/{job_id}`

## Matches

- `GET /api/v1/matches`
- `GET /api/v1/matches/{match_id}`
- `GET /api/v1/matches/{match_id}/players`
- `GET /api/v1/matches/{match_id}/team-summary`
- `GET /api/v1/matches/{match_id}/quality`

## Players

- `GET /api/v1/players/{player_id}`
- `GET /api/v1/players/{player_id}/matches`
- `GET /api/v1/matches/{match_id}/players/{player_id}/metrics`
- `GET /api/v1/matches/{match_id}/players/{player_id}/timeline`
- `GET /api/v1/matches/{match_id}/players/{player_id}/heatmap`
- `GET /api/v1/matches/{match_id}/players/{player_id}/risk`
- `GET /api/v1/matches/{match_id}/players/{player_id}/events`

## Comparisons

- `GET /api/v1/matches/{match_id}/compare-players`
- `GET /api/v1/players/{player_id}/baseline`

API requirements:

- Use a standard error body with `code`, `message`, `details`, `request_id`, and `timestamp`.
- Return heatmaps as bounded aggregated grids and timelines as appropriately downsampled points rather than returning every raw tracking frame to the browser.
- Use multipart multi-file upload with an explicit provider and file-role manifest.
- Make `POST /datasets/demo` idempotent or return the existing deterministic demo import.
- Use in-process background tasks for MVP processing and persist job state, while documenting that interrupted jobs may need to be retried after a process restart.
- Disable third-party file uploads in public production by default using `ENABLE_UPLOADS=false`.

- Pydantic request and response schemas
- Consistent error schema
- Pagination where lists may grow
- Filtering and sorting for matches and players
- Valid HTTP status codes
- OpenAPI descriptions and examples
- Upload file-size limit, file-count limit, parsed-row limit, and processing concurrency limit
- Allowed extensions and MIME checks
- Filename sanitization
- No arbitrary file-path access
- CORS configured through environment variables
- Structured application logging
- Request IDs where practical
- No stack traces returned to clients in production

---

# 11. Frontend product requirements

Create a polished, responsive, accessible analytics dashboard. It should look like a serious sports-performance product, not a generic admin template.

## Visual direction

- Professional football analytics aesthetic
- Clean light and dark modes
- Strong information hierarchy
- Restrained use of color
- Risk states must use label + icon + color, never color alone
- Avoid excessive gradients, glassmorphism, animations, and decorative clutter
- Use football-pitch visuals only when informative
- Mobile usable, desktop optimized
- Include loading, empty, error, and unavailable-data states

## Pages

### 11.1 Landing/demo page

Include:

- Product explanation
- Ethical disclaimer
- “Load demo match” action
- Supported analysis summary
- Dataset attribution
- Link to methodology

### 11.2 Dashboard

Include:

- Match selector
- Total players analysed
- Highest workload
- Number of elevated indicator scores
- Data-quality summary
- Team intensity over time
- Player workload ranking
- Recent processing status
- Clear link to player details

### 11.3 Match explorer

Include:

- Match metadata
- Team filters
- Player list
- Sort by workload, score, distance, sprints, or quality
- Search
- Period selector
- Team summary
- Data-quality panel
- Player comparison selection

### 11.4 Player analysis page

Include:

- Player name/identifier, team, position and playing time
- Performance-risk score
- Category and confidence
- Explanation factors
- Disclaimer
- Total distance
- Distance per minute
- Average and maximum speed
- Sprint count and sprint distance
- Recovery interval
- Movement heatmap
- Speed timeline
- Fifteen-minute workload comparison
- First-half versus second-half comparison
- Event-performance panel when supported
- Baseline comparison
- Data-quality panel
- Missing-data notice

### 11.5 Player comparison page

Compare two to four players using:

- Key metric table
- Normalized workload comparison
- Window-by-window comparison
- Risk factors
- Baseline and confidence
- Position warning when comparing unlike roles

### 11.6 Methodology page

Explain:

- Data sources
- Coordinate processing
- Distance and speed calculation
- Sprint definition
- Window calculation
- Baseline selection
- Risk-score factors
- Anomaly detection
- Confidence
- Limitations
- Ethical disclaimer

### 11.7 Data management page

Include:

- Load deterministic demo dataset
- Upload supported files
- Validation results
- Processing progress
- Dataset source
- Synthetic/real label
- Delete local demo/import record if backend supports it safely

### 11.8 About page

Include:

- Project purpose
- Technology stack
- Portfolio skills demonstrated
- Dataset acknowledgements
- Source-code link placeholder
- Medical/non-diagnostic disclaimer

## Required frontend routes

Use routes similar to:

- `/` - landing and demo introduction
- `/dashboard` - team and match overview
- `/matches` - match list
- `/matches/:matchId` - match explorer
- `/matches/:matchId/players/:playerId` - player analysis
- `/matches/:matchId/compare` - player comparison
- `/data` - demo loading and local import management
- `/methodology` - methodology and model explanation
- `/about` - project, technology and attribution
- `*` - accessible not-found page

## Design identity

- Create an original PlayerPulse wordmark and simple abstract SVG mark combining a football-pitch line and pulse concept. Do not copy a club, league, tournament, provider, or commercial app logo.
- Use CSS variables and support light and dark modes.
- Use neutral slate surfaces with a restrained pitch-green/teal primary accent.
- Use risk colors only as supporting cues and always include text labels and icons.
- Meet WCAG AA contrast for normal text and controls where practical.
- Avoid stock player photographs and copyrighted football imagery; use original SVG pitch graphics and synthetic-data visuals.

## Frontend behavior

- Generate typed API client types from schemas or maintain strict shared types.
- Use TanStack Query for remote state.
- Provide skeleton loaders.
- Provide retry where safe.
- Cancel stale requests where practical.
- Keep filters in URL search parameters where useful.
- Use accessible form labels.
- Ensure keyboard navigation.
- Use semantic headings.
- Add visible focus states.
- Ensure charts have text summaries or accessible alternatives.
- Use meaningful tooltips and units.
- Never display “undefined,” “NaN,” raw stack traces, or unexplained null values.
- Display a visible `Synthetic demo`, `Local import`, or provider-source badge on every match page.
- Make the official dataset source and terms links accessible from the data-management, methodology, and about pages.
- Never display a third-party provider logo unless its current terms require or clearly permit that use.
- Show `Insufficient data` instead of inventing or zero-filling unsupported risk and event metrics.

---

# 12. Football pitch and visualization requirements

Implement a reusable responsive SVG pitch component.

Support:

- Standard pitch lines
- Coordinate scaling
- Heatmap/grid overlay
- Player trajectory
- Average-position marker
- Event markers
- Direction toggle where useful
- Responsive resizing
- Accessible title and description
- Empty-state message

Visualizations must show:

- Correct units
- Axis/period labels
- Legends
- Tooltips
- Source/support status
- Clear early-versus-late comparison
- No misleading 3D charts
- No truncated axes that exaggerate differences without clear indication

---

# 13. Demo-data requirements

The application must work without private credentials.

Create a deterministic demo-data generator that produces:

- Two teams
- At least 14 tracked players total
- One match with first and second halves
- Substitution examples
- Variable playing time
- Realistic coordinate continuity
- Walking, jogging, running, and sprint phases
- At least one stable player
- At least one player with gradual late-match performance decline
- At least one high-workload player
- At least one deliberately corrupted short sequence for data-quality testing
- Event records with passes, pressures, tackles, interceptions, and possession losses
- Fixed random seed
- `is_synthetic=true`

Also create a separate deterministic **feature-level synthetic training corpus** with at least 200 fictional player-match rows for optional anomaly-model development. It must not be presented as real tracking data and must not replace pipeline testing with the full demo match.

Use the single full synthetic match for:

- Local demo
- Unit fixtures
- Integration tests
- Screenshots
- Model-behavior scenarios

---

# 14. Security, privacy and production runtime

Implement a proportionate security baseline:

- Environment-based secrets and `.env.example` with safe placeholders
- Restrictive production CORS using an explicit allowlist
- `ENABLE_UPLOADS=false` by default in public production
- Suggested configurable limits: 25 MB per file, 5 files per import, maximum parsed rows, one processing job per worker, and a bounded request timeout
- Accept only documented CSV and JSON formats; do not accept ZIP archives in the MVP
- File-extension, MIME, schema, and content validation
- Filename sanitization and server-generated storage names
- Temporary-file isolation and cleanup after success or failure
- No execution of uploaded files
- No arbitrary path traversal or user-controlled output paths
- Parameterized database access through SQLAlchemy
- Input validation and bounded pagination
- Safe production errors and redacted structured logs
- Never log full uploaded rows, secrets, database URLs, or personal data
- Rate limiting for public write endpoints when the hosting platform supports it
- Database TLS/SSL in production where supported
- Dependency auditing, Dependabot/dependency review, and secret scanning where available
- Never load user-supplied pickle or Joblib artifacts
- No real athlete health, biometric, sleep, soreness, or injury data in the repository or public demo
- No personal medical inference
- Escape or safely render filenames, provider metadata, and imported text in the frontend
- No user authentication in the MVP unless it can be added safely without harming core delivery
- Document authentication, authorization, audit logging, durable job queues, object storage, retention, and team isolation as requirements for a real club deployment
- Add `SECURITY.md` and `docs/THREAT_MODEL.md`

## Public deployment architecture

Use the following portfolio deployment design:

- Frontend: Vercel or equivalent static hosting
- Backend: Render or equivalent container hosting
- Database: managed PostgreSQL such as Neon, Supabase, or the backend host's managed database
- Public demo data: deterministic synthetic data only
- Public third-party uploads: disabled by default
- Raw/interim/processed files on public hosting: treated as temporary cache, not durable storage
- Durable application records: PostgreSQL
- Local development: Docker Compose volumes for database and ignored data directories

The backend startup/release process must run database migrations before serving traffic. Configure platform health checks against `/api/v1/health` and readiness checks against `/api/v1/readiness`.

Document at least these environment variables:

- `APP_ENV`
- `APP_VERSION`
- `DATABASE_URL`
- `CORS_ALLOWED_ORIGINS`
- `ENABLE_UPLOADS`
- `MAX_UPLOAD_MB`
- `MAX_IMPORT_FILES`
- `MAX_IMPORT_ROWS`
- `PROCESSING_CONCURRENCY`
- `DATA_ROOT`
- `MODEL_ROOT`
- `LOG_LEVEL`
- `SYNTHETIC_SEED`
- analytics threshold variables or a single validated analytics-config path

The deployment must not depend on persistent local disk for the public demo. Regenerate deterministic synthetic data or persist its summaries in PostgreSQL. Do not deploy Metrica raw files or mirror StatsBomb raw files as part of the application image.

---

# 15. Testing requirements

## Backend unit tests

Test:

- Coordinate conversion
- Distance calculation
- Sampling-frequency handling
- Speed calculation
- Acceleration calculation
- Outlier detection
- Interpolation boundaries
- Halftime separation
- Sprint grouping
- Intensity-zone classification
- Match-window assignment
- Baseline selection
- Risk-factor normalization
- Risk category thresholds
- Explanation generation
- Missing event data
- Data-quality score
- Synthetic scenario behavior
- Risk threshold boundary and insufficient-data behavior
- Canonical coordinate orientation
- Event/tracking synchronization tolerance
- Source-rights registry validation

## Backend integration tests

Test:

- Demo dataset creation
- Full processing pipeline
- Database persistence
- Migrations
- API response schemas
- Not-found errors
- Invalid uploads
- Uploads disabled in production configuration
- Temporary-file cleanup
- Multi-file manifest mismatch
- Unsupported formats
- Processing-job lifecycle
- Player metrics endpoint
- Risk endpoint
- Heatmap endpoint
- Comparison endpoint

## Frontend tests

Test:

- Core page rendering
- Navigation
- Match selection
- Loading state
- Empty state
- API error state
- Risk display and disclaimer
- Metric formatting
- Player filters
- Comparison selection
- Accessible labels
- Supported/unsupported event sections
- Synthetic/local/provider source badges and source links
- Insufficient-data risk state

## End-to-end smoke test

Where practical, use Playwright or an equivalent tool to verify:

1. Open the application.
2. Load demo data.
3. Open the generated match.
4. Select a player.
5. View metrics and heatmap.
6. View risk score and explanation.
7. Compare players.
8. Open methodology page.

## Portfolio screenshot verification

Use Playwright after loading the synthetic demo to capture reproducible desktop and mobile screenshots for the README and case study. Screenshots must show the `Synthetic demo` badge, must not contain third-party raw data or protected logos, and must be regenerated after material UI changes.

## Quality targets

- Target at least 85% branch coverage for core analytics/risk modules and at least 70% statement coverage overall, without meaningless tests.
- Do not chase coverage percentage with meaningless tests.
- No failing tests at phase completion.
- No lint errors.
- No type-check errors.
- Production frontend build must succeed.
- Backend application import/startup must succeed.
- Docker Compose configuration must validate and start when Docker is available.
- CI must run fast tests with SQLite and at least one PostgreSQL integration job.
- CI must run the prohibited-dataset-file check, dependency review where available, and a broken-link check for documentation.

---

# 16. Documentation requirements

## README.md

Include:

- Project overview
- Screenshots or placeholders until screenshots are produced
- Key features
- Architecture summary
- Technology stack
- Quick start
- Docker start
- Local backend start
- Local frontend start
- Demo-data instructions
- Environment variables
- Test commands
- Data-source attribution
- Methodology summary
- Ethical limitations
- Deployment links/placeholders
- Portfolio skills demonstrated
- Code licence scope and third-party-data exclusion
- Data and model cards

## METHODOLOGY.md

Explain formulas and choices clearly enough for technical review.

Include:

- Coordinate conversion
- Euclidean distance
- Speed and acceleration
- Sampling assumptions
- Smoothing
- Sprint detection
- Window comparisons
- Baseline methods
- Factor normalization
- Risk score
- Confidence
- Anomaly model
- Validation approach

## ETHICS_AND_LIMITATIONS.md

Include:

- No medical diagnosis
- No confirmed injury prediction
- Dataset limitations
- Position and tactical-context differences
- Tracking errors
- Missing biometric data
- Public sample-data limitations
- Potential bias
- Appropriate and inappropriate uses

## DATA_DICTIONARY.md

Document every canonical and derived field, including unit and nullability.

## ARCHITECTURE.md

Include Mermaid diagrams for:

- System context
- Data processing flow
- Request flow
- Deployment

## API.md

Summarize endpoints and examples while treating generated OpenAPI as the canonical detailed reference.

## USER_GUIDE.md

Explain how a reviewer can load the demo and inspect results.

## DATA_CARD.md

Document synthetic and external data sources, intended uses, fields, coverage, known quality issues, rights status, prohibited uses, and provenance.

## MODEL_CARD.md

Document the deterministic score and optional anomaly model, intended use, non-medical scope, features, training data, minimum-data gate, evaluation approach, limitations, confidence, and versioning.

## CASE_STUDY.md

Create a portfolio-ready case study covering the problem, user need, architecture, data challenges, engineering decisions, analytics methodology, screenshots, tests, limitations, and lessons learned.

## THIRD_PARTY_NOTICES.md and SECURITY.md

Document code/data licence separation, third-party assets and dependencies that require notices, supported security-reporting guidance, and the project's security boundaries.

---

# 17. Git and commit policy

## Required volume

- Minimum 30 meaningful commits in Day 1
- Minimum 30 meaningful commits in Day 2
- Minimum 30 meaningful commits in Day 3
- Minimum 30 meaningful commits in Day 4
- Minimum 30 meaningful commits in Day 5
- Minimum 150 meaningful commits overall

## Atomicity rules

Each commit must:

- Represent one coherent improvement
- Leave the repository understandable
- Include related tests when feasible
- Avoid mixing unrelated frontend, backend, documentation, and infrastructure changes
- Use an informative message
- Avoid “misc,” “updates,” “changes,” or meaningless numbering
- Never be empty
- Never be manufactured from whitespace or file renames with no value

## Commit convention

Use Conventional Commit style:

- `chore:`
- `docs:`
- `feat(frontend):`
- `feat(backend):`
- `feat(analytics):`
- `feat(ml):`
- `fix:`
- `test:`
- `refactor:`
- `ci:`
- `build:`
- `perf:`
- `security:`

## Commit checks

Before each commit:

1. Review `git diff` and `git status`.
2. Confirm no secrets, prohibited third-party data, generated caches, or oversized files.
3. Run the smallest relevant test/lint command.
4. Stage only related files.
5. Commit with a meaningful message.

Do not attempt to include a commit's own hash inside that same commit. Instead, maintain machine-readable validation notes in `docs/PROGRESS.md` during development and run `scripts/export_commit_log.py` at each daily checkpoint to regenerate `docs/COMMIT_LOG.md` from actual Git history. The generated log must include commit hash, day/phase, message, purpose when derivable, and recorded validation notes.

Use the existing Git author configuration. If no author name or email is configured, this is a real blocker for the required commits: report it once and request the user to configure Git identity rather than inventing or impersonating an identity.

Do not push commits, force-push, create or modify remotes, publish a GitHub repository, open pull requests, create hosted releases, or deploy externally unless the user explicitly authorizes that external action. Local commits and local annotated tags are required.

Define phase commit ranges as:

- Day 1: repository start through `day-1-complete`
- Day 2: after `day-1-complete` through `day-2-complete`
- Day 3: after `day-2-complete` through `day-3-complete`
- Day 4: after `day-3-complete` through `day-4-complete`
- Day 5: after `day-4-complete` through `day-5-complete`

At the end of each day:

- Run the complete relevant quality gate.
- Confirm at least 30 valid commits were created for that phase.
- Update `docs/PROGRESS.md`.
- Regenerate and verify `docs/COMMIT_LOG.md`.
- Count meaningful commits for the phase using the checkpoint tag range.
- Create an annotated checkpoint tag:
  - `day-1-complete`
  - `day-2-complete`
  - `day-3-complete`
  - `day-4-complete`
  - `day-5-complete`
- Do not rewrite or squash the required development history unless the user explicitly requests it.

---

# 18. Five-day execution plan

Complete tasks in dependency order. Each numbered item below should normally produce one meaningful commit. A commit may include the implementation and its directly related test. Do not split a trivial change solely to create a commit.

## DAY 1 — Foundation, architecture and reproducible environment

Goal: End with a running frontend shell, running backend health API, database configuration, Docker configuration, CI skeleton, documentation foundation, and deterministic demo-data specification.

Required minimum 30 commits:

1. `chore: initialize PlayerPulse repository`
2. `docs: add product vision, ethical scope and code-data licence separation`
3. `chore: add root ignores, editor settings and runtime version files`
4. `docs: add repository AGENTS instructions`
5. `docs: add five-day implementation plan`
6. `docs: add progress and commit-log templates`
7. `docs: record initial architecture decisions`
8. `build(backend): initialize uv-managed Python project and lockfile`
9. `feat(backend): create FastAPI application factory`
10. `feat(backend): add health endpoint`
11. `feat(backend): add readiness and version endpoints`
12. `test(backend): add system endpoint tests`
13. `chore(backend): configure Ruff formatting and linting`
14. `chore(backend): configure mypy type checking`
15. `feat(backend): add typed application settings`
16. `feat(backend): add structured logging configuration`
17. `feat(backend): configure database engine and sessions`
18. `feat(backend): add initial SQLAlchemy base and timestamps`
19. `build(backend): initialize Alembic migrations`
20. `build(frontend): initialize npm-managed React TypeScript Vite app`
21. `chore(frontend): configure ESLint and Prettier`
22. `feat(frontend): add Tailwind and design tokens`
23. `feat(frontend): create responsive application shell`
24. `feat(frontend): add router and placeholder pages`
25. `feat(frontend): add typed API client foundation`
26. `test(frontend): configure Vitest and render smoke test`
27. `build: add backend and frontend Dockerfiles`
28. `build: add Docker Compose development stack`
29. `ci: add initial GitHub Actions quality workflow`
30. `docs: add setup, architecture, security and environment documentation`

Day 1 acceptance criteria:

- Backend starts and health endpoint responds.
- Frontend starts and displays the PlayerPulse shell.
- Backend and frontend tests run.
- Database connection has SQLite fallback and PostgreSQL configuration.
- Docker Compose file validates when Docker is available.
- CI workflow parses correctly.
- No secrets are committed.
- npm and Python dependency lockfiles exist.
- Code licence scope is separated from external dataset rights.
- At least 30 meaningful commits exist for Day 1.
- Tag `day-1-complete`.

## DAY 2 — Data ingestion, cleaning and football analytics

Goal: End with a tested end-to-end analytics pipeline that processes deterministic demo data and, when available, Metrica sample data into canonical Parquet features.

Required minimum 30 commits:

1. `docs(data): verify official dataset rights and add source registry`
2. `feat(data): add source registry schema and rights-status validation`
3. `feat(data): define canonical tracking and event schemas`
4. `feat(data): add deterministic synthetic match generator`
5. `test(data): validate deterministic demo generation`
6. `feat(data): add local-only Metrica tracking importer`
7. `feat(data): add Metrica event loader`
8. `feat(data): add rights-gated optional StatsBomb event adapter`
9. `feat(data): add multi-file import manifest and validation report`
10. `test(data): cover invalid and missing columns`
11. `feat(analytics): implement coordinate normalization`
12. `test(analytics): cover coordinate boundaries`
13. `feat(analytics): implement player timestamp ordering`
14. `feat(analytics): implement duplicate removal`
15. `feat(analytics): implement short-gap interpolation`
16. `test(analytics): cover interpolation and halftime boundaries`
17. `feat(analytics): implement movement-distance calculation`
18. `test(analytics): cover distance calculation scenarios`
19. `feat(analytics): implement speed calculation`
20. `feat(analytics): implement acceleration and deceleration`
21. `feat(analytics): add impossible-jump and speed-outlier detection`
22. `feat(analytics): add configurable movement smoothing`
23. `feat(analytics): implement intensity-zone classification`
24. `feat(analytics): implement robust sprint detection`
25. `test(analytics): cover sprint grouping and noise tolerance`
26. `feat(analytics): implement match-window metrics`
27. `feat(analytics): implement event-performance metrics`
28. `feat(analytics): add player and match data-quality scoring`
29. `feat(data): persist processed tracking and features as Parquet`
30. `docs(data): finalize data card, attribution, pipeline and calculation assumptions`

Day 2 acceptance criteria:

- Official source and license/terms URLs are recorded in `data/sources.yml` and `docs/DATASET_ATTRIBUTION.md`.
- Public demo and CI use deterministic synthetic data by default.
- Metrica raw files are not committed, packaged, or publicly hosted by the project unless explicit redistribution permission is verified.
- StatsBomb attribution and current license requirements are implemented wherever its data is used.
- Demo match generation is deterministic.
- Full processing pipeline completes.
- Tracking and event data use canonical schemas.
- Player distance, speed, intensity, sprint, window and event metrics are produced.
- Data-quality issues are visible rather than silently removed.
- Processed outputs are reproducible.
- Import manifests, checksums, source status and provenance are stored.
- Canonical coordinate orientation and analytical defaults are documented and tested.
- Analytics tests pass.
- At least 30 meaningful commits exist for Day 2.
- Tag `day-2-complete`.

## DAY 3 — Persistence, API, baseline, risk and machine learning

Goal: End with stored matches, players, metrics and explainable risk assessments exposed through a documented API.

Required minimum 30 commits:

1. `feat(db): add dataset-import lineage model and migration`
2. `feat(db): add team and player models with migrations`
3. `feat(db): add match model linked to dataset imports`
4. `feat(db): add player-match metrics model and migration`
5. `feat(db): add risk-assessment model and migration`
6. `feat(db): add processing-job model and migration`
7. `test(db): add migration and relationship tests`
8. `feat(backend): add repository layer for teams and players`
9. `feat(backend): add repository layer for matches`
10. `feat(backend): add repository layer for metrics and risk`
11. `feat(backend): add demo-dataset creation service`
12. `feat(backend): add match-processing orchestration service`
13. `feat(backend): add processing-job status tracking`
14. `feat(api): add dataset demo endpoint`
15. `feat(api): add secure dataset-upload endpoint`
16. `test(api): cover upload validation and limits`
17. `feat(api): add match list and detail endpoints`
18. `feat(api): add match players and team-summary endpoints`
19. `feat(api): add match data-quality endpoint`
20. `feat(api): add player profile and match-history endpoints`
21. `feat(api): add player metrics and timeline endpoints`
22. `feat(api): add player heatmap endpoint`
23. `feat(analytics): implement baseline-selection strategy`
24. `test(analytics): cover baseline fallbacks and confidence`
25. `feat(analytics): implement transparent rule-based risk score`
26. `feat(analytics): add factor-contribution explanations`
27. `test(analytics): validate risk behavior with synthetic scenarios`
28. `feat(ml): add gated reproducible Isolation Forest pipeline and model metadata`
29. `feat(api): expose risk, event and player-comparison endpoints`
30. `docs(api): finalize API guide, model card and risk limitations`

Day 3 acceptance criteria:

- Migrations run on a clean database.
- Demo data can be processed and stored using an API call.
- API returns matches, players, metrics, timelines, heatmaps, quality and risk.
- Risk response includes score, category, confidence, factors, model version and disclaimer.
- Synthetic risk scenarios and insufficient-data behavior are logical.
- Anomaly training is disabled below the minimum-data threshold.
- API and integration tests pass.
- At least 30 meaningful commits exist for Day 3.
- Tag `day-3-complete`.

## DAY 4 — Complete frontend dashboard and user experience

Goal: End with a polished application through which a reviewer can load demo data, explore a match, inspect a player, understand risk explanations and compare players.

Required minimum 30 commits:

1. `feat(frontend): implement application theme and dark mode`
2. `feat(frontend): add accessible navigation and mobile menu`
3. `feat(frontend): add global query and API error handling`
4. `feat(frontend): create reusable loading skeletons`
5. `feat(frontend): create empty and unavailable-data states`
6. `feat(frontend): build landing and demo introduction page`
7. `feat(frontend): add demo loading and dataset-source status workflow`
8. `feat(frontend): build dashboard summary cards`
9. `feat(frontend): build match selector`
10. `feat(frontend): build team intensity timeline`
11. `feat(frontend): build workload-ranking component`
12. `feat(frontend): build processing-status component`
13. `feat(frontend): build match explorer page`
14. `feat(frontend): add player search, filtering and sorting`
15. `feat(frontend): create reusable responsive SVG football pitch`
16. `feat(frontend): add movement heatmap rendering`
17. `feat(frontend): add player trajectory and average-position layers`
18. `feat(frontend): build player overview and metric cards`
19. `feat(frontend): build risk-score presentation`
20. `feat(frontend): build factor-contribution explanation panel`
21. `feat(frontend): build speed and workload timelines`
22. `feat(frontend): build fifteen-minute comparison view`
23. `feat(frontend): build first-half versus second-half view`
24. `feat(frontend): build event-performance panel`
25. `feat(frontend): build baseline and confidence panel`
26. `feat(frontend): build data-quality panel`
27. `feat(frontend): build multi-player comparison page`
28. `feat(frontend): build methodology, data rights and ethics pages`
29. `feat(frontend): build data-management and about pages`
30. `test(frontend): cover critical dashboard interactions and accessibility`

Day 4 acceptance criteria:

- Reviewer can load demo data from the UI.
- Dashboard, match explorer, player page and comparison page work against the real API.
- Heatmap and charts use actual processed values.
- Risk score is accompanied by explanation, confidence and disclaimer.
- Loading, error, empty and unsupported-data states are present.
- UI is responsive and keyboard usable.
- Source/synthetic status and official source links are visible.
- Frontend tests, lint, type check and build pass.
- At least 30 meaningful commits exist for Day 4.
- Tag `day-4-complete`.

## DAY 5 — Integration, quality, deployment and portfolio presentation

Goal: End with a fully tested, documented, containerized, deployable, portfolio-ready project.

Required minimum 30 commits:

1. `test(e2e): add demo user journey smoke test`
2. `test(integration): cover complete processing-to-dashboard flow`
3. `test(backend): expand analytics edge-case coverage`
4. `test(api): expand error and schema coverage`
5. `test(frontend): expand loading and failure-state coverage`
6. `fix(analytics): resolve findings from edge-case review`
7. `fix(api): resolve integration-review findings`
8. `fix(frontend): resolve responsive-layout findings`
9. `fix(frontend): resolve accessibility-review findings`
10. `security: harden upload limits, temporary files and path handling`
11. `security: review production upload switch, CORS, logs and environment configuration`
12. `perf(analytics): optimize repeated tracking calculations`
13. `perf(api): add safe query and response optimizations`
14. `perf(frontend): reduce unnecessary requests and rerenders`
15. `refactor: remove duplication and dead code`
16. `build: finalize production Docker images`
17. `build: finalize Docker Compose production-like configuration`
18. `ci: enforce backend lint, types and tests`
19. `ci: enforce frontend lint, tests and build`
20. `ci: add dependency, rights, prohibited-data and artifact checks`
21. `docs: finalize README quick start and feature guide`
22. `docs: finalize architecture diagrams`
23. `docs: finalize methodology and formulas`
24. `docs: finalize data dictionary and API guide`
25. `docs: finalize data card, model card, ethics and limitations`
26. `docs: finalize deployment instructions`
27. `docs: add reviewer-focused user guide`
28. `docs: add portfolio case study, verified screenshots and skills summary`
29. `chore: add release checklist and version metadata`
30. `chore: complete release, rights and Git-history audit for v1.0.0`

Day 5 acceptance criteria:

- Clean clone setup is documented and tested as far as environment permits.
- Demo-data flow works end to end.
- Backend tests pass.
- Frontend tests pass.
- Lint and type checks pass.
- Production frontend build succeeds.
- Migrations succeed.
- Docker configuration validates and starts when Docker is available.
- CI is configured.
- Documentation is complete.
- Ethical limitations and dataset-rights notices are visible.
- Production uploads are disabled by default and the public demo uses synthetic data only.
- Data card, model card, case study, security file and third-party notices are complete.
- At least 30 meaningful commits exist for Day 5.
- Tag `day-5-complete`.
- Create final tag `v1.0.0`.

---

# 19. Quality-gate commands

Create a `Makefile` or equivalent scripts so these commands are easy and documented.

Expected logical commands:

```bash
make setup
make dev
make backend-dev
make frontend-dev
make format
make lint
make typecheck
make test
make test-backend
make test-frontend
make build
make migrate
make demo-data
make process-demo
make docker-up
make docker-down
make ci
make verify-rights
make verify-release
make export-commit-log
```

Adapt commands for Windows compatibility through npm scripts, Python commands, or documented PowerShell alternatives.

At the end of every day run, where supported:

```bash
git status
git log --oneline --decorate -n 60
make format
make lint
make typecheck
make test
make build
```

For Day 2 onward also run the demo processing pipeline.

For Day 3 onward run migrations and API integration tests.

For Day 4 onward run the complete demo user flow.

---

# 20. Progress persistence and context recovery

Codex may reach a context, session, or usage boundary. Therefore, after every substantial task:

Update `docs/PROGRESS.md` with:

- Current day and task number
- Completed work
- Current branch
- Latest commit hash
- Tests last run and results
- Known failures
- Current blockers
- Next exact task
- Important implementation notes

Store task-level validation notes in `docs/PROGRESS.md`. Regenerate `docs/COMMIT_LOG.md` from real Git history at each daily checkpoint using `scripts/export_commit_log.py`; do not manually invent hashes or edit history to match the log.

Update `docs/DECISIONS.md` whenever an architectural, methodological, rights, security, or deployment decision is made.

Never rely only on chat history for project state.

## Resume protocol

Whenever work resumes:

1. Read `AGENTS.md`.
2. Read `docs/IMPLEMENTATION_PLAN.md`.
3. Read `docs/PROGRESS.md`.
4. Read recent commits.
5. Inspect Git status and uncommitted changes.
6. Run the smallest useful health check.
7. Continue from the exact recorded next task.
8. Do not repeat completed work.
9. Preserve uncommitted user changes.

Use this continuation instruction when a new Codex session is needed:

> Resume the PlayerPulse build from the repository state. Read `AGENTS.md`, `docs/IMPLEMENTATION_PLAN.md`, `docs/PROGRESS.md`, `docs/COMMIT_LOG.md`, and recent Git history first. Verify the working tree and run the smallest relevant checks. Continue from the exact next unfinished task. Preserve existing work, follow the ethical terminology, maintain meaningful atomic commits, and update progress files after each substantial task. Do not restart the project or duplicate completed work.

---

# 21. Final acceptance checklist

Do not declare the project complete until all applicable items are verified.

## Product

- [ ] Demo data loads without private credentials.
- [ ] Matches and players can be explored.
- [ ] Movement metrics are calculated.
- [ ] Sprint metrics are calculated.
- [ ] Fifteen-minute windows are available.
- [ ] Heatmap uses real processed coordinates.
- [ ] Event metrics clearly indicate whether they are supported.
- [ ] Baseline type and confidence are visible.
- [ ] Risk score is explainable.
- [ ] Risk wording is non-medical.
- [ ] Disclaimer is visible.

## Engineering

- [ ] Frontend is React + TypeScript.
- [ ] Backend is FastAPI + Python.
- [ ] PostgreSQL configuration exists.
- [ ] SQLite demo fallback works.
- [ ] Alembic migrations work.
- [ ] Parquet processed-data flow works.
- [ ] API schemas are typed.
- [ ] Error handling is consistent.
- [ ] No secrets are committed.
- [ ] No large raw dataset is committed.
- [ ] Docker files are present.
- [ ] CI is present.
- [ ] npm and Python dependency lockfiles are committed.
- [ ] Public production uploads default to disabled.
- [ ] Public deployment does not rely on persistent local disk.
- [ ] Dataset import provenance and checksums are stored.

## Quality

- [ ] Backend tests pass.
- [ ] Frontend tests pass.
- [ ] End-to-end smoke flow passes where supported.
- [ ] Lint passes.
- [ ] Type checking passes.
- [ ] Production build passes.
- [ ] Accessibility review completed.
- [ ] Security review completed.
- [ ] Data-quality behavior tested.
- [ ] Synthetic scenario behavior documented.
- [ ] Insufficient-data behavior tested.
- [ ] Minimum-data gate prevents unsupported anomaly-model training.
- [ ] PostgreSQL integration job passes.
- [ ] Prohibited third-party data check passes.

## Documentation

- [ ] README is complete.
- [ ] Architecture is documented.
- [ ] API is documented.
- [ ] Data dictionary is complete.
- [ ] Methodology is complete.
- [ ] Dataset attribution is complete.
- [ ] Exact official source and license/terms URLs are recorded and resolve to the official Metrica Sports and Hudl StatsBomb repositories at release time.
- [ ] External dataset rights were re-checked before release.
- [ ] No third-party raw dataset is redistributed without verified permission.
- [ ] Public demo works entirely with clearly labelled synthetic data.
- [ ] Ethics and limitations are complete.
- [ ] Deployment guide is complete.
- [ ] User guide is complete.
- [ ] Portfolio case study is included.
- [ ] Data card and model card are complete.
- [ ] Code licence and dataset terms are clearly separated.
- [ ] Third-party notices and security guidance are complete.
- [ ] Verified screenshots are included and use synthetic data unless external publication rights were re-checked.

## Git

- [ ] Day 1 has at least 30 meaningful commits.
- [ ] Day 2 has at least 30 meaningful commits.
- [ ] Day 3 has at least 30 meaningful commits.
- [ ] Day 4 has at least 30 meaningful commits.
- [ ] Day 5 has at least 30 meaningful commits.
- [ ] At least 150 meaningful commits exist overall.
- [ ] Commit history contains no fake or empty padding commits.
- [ ] Daily checkpoint tags exist.
- [ ] `v1.0.0` tag exists.
- [ ] Working tree is clean.
- [ ] Commit log was generated from real Git history.
- [ ] No remote push or public release was performed without explicit user authorization.

---

# 22. Final report format

At the end of each day, report:

1. Day completed
2. Features completed
3. Key files added or changed
4. Tests and checks run, with actual results
5. Commit count for that day
6. Latest commit hash
7. Known limitations
8. Exact next task

At final completion, report:

1. Product summary
2. Architecture summary
3. Analytics methodology summary
4. Risk-model limitations
5. Test results
6. Deployment status
7. Demo instructions
8. Total commit count
9. Daily commit counts
10. Tags created
11. Remaining optional improvements
12. Exact commands to run locally

Do not state that deployment is live unless a real deployment URL was created and verified. Preparing deployment files is required, but performing an external deployment requires explicit user authorization and available credentials.

---

# 23. Start now

Begin by:

1. Inspecting the environment and repository.
2. Creating or updating the Git repository safely.
3. Creating `AGENTS.md`.
4. Creating the implementation, progress, decision and commit-log documents.
5. Verifying Git identity, dependency tools, and official dataset source/terms pages without downloading third-party raw data.
6. Recording the initial architecture, licence boundaries and dataset-rights decisions.
7. Starting Day 1 Task 1.
8. Continuing through the plan autonomously while preserving tests, documentation and meaningful Git history.

Do not merely describe the implementation. Create the files, run the commands, test the work, make the commits, and maintain the progress records.
