import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sentinel  # noqa: E402

GOOD_CONTEXT = {
    "applicant_id": "APP-TEST-1",
    "portfolio_value": 2000000,
    "requested_amount": 800000,
    "ltv_requested": 0.4,
    "kyc_status": "VERIFIED",
    "asset_class": "mutual_fund_units",
    "existing_exposure": 200000,
    "credit_score": 760,
    "requested_amount_within_limit": True,
}


class TestGateway(unittest.TestCase):
    def test_missing_required_field_rejected(self):
        result = sentinel.run({"decision_type": "loan_against_securities", "context": {"applicant_id": "X"}})
        self.assertEqual(result["status"], "INVALID_REQUEST")
        self.assertIsNone(result["outcome"])
        self.assertIsNotNone(result["audit_id"])  # even failures are audited

    def test_unknown_decision_type_rejected(self):
        result = sentinel.run({"decision_type": "not_a_real_type", "context": {}})
        self.assertEqual(result["status"], "INVALID_REQUEST")

    def test_malformed_payload_rejected(self):
        result = sentinel.run({"context": {}})  # no decision_type at all
        self.assertEqual(result["status"], "INVALID_REQUEST")


class TestDecisionEngine(unittest.TestCase):
    def test_reproducibility(self):
        """Same input, same config version -> identical result, every time."""
        payload = {"decision_type": "loan_against_securities", "context": dict(GOOD_CONTEXT)}
        results = [sentinel.run(payload) for _ in range(5)]
        outcomes = {r["outcome"] for r in results}
        statuses = {r["status"] for r in results}
        self.assertEqual(len(outcomes), 1, f"Non-reproducible outcomes: {outcomes}")
        self.assertEqual(len(statuses), 1)

    def test_clean_eligible_path(self):
        payload = {"decision_type": "loan_against_securities", "context": dict(GOOD_CONTEXT)}
        result = sentinel.run(payload)
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["outcome"], "ELIGIBLE")
        self.assertEqual(result["policy_status"], "PASS")


class TestPolicyOverride(unittest.TestCase):
    def test_policy_failure_overrides_decision_engine(self):
        ctx = dict(GOOD_CONTEXT)
        ctx["kyc_status"] = "PENDING"
        result = sentinel.run({"decision_type": "loan_against_securities", "context": ctx})
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["outcome"], "DECLINE")
        self.assertEqual(result["policy_status"], "FAIL")
        overrides = result["explanation"]["overrides"]
        self.assertEqual(len(overrides), 1)
        self.assertEqual(overrides[0]["overridden_outcome"], "ELIGIBLE")
        self.assertEqual(overrides[0]["final_outcome"], "DECLINE")

    def test_hard_ltv_cap_blocks_even_strong_profile(self):
        ctx = dict(GOOD_CONTEXT)
        ctx["ltv_requested"] = 0.9  # breaches the regulatory hard cap policy
        result = sentinel.run({"decision_type": "loan_against_securities", "context": ctx})
        self.assertEqual(result["policy_status"], "FAIL")
        self.assertEqual(result["outcome"], "DECLINE")


class TestHumanReview(unittest.TestCase):
    def test_ai_vs_engine_conflict_escalates(self):
        ctx = dict(GOOD_CONTEXT)
        ctx.update({"ltv_requested": 0.55, "credit_score": 705, "existing_exposure": 300000, "requested_amount_within_limit": False})
        result = sentinel.run({"decision_type": "loan_against_securities", "context": ctx})
        self.assertEqual(result["status"], "PENDING_HUMAN_REVIEW")
        self.assertIsNone(result["outcome"])  # not finalized until reviewed
        reasons = result["explanation"]["human_intervention"]["reasons"]
        self.assertTrue(any("conflicts with" in r for r in reasons))

    def test_amount_over_auto_approve_cap_escalates(self):
        ctx = dict(GOOD_CONTEXT)
        ctx["requested_amount"] = 6000000  # over the 5,000,000 auto-approve cap
        result = sentinel.run({"decision_type": "loan_against_securities", "context": ctx})
        self.assertEqual(result["status"], "PENDING_HUMAN_REVIEW")


class TestAudit(unittest.TestCase):
    def test_every_path_is_auditable_and_reconstructable(self):
        from sentinel import audit

        payload = {"decision_type": "loan_against_securities", "context": dict(GOOD_CONTEXT)}
        result = sentinel.run(payload)
        rebuilt = audit.reconstruct(audit_id=result["audit_id"])
        self.assertIsNotNone(rebuilt)
        self.assertEqual(rebuilt["request_id"], result["request_id"])
        self.assertEqual(rebuilt["status"], result["status"])


class TestExplainability(unittest.TestCase):
    def test_explanation_is_grounded_in_execution_data(self):
        payload = {"decision_type": "loan_against_securities", "context": dict(GOOD_CONTEXT)}
        result = sentinel.run(payload)
        exp = result["explanation"]
        self.assertTrue(len(exp["rules_evaluated"]) > 0)
        self.assertTrue(len(exp["policies_evaluated"]) > 0)
        self.assertIn("decision_engine", exp["config_versions"])


if __name__ == "__main__":
    unittest.main()
