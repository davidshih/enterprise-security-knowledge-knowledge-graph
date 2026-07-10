import json
import tempfile
import unittest
from pathlib import Path

from security_graph.cli import main


class CliTests(unittest.TestCase):
    def test_ingest_writes_canonical_graph(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        input_path = project_root / "data" / "sample" / "records.jsonl"

        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "graph.json"
            exit_code = main(
                ["ingest", "--input", str(input_path), "--output", str(output_path)]
            )
            graph = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertEqual(exit_code, 0)
        self.assertEqual(len(graph["entities"]), 4)
        self.assertEqual(len(graph["relationships"]), 3)


if __name__ == "__main__":
    unittest.main()
