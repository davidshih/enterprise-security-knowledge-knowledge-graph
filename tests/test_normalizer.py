import unittest

from security_graph.normalizer import normalize_records


def evidence(record_id: str) -> dict[str, str]:
    return {
        "source_system": "test-source",
        "source_record_id": record_id,
        "observed_at": "2026-07-10T12:00:00Z",
    }


class NormalizerTests(unittest.TestCase):
    def test_normalizes_entities_and_relationships(self) -> None:
        records = [
            {
                "record_type": "entity",
                "entity_type": "AwsAccount",
                "natural_key": "123",
                "properties": {"name": "Payments"},
                "evidence": evidence("account/123"),
            },
            {
                "record_type": "entity",
                "entity_type": "Workload",
                "natural_key": "payments-api",
                "properties": {},
                "evidence": evidence("workload/payments-api"),
            },
            {
                "record_type": "relationship",
                "relationship_type": "HOSTS",
                "source_type": "AwsAccount",
                "source_natural_key": "123",
                "target_type": "Workload",
                "target_natural_key": "payments-api",
                "evidence": evidence("edge/1"),
            },
        ]
        graph = normalize_records(records)
        self.assertEqual(len(graph["entities"]), 2)
        self.assertEqual(len(graph["relationships"]), 1)

    def test_rejects_dangling_relationship(self) -> None:
        records = [
            {
                "record_type": "entity",
                "entity_type": "AwsAccount",
                "natural_key": "123",
                "properties": {},
                "evidence": evidence("account/123"),
            },
            {
                "record_type": "relationship",
                "relationship_type": "HOSTS",
                "source_type": "AwsAccount",
                "source_natural_key": "123",
                "target_type": "Workload",
                "target_natural_key": "missing",
                "evidence": evidence("edge/1"),
            },
        ]
        with self.assertRaisesRegex(ValueError, "dangling relationships"):
            normalize_records(records)


if __name__ == "__main__":
    unittest.main()
