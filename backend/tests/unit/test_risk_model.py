"""Risk assessment model tests."""

from app.db.models import RiskAssessment


def test_risk_model_allows_explicit_insufficient_state() -> None:
    columns = RiskAssessment.__table__.columns

    assert columns["score"].nullable
    assert columns["category"].nullable
    assert not columns["assessment_status"].nullable
    assert not columns["explanation_json"].nullable
