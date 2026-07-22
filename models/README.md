# PlayerPulse model artifacts

Model artifacts are ignored and must be created only by the repository's
trusted training pipeline. Never load a user-uploaded pickle or Joblib file.

The transparent rule-based indicator requires no binary artifact. The optional
Isolation Forest is trained only by repository code after at least 50 complete
feature rows; the public tests use 200 deterministic fictional records. Current
implementation returns the fitted pipeline in memory with reproducibility
metadata and does not commit a binary artifact. See `docs/MODEL_CARD.md`.
