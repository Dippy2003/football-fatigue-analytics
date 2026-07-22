"""Clean-database migration-chain verification."""

from pathlib import Path

import pytest
from alembic.config import Config
from sqlalchemy import create_engine, inspect

from alembic import command
from app.core.config import get_settings

BACKEND_ROOT = Path(__file__).parents[2]


def test_full_migration_chain_upgrades_and_downgrades(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    database_path = tmp_path / "clean.db"
    database_url = f"sqlite:///{database_path.as_posix()}"
    monkeypatch.setenv("DATABASE_URL", database_url)
    get_settings.cache_clear()
    config = Config(str(BACKEND_ROOT / "alembic.ini"))

    command.upgrade(config, "head")
    engine = create_engine(database_url)
    tables = set(inspect(engine).get_table_names())

    assert {
        "dataset_imports",
        "teams",
        "players",
        "matches",
        "player_match_metrics",
        "risk_assessments",
        "processing_jobs",
    }.issubset(tables)

    engine.dispose()
    command.downgrade(config, "base")
    get_settings.cache_clear()
