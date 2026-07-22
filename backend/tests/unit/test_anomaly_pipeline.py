"""Anomaly pipeline gating and reproducibility tests."""

from app.analytics.anomaly import (
    ANOMALY_FEATURES,
    generate_synthetic_feature_corpus,
    train_isolation_forest,
)


def test_anomaly_training_falls_back_below_minimum_rows() -> None:
    result = train_isolation_forest(generate_synthetic_feature_corpus(rows=49))

    assert result.status == "model_not_trained_insufficient_data"
    assert result.pipeline is None
    assert result.metadata["valid_rows"] == 49


def test_anomaly_training_is_reproducible_on_fictional_corpus() -> None:
    corpus = generate_synthetic_feature_corpus(seed=42, rows=200)
    first = train_isolation_forest(corpus, random_state=42)
    second = train_isolation_forest(corpus, random_state=42)

    assert first.status == "trained"
    assert first.pipeline is not None and second.pipeline is not None
    assert first.pipeline.predict(corpus[list(ANOMALY_FEATURES)]).tolist() == (
        second.pipeline.predict(corpus[list(ANOMALY_FEATURES)]).tolist()
    )
    assert (
        first.metadata["training_data_sha256"]
        == second.metadata["training_data_sha256"]
    )
