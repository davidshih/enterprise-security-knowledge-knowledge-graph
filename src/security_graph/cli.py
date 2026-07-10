"""Command-line entry points for local ingestion and validation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from security_graph.normalizer import load_jsonl, normalize_records


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="security-graph")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest = subparsers.add_parser("ingest", help="Normalize and validate JSONL records")
    ingest.add_argument("--input", required=True, type=Path)
    ingest.add_argument("--output", required=True, type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "ingest":
        graph = normalize_records(load_jsonl(args.input))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(graph, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(
            f"Wrote {len(graph['entities'])} entities and "
            f"{len(graph['relationships'])} relationships to {args.output}"
        )
        return 0
    return 2
