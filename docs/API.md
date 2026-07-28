# PlayerPulse API

Swagger UI at `/docs` and ReDoc at `/redoc` are the canonical interactive
references. All application routes are versioned under `/api/v1`.

## Implemented routes

| Area | Method and route | Result |
| --- | --- | --- |
| System | `GET /health`, `/readiness`, `/version` | Operational state and version |
| Data | `POST /datasets/demo` | Idempotent fictional import, match, players, metrics |
| Data | `GET /datasets/sources` | Rights status and attribution |
| Data | `GET /datasets/import-capabilities` | Upload state, provider, and configured limits |
| Data | `POST /datasets/upload` | Rights-gated local tracking processing and persistence |
| Processing | `POST /matches/{id}/process` | Queues an in-process persisted job |
| Processing | `GET /jobs/{id}` | Stage, progress, outcome, retry limitation |
| Matches | `GET /matches`, `/matches/{id}` | Stored list and detail |
| Matches | `GET /matches/{id}/players` | Player identities and summary workload |
| Matches | `GET /matches/{id}/team-summary` | Team workload aggregation |
| Matches | `GET /matches/{id}/quality` | Quality score and metric coverage |
| Players | `GET /players/{id}`, `/players/{id}/matches` | Profile and match history |
| Analytics | `GET /matches/{m}/players/{p}/metrics` | Typed feature summary |
| Analytics | `GET /matches/{m}/players/{p}/timeline` | At most about 120 points |
| Analytics | `GET /matches/{m}/players/{p}/heatmap` | Bounded 8 by 12 count grid |
| Analytics | `GET /matches/{m}/players/{p}/events` | Supported canonical events |
| Analytics | `GET /players/{id}/baseline` | Baseline type/confidence/limitations |
| Indicator | `GET /matches/{m}/players/{p}/risk` | Score or insufficient state, confidence, factors, disclaimer |
| Comparison | `GET /matches/{m}/compare-players` | Two-to-four aligned player summaries |

## Demo journey

Start with `POST /api/v1/datasets/demo`. Save the returned `match_id`, list
`/matches/{match_id}/players`, then use a returned player `id` with metrics,
timeline, heatmap, events, risk, and baseline routes. Repeating demo creation
returns the existing checksum-addressed records and `created=false`.

## Upload contract

Uploads use multipart fields `provider`, JSON-string `manifest`, and one or
more `files`. `ENABLE_UPLOADS=false` returns 403 before parsing source content.
When locally enabled, `provider` must be `metrica_sample_data`. The JSON
manifest declares a safe source match ID, competition, rights acknowledgement,
and exactly one tracking file plus an optional events file. Multipart filenames
must exactly match those declarations. Only safe-basename CSV files with
matching media types are accepted. File count, byte size, combined rows,
canonical columns, coordinate bounds, match ID, two-team membership, and
player identity are validated. ZIP, JSON, pickle, Joblib, path-like filenames,
malformed manifests, undeclared files, and over-limit files are rejected.

On success, the response contains the persisted dataset and match IDs, player
count, quality score/confidence, limitations, and idempotency state. Raw uploads
are removed with the temporary directory; derived Parquet is written to the
ignored local data workspace. Validation does not grant data rights or enable
public redistribution.

## Errors

HTTP and validation failures use:

```json
{
  "code": "http_404",
  "message": "Match not found.",
  "details": null,
  "request_id": "caller-or-generated-id",
  "timestamp": "UTC ISO-8601"
}
```

Responses echo `X-Request-ID`. Production errors do not return stack traces or
raw uploaded rows.

## Current limitations

In-process jobs are not durable workers: a server restart can require retry.
Synthetic timeline, heatmap, and event tables are regenerated deterministically
instead of stored as raw frames. Local-import timeline, heatmap, and event
responses read ignored derived Parquet. External imports remain local and
rights-gated.
