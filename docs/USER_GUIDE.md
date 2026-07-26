# PlayerPulse user guide

## Start locally

From the repository root in Windows PowerShell:

```powershell
$env:UV_CACHE_DIR="$PWD\.uv-cache"
$env:UV_PYTHON_INSTALL_DIR="$PWD\.uv-python"
$env:DATABASE_URL="sqlite:///$($PWD.Path.Replace('\','/'))/playerpulse-ui.db"
uv run --project backend alembic -c backend/alembic.ini upgrade head
```

Start the API and frontend in separate root terminals:

```powershell
uv run --project backend uvicorn app.main:app --reload
```

```powershell
npm.cmd --prefix frontend run dev
```

Open `http://localhost:5173`.

## Reviewer journey

1. Select **Load demo match** on the home or data page.
2. Review the synthetic-source badge and match team/player summary.
3. Search, filter, or sort the player table.
4. Open a player to inspect workload, heatmap, speed, baseline, quality,
   performance-risk score, confidence, factors, and limitations.
5. Return to the match and choose **Compare players**.
6. Select two to four fictional players and review the role warning.
7. Read Methodology and Ethics before interpreting indicators.

Use the moon/sun button to change theme. Keyboard users can tab to the skip
link, navigation, filters, actions, table links, and comparison checkboxes.

## Interpretation boundary

PlayerPulse provides performance-based indicators from available match data.
It is not a medical diagnostic tool and must not be used as a substitute for
qualified medical or sports-science assessment.
