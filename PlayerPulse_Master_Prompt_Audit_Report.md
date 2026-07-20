# PlayerPulse Master Prompt - Final Audit Report

**Audit date:** 2026-07-20  
**Audited file:** `PlayerPulse_Codex_Master_Prompt_FINAL_Audited.md`

## Audit result

The final master prompt is sufficiently detailed to guide Codex from an empty repository through a portfolio-ready PlayerPulse MVP. It includes the product scope, non-goals, fixed technology choices, repository structure, dataset-rights controls, data schemas, analytics formulas, risk methodology, database design, API contract, frontend routes, testing, security, deployment preparation, documentation, Git checkpoints, and continuation procedures.

The final file contains:

- Five development phases
- Exactly 30 numbered commit tasks per phase
- Exactly 150 planned meaningful commits overall
- Daily/phase acceptance criteria
- Final release acceptance checklist
- Context-recovery instructions for later Codex sessions
- Four official dataset source/terms URLs
- Balanced Markdown code fences

## Areas checked

### 1. Product and scope

Passed. The file includes:

- Product name and description
- Intended users
- Reviewer journey
- Ethical wording
- Visible non-medical disclaimer
- Clear MVP non-goals to prevent scope expansion

### 2. Technology stack

Passed. Ambiguous alternatives were removed for the main implementation:

- React, TypeScript and Vite
- Tailwind CSS and shadcn/ui
- Recharts and custom SVG pitch graphics
- TanStack Query and Axios
- Python 3.12, FastAPI and Pydantic Settings
- SQLAlchemy, Alembic, PostgreSQL and SQLite fallback
- Pandas, NumPy, SciPy and scikit-learn
- npm with `package-lock.json`
- uv with `uv.lock`
- Docker, Docker Compose and GitHub Actions

### 3. Repository structure

Passed. The structure now includes overlooked files such as:

- `THIRD_PARTY_NOTICES.md`
- `SECURITY.md`
- `CHANGELOG.md`
- `data/sources.yml`
- `DATA_CARD.md`
- `MODEL_CARD.md`
- `CASE_STUDY.md`
- `THREAT_MODEL.md`
- screenshot directory
- commit-log generation script
- prohibited-dataset-file check
- release verification script

### 4. Dataset sources and rights

Passed with deliberate restrictions.

Official sources recorded in the prompt:

- Metrica Sports sample data: `https://github.com/metrica-sports/sample-data`
- Metrica legal statement: `https://github.com/metrica-sports/sample-data#legal-stuff`
- Hudl StatsBomb Open Data: `https://github.com/hudl/open-data`
- StatsBomb licence file: `https://github.com/hudl/open-data/blob/master/LICENSE.pdf`

The prompt correctly requires:

- Terms verification before implementation and release
- Access date, commit reference and licence digest where available
- Attribution and provenance records
- No unverified redistribution
- No third-party raw data in Git, Docker images or the public demo
- Synthetic data as the public demo default
- Separate code and dataset licences
- Trademark and logo restrictions

Metrica is intentionally treated as local-import-only because its repository contains an acknowledgement request but no separate standard licence file in the repository root.

StatsBomb is intentionally marked verification-required in the example registry so Codex must read the current README and licence before enabling the adapter.

### 5. Data pipeline

Passed. The prompt specifies:

- Provider-specific multi-file manifests
- Canonical tracking and event schemas
- Canonical coordinate orientation
- Checksums and import lineage
- Validation and actionable errors
- Missing-frame handling
- Short-gap interpolation
- Period boundaries
- Outlier and impossible-jump detection
- Movement, speed, acceleration and sprint calculations
- Match windows and event metrics
- Baselines and feature tables
- Parquet and database persistence

### 6. Analytical defaults

Passed. The prompt now gives initial configurable defaults for:

- Pitch dimensions
- Interpolation duration
- Maximum credible speed
- Smoothing window
- Movement intensity zones
- Sprint threshold and duration
- Sprint-gap merging
- Event/tracking synchronization tolerance

It also states that these are portfolio engineering defaults rather than universal medical standards.

### 7. Risk methodology

Passed. The file includes:

- Explicit normalized factors
- Initial factor thresholds
- Initial weights
- Weight re-normalization rules
- Minimum feature coverage
- Insufficient-data behavior
- Separate score and confidence calculations
- Baseline confidence rules
- Full contribution storage
- Non-medical terminology
- Threshold-boundary testing

### 8. Machine learning

Passed. The file prevents unsupported training by requiring:

- Minimum 50 valid player-match rows
- Preference for at least 100 rows
- A separate synthetic feature corpus of at least 200 records
- Reproducible random seeds
- Training-data digest and feature-schema version
- No user-uploaded Joblib/pickle loading
- Rule-based fallback when ML cannot be trained
- No misleading accuracy claims without labelled ground truth

### 9. Database and API

Passed. The prompt specifies:

- UUID IDs and UTC timestamps
- Dataset import lineage
- Teams, players, matches, metrics, assessments and processing jobs
- Alembic migrations
- Versioned API routes
- Standard error response
- Pagination, filtering and sorting
- Aggregated heatmaps and downsampled timelines
- Multi-file upload contract
- Idempotent demo creation
- Job-state handling

### 10. Frontend

Passed. The prompt includes:

- Exact route map
- Landing, dashboard, match, player, comparison, data, methodology and about pages
- Original non-infringing visual identity
- Responsive SVG pitch
- Heatmaps, timelines and comparison visuals
- Loading, error, empty and unsupported states
- Source and synthetic badges
- Accessibility requirements
- Light and dark modes
- Reproducible portfolio screenshots

### 11. Security and privacy

Passed. The prompt now covers:

- Production uploads disabled by default
- File-size, file-count and row-count limits
- No ZIP uploads
- MIME, schema and content validation
- Temporary-file cleanup
- Filename and path safety
- Safe logs and errors
- Database TLS where supported
- Rate limiting where available
- Dependency and secret scanning
- No real health or biometric data
- No untrusted pickle loading
- Threat-model and security documentation

### 12. Deployment

Passed as deployment preparation.

The prompt defines:

- Vercel-style frontend hosting
- Render-style backend container hosting
- Managed PostgreSQL
- Synthetic public demo
- No dependency on persistent backend disk
- Migration-before-start process
- Health and readiness endpoints
- Required environment variables

Actual external deployment still requires the user's authorization, accounts and credentials.

### 13. Testing and quality

Passed. It covers:

- Analytics unit tests
- Risk boundary tests
- Data-rights registry tests
- API and database integration tests
- PostgreSQL CI integration
- Frontend component and accessibility tests
- Playwright end-to-end demo flow
- Screenshot verification
- Lint, formatting, types and production builds
- Dataset-file and broken-link checks

### 14. Documentation

Passed. Required documentation now includes:

- README
- Architecture
- API guide
- Data dictionary
- Data pipeline
- Dataset attribution
- Data card
- Model card
- Methodology
- Ethics and limitations
- Security and threat model
- Deployment guide
- User guide
- Portfolio case study
- Third-party notices
- Changelog

### 15. Git workflow

Passed after correction.

The previous recursive requirement to place a commit's own hash inside that same commit was removed. The final prompt now requires:

- Actual Git history as the source of truth
- Generated commit log at phase checkpoints
- Existing Git identity rather than an invented identity
- Exactly 30 planned tasks in each phase
- Annotated phase tags
- No fake, empty or whitespace-only commits
- No history rewriting
- No remote push or public release without user permission

## Remaining intentional limitations

1. Five phases and 150 meaningful commits are ambitious. Codex may need multiple sessions, but the progress and resume protocol preserves state.
2. External dataset terms can change. They must be checked again immediately before public release.
3. Public tracking/event data cannot medically validate fatigue or injury. The product must remain a performance-indicator system.
4. The optional anomaly model must remain disabled when the minimum data requirement is not met.
5. A public deployment cannot be completed without the user's hosting accounts, credentials and authorization.
6. Metrica raw files and mirrored StatsBomb datasets must not be included in the repository or public Docker image under the default policy.

## Final recommendation

Use only `PlayerPulse_Codex_Master_Prompt_FINAL_Audited.md` for the Codex build. The earlier v1, v2 and v3 files should be ignored to avoid conflicting instructions.
