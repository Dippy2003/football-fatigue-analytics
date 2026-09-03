# Security policy

PlayerPulse is a portfolio MVP and not a production club medical system.
Security reports should be shared privately with the repository owner; do not
include real credentials, athlete data, or exploit payloads in a public issue.

## Current safeguards

- secrets and `.env` are ignored; `.env.example` contains safe placeholders
- production uploads default to disabled
- CORS uses an explicit environment allowlist
- settings enforce bounded upload, file, row, and concurrency limits
- structured logging redacts password, token, secret, cookie, authorization,
  and database-URL shaped fields
- database access uses SQLAlchemy rather than string-built queries
- untrusted pickle and Joblib models are prohibited
- raw/interim/processed data and generated model artifacts are ignored
- CI and local checks scan for prohibited tracked data and oversized files
- container health checks and a non-root backend runtime are configured
- API responses and Nginx add anti-sniffing, framing, referrer, permissions,
  cache, and content-security controls
- production startup rejects wildcard, HTTP, localhost, and loopback CORS
- uploads stream through bounded memory and validate suffix, media type, path,
  file declaration, file count, row count, canonical schema, coordinate bounds,
  match identity, team membership, and configured size
- accepted raw upload files use temporary storage and are deleted after
  processing; derived Parquet stays in a Git-ignored local workspace
- CI audits Python packages, critical production npm issues, tracked secrets,
  dataset distribution, migrations, browsers, and container configuration

## Supported version

Security fixes are maintained on the current `1.x` release line. Older
development checkpoints are historical and unsupported.

## Reporting

Send a private report to the repository owner with the affected version,
reproduction conditions, impact, and suggested mitigation. Do not include
credentials, real athlete information, provider raw data, or destructive
payloads. Expect acknowledgement when the owner is available; this portfolio
project does not promise a commercial response SLA.

## Data and privacy boundary

The repository and public demo must never contain real athlete health,
biometric, sleep, soreness, injury, or medical data. Synthetic data is fictional
and explicitly labelled. External football data remains subject to its provider
terms and must not be redistributed by default.

## Production limitations

Authentication, authorization, rate limiting, durable audit logs, object
storage, retention policies, club tenancy, and a durable job queue are outside
the portfolio MVP. The local import workflow must not be exposed as a public
upload service until those controls and athlete-data governance exist. They are
mandatory design work before real club deployment.

Never commit a vulnerability report containing secrets.
