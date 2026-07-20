# Testing and quality guide

## One-command Windows gate

From the repository root:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/check_day1.ps1
```

The script stops on a failed native command and covers backend format, lint,
types, tests; frontend format, lint, types, tests, production build; tracked
dataset policy; and Docker Compose configuration.

## Day 1 verified scope

- API health, readiness, version, and OpenAPI paths
- safe environment defaults and environment parsing
- log redaction for credential-shaped fields
- SQLite connection and PostgreSQL URL normalization
- UUID primary keys and UTC Python-side timestamp defaults
- frontend shell rendering, non-medical disclaimer, and client-side navigation

## Known test warning

FastAPI's current synchronous `TestClient` emits a Starlette deprecation warning
about a future `httpx2` migration. Tests pass and the warning originates in the
installed framework compatibility layer. It is not suppressed; dependency
compatibility will be revisited before release.

Day 1 does not yet have analytics, database-domain, upload, integration, or E2E
demo tests because those features are scheduled for later phases.
