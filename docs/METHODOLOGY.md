# PlayerPulse analytics methodology

## Scope

PlayerPulse turns football tracking and event observations into transparent
performance indicators. It does not diagnose fatigue, predict confirmed injury,
recommend treatment, or replace qualified medical or sports-science assessment.

> PlayerPulse provides performance-based indicators from available match data.
> It is not a medical diagnostic tool and must not be used as a substitute for
> qualified medical or sports-science assessment.

## Canonical coordinate and time model

All providers are converted to a 105 by 68 metre pitch. The x-axis runs from
left to right and the y-axis from top to bottom. Tracking time is seconds within
each period. Every movement calculation groups by match, period, and player, so
distance, speed, interpolation, and smoothing never cross a period boundary.

Metrica-compatible normalized coordinates are multiplied by 105 and 68.
StatsBomb's 120 by 80 event grid is scaled to the same metre model. Boundary
checks reject finite coordinates outside the pitch.

## Cleaning and quality controls

Rows are stably sorted and duplicate match-period-player-timestamp observations
keep their first value. Missing x/y observations are linearly interpolated only
when they sit between known observations in the same player and period and the
known-to-known gap is no more than 0.5 seconds. Longer and boundary gaps remain
missing and are reported. Interpolated rows are visibly marked.

Speeds above 12.5 m/s are retained but marked as physiological outliers and
excluded from trusted interpretations. The quality score combines coordinate
completeness (50%), monotonic timestamps (20%), and plausible-speed rate (30%).
It is evidence about the input, not evidence about player health.

## Movement features

Step distance uses Euclidean distance in metres between consecutive valid
observations. Speed is step distance divided by a positive time delta.
Acceleration is the change in speed divided by time; positive acceleration and
deceleration magnitude are also exposed separately. Centered rolling-median
smoothing uses the observed sampling interval and a default 0.2-second window.

Distance per active minute divides observed distance by observed duration. It
does not assume that missing time was played. Average and maximum speed use
valid observed speeds.

## Intensity zones and sprints

Speed bands are lower-bound inclusive:

| Zone | Speed |
|---|---:|
| Recovery | under 2.0 m/s |
| Low | 2.0 to under 4.0 m/s |
| Moderate | 4.0 to under 5.5 m/s |
| High | 5.5 to under 7.0 m/s |
| Sprint | 7.0 m/s and above |

A sprint is a bout at or above 7.0 m/s for at least 0.5 seconds. Gaps no longer
than 0.2 seconds may be merged. Each bout reports start/end time, duration,
distance, and peak speed. These defaults are configurable and should be adapted
only with documented sports-science rationale.

## Windows and event metrics

Movement is summarized in continuous 15-minute match windows. Period 2 begins
at match minute 45 for window assignment even though provider timestamps reset.
Event metrics count pass attempts/completions, pressures, tackles,
interceptions, and possession losses. Pass completion is unknown—not zero—when
no passes are observed.

## Synthetic demo

The public demo uses a fixed-seed fictional match with two teams, 18 players,
two periods, 10 Hz tracking, several workload profiles, supported event types,
and a short deliberate coordinate dropout. Every row is marked
`is_synthetic=true`. Synthetic patterns demonstrate software behavior and are
not validation against real athletes or competitions.
