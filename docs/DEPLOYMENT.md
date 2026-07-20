# Deployment preparation

Day 1 prepares, but does not perform, external deployment.

The intended portfolio topology is a static frontend host, a FastAPI container,
and managed PostgreSQL. Public demo data is deterministic synthetic data only;
third-party uploads default to disabled; local container disk is temporary.

## Container preparation

```powershell
docker compose config
docker compose up --build
```

The backend container uses Python 3.12 and uv's frozen lockfile. The frontend is
built under Node 22 and served by Nginx with SPA routing and baseline headers.
Compose waits for PostgreSQL, runs Alembic before the API, and then starts the
frontend after backend health succeeds.

Compose syntax was verified on Day 1. The Docker engine was not running, so
images and the complete container stack are implemented but not runtime-verified.

Before public deployment: configure HTTPS origins, managed database TLS,
migration-before-start, platform health/readiness checks, rate limits, secret
storage, and synthetic demo regeneration. Never deploy Metrica raw files or a
StatsBomb mirror.
