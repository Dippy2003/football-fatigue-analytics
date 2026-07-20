# PlayerPulse backend

FastAPI application, persistence, analytics, and processing services for
PlayerPulse. Python 3.12 dependencies are managed and locked with uv.

From the repository root:

```powershell
uv sync --project backend --all-groups
uv run --project backend uvicorn app.main:app --reload
```
