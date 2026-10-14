"""
FR-006: Decision Engine -- deterministic decision logic.

The same input and the same decision-engine config version must always
produce the same result (reproducibility, NFR section 25). There is no
randomness and no model call anywhere in this module.

Config shape (decision_type config's "decision_engine" key):
  {
    "version": "1.0",
    "rules": [
      {"id": "R1", "description": "...", "field": "a.b", "op": "<=", "value": 0.5, "weight": 40}
    ],
    "thresholds": [
      {"min_score": 70, "outcome": "ELIGIBLE"},
      {"min_score": 40, "outcome": "REVIEW"},
      {"min_score": -1e9, "outcome": "DECLINE"}
    ]
  }
Thresholds are checked in the order given -- put the highest min_score first.
"""
from __future__ import annotations

from .errors import DecisionEngineError
from .models import DecisionEngineResult
from .rules import evaluate_condition


def evaluate(context: dict, engine_config: dict) -> DecisionEngineResult:
    rules = engine_config.get("rules", [])
    thresholds = engine_config.get("thresholds", [])
    if not thresholds:
        raise DecisionEngineError("Decision engine config has no thresholds defined")

    score = 0.0
    trace = []
    for rule in rules:
        try:
            passed, detail = evaluate_condition(context, rule)
        except (KeyError, ValueError) as e:
            raise DecisionEngineError(f"Malformed rule {rule.get('id')}: {e}") from e
        weight = rule.get("weight", 0)
        contribution = weight if passed else 0
        score += contribution
        trace.append(
            {
                "rule": rule.get("id", "unnamed"),
                "description": rule.get("description", ""),
                "result": "pass" if passed else "fail",
                "detail": detail,
                "weight": weight,
                "contribution": contribution,
            }
        )

    outcome = None
    for t in thresholds:
        if score >= t["min_score"]:
            outcome = t["outcome"]
            break
    if outcome is None:
        outcome = thresholds[-1]["outcome"]

    return DecisionEngineResult(
        outcome=outcome,
        score=score,
        rule_trace=trace,
        config_version=engine_config.get("version", "unversioned"),
    )
