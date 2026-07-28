# PlayerPulse data dictionary

PlayerPulse stores provider-neutral identifiers and bounded analytical summaries.
Raw tracking frames stay in ignored local workspaces and are never returned by
the public API.

## Canonical tracking observations

| Field | Type | Unit | Meaning |
|---|---|---:|---|
| `match_id` | string | — | Source-scoped match identifier |
| `period` | integer | — | Match period, currently 1 or 2 |
| `timestamp_seconds` | number | seconds | Elapsed time within the period |
| `player_id` | string | — | Source-scoped fictional or provider player ID |
| `team_id` | string | — | Source-scoped team ID |
| `x`, `y` | number/null | metres | Position on a 105 × 68 metre pitch |
| `is_interpolated` | boolean | — | Position filled within the bounded gap rule |
| `is_synthetic` | boolean | — | True for every public-demo observation |

## Canonical events

Events carry `match_id`, `period`, `timestamp_seconds`, `team_id`,
`player_id`, `event_type`, optional `outcome`, optional metre coordinates, and
`is_synthetic`. Unsupported provider fields remain absent rather than being
invented.

## Persisted entities

| Table | Purpose | Important constraints |
|---|---|---|
| `dataset_imports` | Provenance, rights snapshot, checksums, import status | Aggregate checksum is unique |
| `teams` | Source-scoped team identity | Source plus external ID is unique |
| `players` | Source-scoped player identity and role | Source plus external ID is unique |
| `matches` | Teams, competition, source, processing state | Source plus external ID is unique |
| `player_match_metrics` | One bounded workload summary per player and match | Match plus player is unique |
| `risk_assessments` | Versioned explanation, confidence, factors, limitations | No medical diagnosis fields |
| `processing_jobs` | Import/processing lifecycle and safe failure text | No raw uploaded content |

All database IDs are UUIDs. Timestamps are UTC-aware. Deleting a match removes
its dependent summaries; dataset provenance is retained according to the
configured operational policy.

## Derived metric units

- Distances: metres (`*_m`)
- Speed: metres per second (`*_mps`)
- Acceleration: metres per second squared (`*_mps2`)
- Durations: seconds (`*_seconds` or `*_s`)
- Rates and changes: percentages or explicitly named 0–1 fractions
- Performance-risk score: bounded 0–100, not a probability
- Confidence and data quality: bounded 0–1

Missing, unsupported, and insufficient values are `null` or an explicit status;
they are never silently replaced with zero.
