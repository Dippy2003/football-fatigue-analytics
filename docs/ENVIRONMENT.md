# Environment configuration

Settings are defined and validated in `backend/app/core/config.py`. Copy
`.env.example` to ignored `.env` for local overrides.

| Variable | Safe default | Purpose |
| --- | --- | --- |
| `APP_ENV` | `development` | development, test, or production safeguards |
| `APP_VERSION` | `0.1.0` | public build version |
| `LOG_LEVEL` | `INFO` | structured application log threshold |
| `DATABASE_URL` | `sqlite:///./playerpulse.db` | SQLite local fallback or PostgreSQL URL |
| `CORS_ALLOWED_ORIGINS` | `["http://localhost:5173"]` | explicit browser origin allowlist |
| `ENABLE_UPLOADS` | `false` | third-party import switch |
| `MAX_UPLOAD_MB` | `25` | per-file size ceiling |
| `MAX_IMPORT_FILES` | `5` | files per manifest ceiling |
| `MAX_IMPORT_ROWS` | `2000000` | parsed row ceiling |
| `PROCESSING_CONCURRENCY` | `1` | in-process job ceiling |
| `DATA_ROOT` | `../data` | ignored data workspace |
| `MODEL_ROOT` | `../models` | trusted generated model workspace |
| `SYNTHETIC_SEED` | `20260720` | deterministic demo seed |
| `VITE_API_BASE_URL` | `http://localhost:8000/api/v1` | frontend API target at build/dev time |

PostgreSQL example:

```text
postgresql+psycopg://playerpulse:replace-me@localhost:5432/playerpulse
```

Never commit live passwords or database URLs. Production CORS must contain only
the deployed frontend origins, production uploads remain off unless explicitly
approved, and hosted database connections should require provider-supported TLS.
