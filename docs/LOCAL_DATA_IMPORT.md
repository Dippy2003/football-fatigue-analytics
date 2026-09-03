# Local football data import

PlayerPulse can process a rights-cleared tracking export on the operator's own
machine. This workflow is disabled by default and is not available in the
public demo.

## What the import produces

An accepted tracking file is converted from normalized coordinates to a
105 by 68 metre pitch, cleaned, quality-scored, and used to calculate distance,
speed, acceleration, intensity zones, sprints, match windows, workload
summaries, heatmaps, timelines, and available performance-risk factors.
An optional event file adds supported event summaries.

The raw upload exists only in a temporary directory while it is validated and
processed. Derived Parquet tables are stored under the Git-ignored
`data/processed/imports/` directory. Provenance, checksums, team/player
identities, match metadata, and summary metrics are stored in the configured
database.

## Enable the controlled local workflow

From the repository root in Windows PowerShell:

```powershell
Copy-Item .env.example .env
(Get-Content .env) -replace 'ENABLE_UPLOADS=false', 'ENABLE_UPLOADS=true' |
  Set-Content .env
uv run --project backend alembic -c backend/alembic.ini upgrade head
uv run --project backend uvicorn app.main:app --app-dir backend --reload
```

Start the frontend in a second repository-root terminal:

```powershell
npm.cmd --prefix frontend run dev
```

Open `http://127.0.0.1:5173/data`. The local-import form should replace the
`Disabled by server` badge.

## Try the ready-made fictional files

The Data page provides **Fictional tracking sample** and
**Fictional events sample** downloads. Download both, enter
`fictional-upload-003` as the Source match ID, select the tracking sample in the
required field and the events sample in the optional field, acknowledge the
rights statement, and select **Process match**.

These files are generated deterministically by PlayerPulse, contain 20
fictional players across two periods, and may be used for local checks,
screenshots, and tests. They contain no third-party or real-athlete data. The
blank **Tracking template** and **Events template** downloads remain available
for preparing an independently authorized dataset. Open player `home-06` after
processing to see a numeric example indicator; other players may correctly show
`Insufficient Data` when their sample factors do not meet the availability
threshold.

## Required tracking CSV

Download **Tracking template** from the Data page. The file is long-form: one
row represents one player at one frame.

| Column | Requirement |
| --- | --- |
| `match_id` | Must equal the Source match ID entered in the form |
| `period` | Match period number |
| `frame_id` | Frame number within the source export |
| `timestamp_seconds` | Seconds elapsed within the period |
| `team_id` | Stable team identifier; exactly two teams are required |
| `player_id` | Stable player identifier |
| `x`, `y` | Player position normalized from 0 to 1 |
| `ball_x`, `ball_y` | Ball position normalized from 0 to 1; may be blank |

PlayerPulse currently displays source team and player identifiers as names.
Use identifiers that are suitable for the local review context and do not
upload health records, secrets, or unnecessary personal information.

## Optional event CSV

Download **Events template** from the Data page. Required columns are
`match_id`, `event_id`, `period`, `timestamp_seconds`, `team_id`, `event_type`,
`start_x`, and `start_y`. `player_id`, `outcome`, `end_x`, and `end_y` are
optional. Coordinates are normalized from 0 to 1.

Tracking is mandatory because event-only data cannot support movement,
workload, heatmap, sprint, or speed calculations.

## Import steps

1. Enter a safe source match ID containing letters, numbers, `.`, `_`, or `-`.
2. Enter a competition or analysis-context label.
3. Choose the tracking CSV and, if available, the event CSV.
4. Confirm that you are authorized to use the files and have checked the
   provider's current terms.
5. Select **Process match**.
6. PlayerPulse validates and processes the data, then opens the imported match.
7. Select **Analyse** beside a player to inspect workload and the
   performance-risk result.

If fewer than three physical factors are available, PlayerPulse intentionally
shows `Insufficient Data` instead of issuing a numeric indicator. A full
two-period tracking export with enough valid movement and sprint observations
is needed for the rule-based score.

## Safety and limits

- Only Metrica-compatible long-form CSV is accepted by this workflow.
- StatsBomb Open Data is event-only in PlayerPulse and is not accepted through
  this tracking import form.
- File count, filename, media type, byte size, combined row count, schema,
  coordinate bounds, match identity, team count, and source rights are checked.
- ZIP, JSON, pickle, Joblib, executable, path-like, and undeclared files are
  rejected.
- Repeating the same import is idempotent. Reusing a source match ID with
  different content is rejected.
- This local portfolio workflow has no authentication, tenancy, rate limiting,
  durable audit log, or organization privacy controls. Do not expose it as a
  public upload service.

PlayerPulse provides performance-based indicators from available match data.
It is not a medical diagnostic tool and must not be used as a substitute for
qualified medical or sports-science assessment.
