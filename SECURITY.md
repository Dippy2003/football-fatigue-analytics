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

## Data and privacy boundary

The repository and public demo must never contain real athlete health,
biometric, sleep, soreness, injury, or medical data. Synthetic data is fictional
and explicitly labelled. External football data remains subject to its provider
terms and must not be redistributed by default.

## Not yet implemented

Authentication, authorization, rate limiting, durable audit logs, object
storage, retention policies, club tenancy, and a durable job queue are outside
the five-day MVP. They are mandatory design work before real club deployment.

Supported-version and coordinated-disclosure details will be finalized for
v1.0.0. Never commit a vulnerability report containing secrets.
