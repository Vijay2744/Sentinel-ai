"""
Run four requests through the full Sentinel pipeline and print the
decision contract + a one-line audit confirmation for each, so you can
see all the FR-008/FR-011 paths (clean approval, policy override,
mandatory review, invalid request) in one pass.

    python3 run_demo.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sentinel  # noqa: E402
from sentinel import audit  # noqa: E402

SCENARIOS = {
    "clean_approval": {
        "decision_type": "loan_against_securities",
        "context": {
            "applicant_id": "APP-1001",
            "portfolio_value": 2000000,
            "requested_amount": 800000,
            "ltv_requested": 0.4,
            "kyc_status": "VERIFIED",
            "asset_class": "mutual_fund_units",
            "existing_exposure": 200000,
            "credit_score": 760,
            "requested_amount_within_limit": True,
        },
    },
    "policy_blocked_kyc": {
        "decision_type": "loan_against_securities",
        "context": {
            "applicant_id": "APP-1002",
            "portfolio_value": 2000000,
            "requested_amount": 800000,
            "ltv_requested": 0.4,
            "kyc_status": "PENDING",
            "asset_class": "equity_shares",
            "existing_exposure": 200000,
            "credit_score": 760,
            "requested_amount_within_limit": True,
        },
    },
    "escalated_low_confidence": {
        "decision_type": "loan_against_securities",
        "context": {
            "applicant_id": "APP-1003",
            "portfolio_value": 1000000,
            "requested_amount": 550000,
            "ltv_requested": 0.55,
            "kyc_status": "VERIFIED",
            "asset_class": "equity_shares",
            "existing_exposure": 300000,
            "credit_score": 705,
            "requested_amount_within_limit": False,
        },
    },
    "invalid_missing_field": {
        "decision_type": "loan_against_securities",
        "context": {
            "applicant_id": "APP-1004",
            "requested_amount": 100000,
        },
    },
}


def main():
    for name, payload in SCENARIOS.items():
        print(f"\n=== {name} ===")
        result = sentinel.run(payload)
        print(json.dumps(result, indent=2, default=str))
        if result.get("audit_id"):
            rebuilt = audit.reconstruct(audit_id=result["audit_id"])
            print(f"-- audit {result['audit_id']} reconstructable: {rebuilt is not None}")


if __name__ == "__main__":
    main()
