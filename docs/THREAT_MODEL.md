# Threat model

## Assets

- application availability and trustworthy analytics output
- database credentials and environment configuration
- locally supplied football files and their provenance
- generated metrics, risk explanations, and model metadata
- provider attribution and licence evidence

## Trust boundaries

1. Browser to public FastAPI API.
2. FastAPI validation to processing and persistence modules.
3. Local developer files to rights-gated import adapters.
4. Application container to PostgreSQL and ephemeral storage.
5. Repository training code to trusted model artifacts.

## Priority threats and controls

| Threat | Day 1 control | Later control |
| --- | --- | --- |
| Secret disclosure | ignored env files, redacted logs | secret scanning and deployment audit |
| Path traversal/upload abuse | uploads disabled by default, bounded settings | MIME/schema validation and isolated temporary files |
| Malicious serialized model | all user pickle/Joblib loading prohibited | trusted artifact registry and digest checks |
| SQL injection | SQLAlchemy engine/session boundary | typed repositories and API validation tests |
| Unlicensed data release | rights registry, ignored data paths, tracked-file scan | adapter gates and release re-verification |
| Misleading medical inference | mandatory non-medical scope and disclaimer | explainable factors, confidence, missing-data behavior |
| Cross-origin misuse | explicit CORS allowlist | production origin audit and rate limiting |
| Resource exhaustion | file/row/concurrency settings | enforced upload and job limits |

## Residual risk

The MVP has no authentication or multi-club isolation and is unsuitable for
sensitive operational data. In-process jobs are not durable. Local SQLite is
for development only. Tactical context and tracking errors can make a valid
calculation misleading; visible quality and confidence are product controls,
not security guarantees.
