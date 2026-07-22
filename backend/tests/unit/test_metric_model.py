"""Player-match metric model tests."""

from app.db.models import PlayerMatchMetric


def test_metric_model_keeps_quality_baseline_and_support_fields() -> None:
    columns = PlayerMatchMetric.__table__.columns

    assert not columns["data_quality_score"].nullable
    assert "baseline_confidence" in columns
    assert "supported_event_metrics" in columns
    assert columns["pass_accuracy_change_pct"].nullable
