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
uv run --project backend uvicorn app.main:app --app-dir backend --reload
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

If the API is unavailable, the page shows a safe retry state. Start the backend
and choose **Try again**. If a risk result is `Insufficient data`, read its
missing-factor and data-quality explanation instead of interpreting the absent
score as low risk.

Use the moon/sun button to change theme. Keyboard users can tab to the skip
link, navigation, filters, actions, table links, and comparison checkboxes.

## Interpretation boundary

PlayerPulse provides performance-based indicators from available match data.
It is not a medical diagnostic tool and must not be used as a substitute for
qualified medical or sports-science assessment.

## Importing local provider files

Uploads are disabled by default and are not needed for the demo. In a
controlled local environment, set `ENABLE_UPLOADS=true`, restart the API, and
open the Data page. Supply a Metrica-compatible long-form tracking CSV,
optionally supply an event CSV, acknowledge your rights to use the files, and
select **Process match**. The accepted match opens automatically.

The raw multipart files are temporary; derived Parquet remains in the ignored
local data workspace. Keep provider originals outside Git and re-check
`DATASET_ATTRIBUTION.md`. StatsBomb event-only files do not contain the tracking
needed for PlayerPulse workload indicators and are not accepted by this form.
See [Local football data import](LOCAL_DATA_IMPORT.md) for exact columns,
commands, limits, and expected results.
