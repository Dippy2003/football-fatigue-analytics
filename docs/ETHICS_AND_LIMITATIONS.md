# Ethics and limitations

> PlayerPulse provides performance-based indicators from available match data.
> It is not a medical diagnostic tool and must not be used as a substitute for
> qualified medical or sports-science assessment.

## Responsible use

PlayerPulse can help a coach or analyst decide what to review. It cannot decide
whether an athlete is fatigued, injured, fit to play, or in need of treatment.
Every score requires human interpretation alongside role, tactics, match state,
substitution, environment, recovery context, and data quality.

Do not use an indicator as the sole basis for selection, discipline, contract,
insurance, employment, medical, or return-to-play decisions. Real deployments
need athlete consultation, documented governance, role-based access, retention
limits, appeal/correction paths, and qualified clinical or sports-science
oversight.

## Known analytical limitations

- The fixed thresholds are transparent defaults, not universal physiology.
- Match-only baselines have low confidence and do not represent longitudinal
  readiness.
- Event availability varies by provider; unsupported factors remain missing.
- Tracking gaps, coordinate errors, sampling frequency, substitutions, and
  position can alter movement summaries.
- The rule score is not a probability and has no demonstrated sensitivity,
  specificity, calibration, or clinical validity.
- Isolation Forest is an optional anomaly signal; anomalous does not mean
  fatigued or injured.
- The public data is synthetic and cannot establish real-world accuracy or
  fairness.

## Fairness and privacy

Position and role affect workload, so direct rankings—especially goalkeeper
versus outfield—can mislead. Before real use, evaluate performance and error
rates across relevant roles, age groups, gender groups, competitions, devices,
and data providers with appropriately governed data.

The public repository must not contain real athlete health, sleep, soreness,
injury, biometric, or medical records. Data minimisation, purpose limitation,
access controls, deletion, and incident response are prerequisites for any club
pilot.

## Language boundary

Use `fatigue indicator`, `performance-risk score`, `workload warning`, and
`recovery review recommended`. Do not claim diagnosis, injury prediction,
treatment advice, medical clearance, or certainty.
