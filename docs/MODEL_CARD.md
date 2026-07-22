# PlayerPulse indicator model card

## Intended use

The primary model is `rule-risk-v1`, a deterministic performance-risk indicator
for workload review by coaches and analysts. It is not clinically validated and
does not estimate injury probability.

> PlayerPulse provides performance-based indicators from available match data.
> It is not a medical diagnostic tool and must not be used as a substitute for
> qualified medical or sports-science assessment.

## Inputs and availability

The model supports speed decline, sprint-frequency decline, sprint-recovery
increase, workload-versus-baseline z-score, and supported event-performance
decline. Missing factors are not zero-filled. A numeric score requires at least
three physical factors, 60% feature coverage, and data quality of at least 0.50.
Otherwise the status is `insufficient_data`.

Factors use documented piecewise-linear 0–100 scaling. Available weights are
renormalized from 25%, 25%, 20%, 20%, and 10%, respectively. Confidence is
separate: 50% data quality, 35% baseline confidence, and 15% feature coverage.
Every response includes raw values, normalized factors, effective weights,
contributions, top contributors, limitations, formula version, and disclaimer.

## Validation

Tests cover stable performance, severe decline, high workload without decline,
missing core factors, low data quality, and threshold values immediately below,
at, and above boundaries. These are logical software scenarios—not clinical
accuracy, sensitivity, or specificity evidence.

## Optional anomaly signal

The optional Isolation Forest fits scaling and the estimator in one scikit-learn
Pipeline. Training is refused below 50 complete feature rows. Tests use a
separate fixed-seed corpus of 200 fictional player-match records. Metadata stores
the exact feature list, random state, training-data SHA-256, schema/library
versions, timestamp, and observed training anomaly rate. It is a separate signal
and never confirms fatigue.

No user-uploaded pickle or Joblib artifact is loaded. Binary model persistence
is reserved for trusted repository build output and remains ignored by Git.

## Limitations and alternative explanations

Tactics, score state, position, role changes, substitutions, match tempo,
opponent strength, sensor gaps, and provider coverage can explain changes. Do
not compare goalkeepers directly with outfield players without visible context.
Use the result to prompt qualified review, never treatment or selection by
itself.

