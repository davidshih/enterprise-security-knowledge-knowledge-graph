"""Contract implemented by every source-system collector."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Protocol


class SourceAdapter(Protocol):
    name: str

    def collect(self, checkpoint: str | None = None) -> Iterable[dict[str, Any]]:
        """Yield source-neutral records and support incremental collection."""
        ...
