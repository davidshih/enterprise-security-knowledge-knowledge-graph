"""Normalize source-neutral JSONL records into the canonical graph contract."""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from security_graph.models import Entity, Evidence, Relationship, canonical_id


def _evidence(raw: dict[str, Any]) -> Evidence:
    return Evidence(**raw)


def normalize_records(records: Iterable[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    entities: list[Entity] = []
    relationships: list[Relationship] = []

    for line_number, raw in enumerate(records, start=1):
        record_type = raw.get("record_type")
        try:
            if record_type == "entity":
                entities.append(
                    Entity(
                        entity_type=raw["entity_type"],
                        natural_key=raw["natural_key"],
                        properties=raw.get("properties", {}),
                        evidence=_evidence(raw["evidence"]),
                    )
                )
            elif record_type == "relationship":
                source_id = canonical_id(raw["source_type"], raw["source_natural_key"])
                target_id = canonical_id(raw["target_type"], raw["target_natural_key"])
                relationships.append(
                    Relationship(
                        relationship_type=raw["relationship_type"],
                        source_id=source_id,
                        target_id=target_id,
                        properties=raw.get("properties", {}),
                        evidence=_evidence(raw["evidence"]),
                    )
                )
            else:
                raise ValueError("record_type must be 'entity' or 'relationship'")
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"invalid record at line {line_number}: {exc}") from exc

    entity_ids = {entity.id for entity in entities}
    dangling = [
        edge.id
        for edge in relationships
        if edge.source_id not in entity_ids or edge.target_id not in entity_ids
    ]
    if dangling:
        raise ValueError(f"dangling relationships detected: {', '.join(dangling)}")

    return {
        "entities": [entity.to_dict() for entity in entities],
        "relationships": [edge.to_dict() for edge in relationships],
    }


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSON at line {line_number}: {exc.msg}") from exc
    return records
