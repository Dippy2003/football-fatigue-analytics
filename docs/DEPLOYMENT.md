# Deployment guide

No public deployment is implied by this repository. The supported release
artifact is a local/CI-verified container stack.

## Required production services

- Static Nginx frontend image
- FastAPI backend image
- Managed PostgreSQL 17-compatible database
- HTTPS reverse proxy/platform ingress
- Platform secret store and centralized logs

Persistent local disk must not be required. Public data is regenerated from the
deterministic synthetic source; external raw datasets are not packaged.

## Environment

Set at minimum:

```text
APP_ENV=production
APP_VERSION=1.0.0
DATABASE_URL=postgresql://...
CORS_ALLOWED_ORIGINS=["https://your-frontend.example"]
ENABLE_UPLOADS=false
LOG_LEVEL=INFO
```

Production startup rejects wildcard, HTTP, localhost, and loopback CORS
origins. Store values in the platform secret manager, not `.env` in Git.

## Container verification

From the repository root:

```powershell
docker compose config --quiet
docker compose build
docker compose up
```

Wait for all services to become healthy, then check:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/v1/health
Invoke-RestMethod http://127.0.0.1:8000/api/v1/readiness
Invoke-RestMethod http://127.0.0.1:8000/api/v1/version
```

Open http://127.0.0.1:5173 and complete the demo journey. Stop and remove the
local stack with `docker compose down`; add `-v` only when intentionally
discarding the local database volume.

## Platform release order

1. Provision PostgreSQL with encrypted connections, backups, and restricted
   network access.
2. Run `alembic upgrade head` as a one-off release task.
3. Deploy the backend and verify health/readiness/version.
4. Deploy the frontend with its API origin configured at build time.
5. Load the synthetic demo and inspect risk disclaimer/quality behavior.
6. Monitor logs, latency, error rate, database health, and resource use.
7. Roll back application images if needed; use Alembic downgrade only after
   reviewing whether the migration is safely reversible.

## Before real club use

Add authentication, authorization, tenancy, rate limiting, durable audit logs,
object storage, retention/deletion controls, privacy/legal review, incident
response, athlete governance, monitored backups, and real-world analytical
validation. Do not enable uploads or ingest real athlete health data as part of
the public portfolio deployment.
