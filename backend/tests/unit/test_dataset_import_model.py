"""Dataset import model tests."""

from app.db.models import DatasetImport


def test_dataset_import_declares_lineage_and_rights_fields() -> None:
    columns = DatasetImport.__table__.columns

    assert columns["aggregate_checksum"].unique
    assert not columns["rights_status_snapshot"].nullable
    assert not columns["original_filename_manifest_json"].nullable
    assert not columns["is_synthetic"].nullable
