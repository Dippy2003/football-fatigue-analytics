"""Match repository operations."""

from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Match


class MatchRepository:
    """Provider-scoped match creation and querying."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, match_id: UUID) -> Match | None:
        return self.session.get(Match, match_id)

    def list(self, *, offset: int = 0, limit: int = 50) -> list[Match]:
        return list(
            self.session.scalars(
                select(Match)
                .order_by(Match.match_date.desc(), Match.created_at.desc())
                .offset(offset)
                .limit(limit)
            )
        )

    def get_by_external_id(self, *, source: str, external_id: str) -> Match | None:
        return self.session.scalar(
            select(Match).where(
                Match.source == source, Match.external_id == external_id
            )
        )

    def create_if_absent(self, **values: Any) -> Match:
        source = str(values["source"])
        external_id = str(values["external_id"])
        existing = self.get_by_external_id(source=source, external_id=external_id)
        if existing is not None:
            return existing
        match = Match(**values)
        self.session.add(match)
        self.session.flush()
        return match
