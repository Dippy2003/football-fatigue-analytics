"""Tests for the dataset source registry."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from app.data.registry import SourceRegistry, UsageStatus

ROOT = Path(__file__).parents[3]


def test_repository_source_registry_is_valid() -> None:
    registry = SourceRegistry.load(ROOT / "data" / "sources.yml")

    assert registry.schema_version == 1
    assert len(registry.sources) == 3
    assert registry.get("synthetic_playerpulse").allows_import()


def test_local_only_source_requires_local_file() -> None:
    metrica = SourceRegistry.load(ROOT / "data" / "sources.yml").get(
        "metrica_sample_data"
    )

    assert metrica.usage_status is UsageStatus.LOCAL_IMPORT_ONLY
    assert not metrica.allows_import()
    assert metrica.allows_import(supplied_locally=True)


def test_verification_required_source_is_closed_by_default() -> None:
    statsbomb = SourceRegistry.load(ROOT / "data" / "sources.yml").get(
        "statsbomb_open_data"
    )

    assert not statsbomb.allows_import(supplied_locally=True)


def test_duplicate_source_ids_are_rejected() -> None:
    registry = SourceRegistry.load(ROOT / "data" / "sources.yml")
    payload = registry.model_dump(mode="json")
    payload["sources"].append(payload["sources"][0])

    with pytest.raises(ValidationError, match="source ids must be unique"):
        SourceRegistry.model_validate(payload)


def test_unknown_source_has_clear_error() -> None:
    registry = SourceRegistry.load(ROOT / "data" / "sources.yml")

    with pytest.raises(KeyError, match="unknown data source"):
        registry.get("missing")
