import unittest

from security_graph.models import Evidence, Entity, canonical_id
from security_graph.risk import RiskFactors, score_risk


class ModelTests(unittest.TestCase):
    def test_canonical_id_is_stable_and_hides_natural_key(self) -> None:
        first = canonical_id("AwsAccount", "123456789012")
        second = canonical_id("AwsAccount", "123456789012")
        self.assertEqual(first, second)
        self.assertNotIn("123456789012", first)

    def test_entity_requires_evidence(self) -> None:
        evidence = Evidence(
            source_system="aws-organizations",
            source_record_id="account/123",
            observed_at="2026-07-10T12:00:00Z",
        )
        entity = Entity("AwsAccount", "123", {"name": "Payments"}, evidence)
        self.assertTrue(entity.id.startswith("awsaccount:"))

    def test_risk_score_is_bounded_and_control_aware(self) -> None:
        base = RiskFactors(1.0, 0.8, 1.0, 1.0, 0.8, 0.0)
        controlled = RiskFactors(1.0, 0.8, 1.0, 1.0, 0.8, 0.8)
        self.assertGreater(score_risk(base), score_risk(controlled))
        self.assertLessEqual(score_risk(base), 100)

    def test_risk_score_rejects_invalid_factor(self) -> None:
        with self.assertRaises(ValueError):
            score_risk(RiskFactors(1.1, 0.5, 0.5, 0.5, 0.5))


if __name__ == "__main__":
    unittest.main()
