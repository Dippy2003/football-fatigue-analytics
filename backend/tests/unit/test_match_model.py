"""Match model tests."""

from app.db.models import Match


def test_match_links_teams_and_dataset_lineage() -> None:
    foreign_keys = {key.target_fullname for key in Match.__table__.foreign_keys}

    assert foreign_keys == {
        "teams.id",
        "dataset_imports.id",
    }
    assert not Match.__table__.columns["is_synthetic"].nullable
