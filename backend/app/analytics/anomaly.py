"""Reproducible, minimum-data-gated anomaly detection."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import UTC, datetime

import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ANOMALY_FEATURES = (
    "total_distance_m",
    "average_speed_mps",
    "max_speed_mps",
    "high_speed_distance_m",
    "sprint_count",
)
MINIMUM_TRAINING_ROWS = 50


@dataclass(frozen=True)
class AnomalyTrainingResult:
    """Training status, trusted in-memory pipeline, and reproducibility metadata."""

    status: str
    pipeline: Pipeline | None
    metadata: dict[str, object]


def generate_synthetic_feature_corpus(
    *, seed: int = 20_260_720, rows: int = 200
) -> pd.DataFrame:
    """Create fictional feature-level history independent of the demo match."""
    rng = np.random.default_rng(seed)
    distance = rng.normal(9_500, 900, rows).clip(5_000, 13_000)
    average_speed = rng.normal(2.0, 0.25, rows).clip(1.1, 3.2)
    return pd.DataFrame(
        {
            "total_distance_m": distance,
            "average_speed_mps": average_speed,
            "max_speed_mps": rng.normal(8.2, 0.7, rows).clip(5.5, 11.5),
            "high_speed_distance_m": rng.normal(650, 180, rows).clip(100, 1_300),
            "sprint_count": rng.poisson(18, rows),
        }
    )


def train_isolation_forest(
    features: pd.DataFrame, *, random_state: int = 20_260_720
) -> AnomalyTrainingResult:
    """Train only with sufficient valid rows and return inspectable metadata."""
    missing = sorted(set(ANOMALY_FEATURES) - set(features.columns))
    if missing:
        raise ValueError(f"missing anomaly features: {', '.join(missing)}")
    clean = features.loc[:, ANOMALY_FEATURES].dropna()
    hashed_rows = pd.util.hash_pandas_object(clean, index=True).to_numpy(
        dtype=np.uint64
    )
    digest = hashlib.sha256(hashed_rows.tobytes()).hexdigest()
    metadata: dict[str, object] = {
        "feature_schema_version": "anomaly-features-v1",
        "features": list(ANOMALY_FEATURES),
        "valid_rows": len(clean),
        "minimum_rows": MINIMUM_TRAINING_ROWS,
        "random_state": random_state,
        "training_data_sha256": digest,
        "scikit_learn_version": sklearn.__version__,
    }
    if len(clean) < MINIMUM_TRAINING_ROWS:
        metadata["reason"] = "model_not_trained_insufficient_data"
        return AnomalyTrainingResult(
            status="model_not_trained_insufficient_data",
            pipeline=None,
            metadata=metadata,
        )
    pipeline = Pipeline(
        [
            ("scale", StandardScaler()),
            (
                "model",
                IsolationForest(
                    n_estimators=200,
                    contamination="auto",
                    random_state=random_state,
                    n_jobs=1,
                ),
            ),
        ]
    )
    pipeline.fit(clean)
    predictions = pipeline.predict(clean)
    metadata.update(
        {
            "trained_at_utc": datetime.now(UTC).isoformat(),
            "evaluation": {
                "training_anomaly_rate": float((predictions == -1).mean()),
                "note": (
                    "Stability inspection only; no labelled fatigue outcome exists."
                ),
            },
        }
    )
    return AnomalyTrainingResult(status="trained", pipeline=pipeline, metadata=metadata)
