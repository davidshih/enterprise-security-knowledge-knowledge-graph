"""Canonical graph records with evidence and deterministic identifiers."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any


def canonical_id(record_type: str, natural_key: str) -> str:
    """Build a stable identifier without exposing the source natural key."""
    digest = sha256(f"{record_type.lower()}|{natural_key.strip()}".encode()).hexdigest()[:24]
    return f"{record_type.lower()}:{digest}"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class Evidence:
    source_system: str
    source_record_id: str
    observed_at: str
    collected_at: str = field(default_factory=utc_now)
    collector_version: str = "0.1.0"
    source_uri: str | None = None

    def validate(self) -> None:
        if not self.source_system.strip():
            raise ValueError("evidence.source_system is required")
        if not self.source_record_id.strip():
            raise ValueError("evidence.source_record_id is required")
        datetime.fromisoformat(self.observed_at.replace("Z", "+00:00"))


@dataclass(frozen=True)
class Entity:
    entity_type: str
    natural_key: str
    properties: dict[str, Any]
    evidence: Evidence
    id: str = ""

    def __post_init__(self) -> None:
        if not self.entity_type.strip():
            raise ValueError("entity_type is required")
        if not self.natural_key.strip():
            raise ValueError("natural_key is required")
        self.evidence.validate()
        if not self.id:
            object.__setattr__(self, "id", canonical_id(self.entity_type, self.natural_key))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Relationship:
    relationship_type: str
    source_id: str
    target_id: str
    properties: dict[str, Any]
    evidence: Evidence
    id: str = ""

    def __post_init__(self) -> None:
        if not self.relationship_type.strip():
            raise ValueError("relationship_type is required")
        if not self.source_id or not self.target_id:
            raise ValueError("source_id and target_id are required")
        self.evidence.validate()
        if not self.id:
            edge_key = f"{self.source_id}|{self.target_id}"
            object.__setattr__(self, "id", canonical_id(self.relationship_type, edge_key))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
