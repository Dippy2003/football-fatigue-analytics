# PlayerPulse API

Generated OpenAPI at `/docs` is the detailed canonical reference. Day 1 exposes
only operational routes under `/api/v1`.

| Method | Route | Purpose | Verified response |
| --- | --- | --- | --- |
| GET | `/api/v1/health` | Process liveness | `{"status":"ok"}` |
| GET | `/api/v1/readiness` | Current dependency readiness | `{"status":"ready","checks":{"application":"ok"}}` |
| GET | `/api/v1/version` | Safe public build identity | name, version `0.1.0`, API version `v1` |

The OpenAPI document is available at `/api/v1/openapi.json`; Swagger UI is at
`/docs` and ReDoc is at `/redoc`.

Readiness currently covers the application process only. Database readiness is
added with persisted domain models and migrations in Day 3. No match, player,
upload, processing, metric, heatmap, comparison, or risk endpoint is claimed on
Day 1.
