"""
A tiny, safe condition evaluator used by both the Decision Engine and the
Policy Engine. Deliberately NOT eval()/exec() -- conditions are plain data
({"field": "...", "op": "...", "value": ...}) so they are deterministic,
reproducible, auditable, and safe to load from untrusted/external config.
"""
from __future__ import annotations

from typing import Any

_OPS = {
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
    "<": lambda a, b: a is not None and a < b,
    "<=": lambda a, b: a is not None and a <= b,
    ">": lambda a, b: a is not None and a > b,
    ">=": lambda a, b: a is not None and a >= b,
    "in": lambda a, b: a in b,
    "not_in": lambda a, b: a not in b,
    "exists": lambda a, b: a is not None,
    "not_exists": lambda a, b: a is None,
}

_MISSING = object()


def get_field(context: dict, path: str) -> Any:
    """Dot-notation lookup, e.g. 'applicant.kyc_status'. Returns None if absent."""
    cur: Any = context
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur


def evaluate_condition(context: dict, condition: dict) -> tuple[bool, str]:
    """Evaluate one condition against context. Returns (passed, detail_string)."""
    field_path = condition["field"]
    op = condition["op"]
    expected = condition.get("value")

    if op not in _OPS:
        raise ValueError(f"Unsupported operator: {op}")

    actual = get_field(context, field_path)
    try:
        passed = bool(_OPS[op](actual, expected))
    except TypeError:
        # e.g. comparing None to a number -- treat as a clean fail, not a crash
        passed = False

    detail = f"{field_path} ({actual!r}) {op} {expected!r} -> {'pass' if passed else 'fail'}"
    return passed, detail


def required_fields_present(context: dict, required: list[str]) -> list[str]:
    """Returns the list of required fields that are missing/None."""
    missing = []
    for path in required:
        if get_field(context, path) is None:
            missing.append(path)
    return missing
