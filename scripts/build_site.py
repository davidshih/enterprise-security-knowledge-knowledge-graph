"""Build the dependency-free GitHub Pages knowledge base."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
STATIC_ROOT = PROJECT_ROOT / "website"

KNOWLEDGE_FILES = {
    PROJECT_ROOT / "docs" / "PLAN.md": "PLAN.md",
    PROJECT_ROOT / "schema" / "graph-model.yaml": "graph-model.yaml",
    PROJECT_ROOT / "examples" / "queries.cypher": "queries.cypher",
    PROJECT_ROOT / "examples" / "openapi.yaml": "openapi.yaml",
    PROJECT_ROOT / "config" / "sources.yaml": "sources.yaml",
    PROJECT_ROOT / "config" / "risk-model.yaml": "risk-model.yaml",
    PROJECT_ROOT / "config" / "access-policy.yaml": "access-policy.yaml",
}


def build(output: Path) -> None:
    if output.exists():
        shutil.rmtree(output)

    shutil.copytree(STATIC_ROOT, output)
    knowledge_dir = output / "knowledge"
    knowledge_dir.mkdir()

    for source, destination in KNOWLEDGE_FILES.items():
        if not source.is_file():
            raise FileNotFoundError(f"knowledge source is missing: {source}")
        shutil.copy2(source, knowledge_dir / destination)

    manifest = {
        "project": "enterprise-security-knowledge-graph",
        "schema_version": 1,
        "built_at": datetime.now(timezone.utc).isoformat(),
        "knowledge_files": sorted(KNOWLEDGE_FILES.values()),
    }
    (knowledge_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    build(args.output.resolve())
    print(f"Built knowledge base at {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
