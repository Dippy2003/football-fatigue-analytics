"""Dataset source registry models and rights-policy checks."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator


class UsageStatus(StrEnum):
    """Supported dataset rights states."""

    PROJECT_OWNED_SYNTHETIC = "project_owned_synthetic"
    LOCAL_IMPORT_ONLY = "local_import_only"
    VERIFICATION_REQUIRED = "verification_required"
    PERMISSION_REQUIRED = "permission_required"
    DISABLED_DUE_TO_UNCLEAR_RIGHTS = "disabled_due_to_unclear_rights"


class SourceRecord(BaseModel):
    """Rights and provenance record for one data source."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=r"^[a-z0-9_]+$")
    provider: str
    repository_owner: str
    source_url: HttpUrl | None
    terms_url: HttpUrl | None
    access_date: str
    checked_ref: str | None
    verified_commit: str | None = Field(default=None, pattern=r"^[0-9a-f]{40}$")
    terms_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    terms_digest_scope: str | None = None
    usage_status: UsageStatus
    allowed_uses: str
    redistribution: str
    attribution: str
    notes: str

    @model_validator(mode="after")
    def require_external_provenance(self) -> SourceRecord:
        """Require immutable evidence for every non-synthetic source."""
        if self.usage_status is UsageStatus.PROJECT_OWNED_SYNTHETIC:
            return self
        required = (
            self.source_url,
            self.terms_url,
            self.checked_ref,
            self.verified_commit,
            self.terms_sha256,
        )
        if any(value is None for value in required):
            raise ValueError("external sources require URLs and verification evidence")
        return self

    def allows_import(self, *, supplied_locally: bool = False) -> bool:
        """Return whether the default policy permits an import."""
        if self.usage_status is UsageStatus.PROJECT_OWNED_SYNTHETIC:
            return True
        return self.usage_status is UsageStatus.LOCAL_IMPORT_ONLY and supplied_locally


class SourceRegistry(BaseModel):
    """Versioned collection of source-rights records."""

    model_config = ConfigDict(extra="forbid")

    schema_version: int = Field(ge=1)
    verified_at_utc: str
    sources: list[SourceRecord]

    @model_validator(mode="after")
    def require_unique_source_ids(self) -> SourceRegistry:
        """Reject ambiguous duplicate source identifiers."""
        identifiers = [source.id for source in self.sources]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("source ids must be unique")
        return self

    @classmethod
    def load(cls, path: Path) -> SourceRegistry:
        """Read and validate a YAML registry."""
        with path.open(encoding="utf-8") as registry_file:
            payload = yaml.safe_load(registry_file)
        return cls.model_validate(payload)

    def get(self, source_id: str) -> SourceRecord:
        """Return a source or raise a clear lookup error."""
        for source in self.sources:
            if source.id == source_id:
                return source
        raise KeyError(f"unknown data source: {source_id}")
