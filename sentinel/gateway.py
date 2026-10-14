"""
FR-001 (decision request) + FR-002 (request validation).
Invalid requests are rejected before any decision execution begins.
"""
from __future__ import annotations

from . import config
from .errors import InvalidRequestError
from .models import DecisionRequest
from .rules import required_fields_present

_seen_idempotency_keys: set[str] = set()  # in-memory for MVP; use a store in production


def parse_request(payload: dict) -> DecisionRequest:
    if not isinstance(payload, dict):
        raise InvalidRequestError("Request body must be a JSON object")

    decision_type = payload.get("decision_type")
    if not decision_type or not isinstance(decision_type, str):
        raise InvalidRequestError("'decision_type' is required and must be a string")

    context = payload.get("context", {})
    if not isinstance(context, dict):
        raise InvalidRequestError("'context' must be an object")

    metadata = payload.get("metadata", {})
    if not isinstance(metadata, dict):
        raise InvalidRequestError("'metadata' must be an object")

    return DecisionRequest(
        decision_type=decision_type,
        context=context,
        metadata=metadata,
        request_id=payload.get("request_id"),
        idempotency_key=payload.get("idempotency_key"),
    )


def validate_request(req: DecisionRequest) -> config.DecisionTypeConfig:
    """Validates decision type support, required fields, and idempotency.
    Returns the loaded DecisionTypeConfig so the orchestrator doesn't load it twice.
    """
    try:
        type_config = config.load_decision_type(req.decision_type)
    except config.ConfigError as e:
        raise InvalidRequestError(
            f"Unsupported decision_type: {req.decision_type}",
            detail={"supported_types": config.list_decision_types()},
        ) from e

    missing = required_fields_present(req.context, type_config.required_context_fields)
    if missing:
        raise InvalidRequestError(
            "Missing required context fields",
            detail={"missing_fields": missing},
        )

    if req.idempotency_key:
        if req.idempotency_key in _seen_idempotency_keys:
            raise InvalidRequestError(
                "Duplicate request (idempotency_key already processed)",
                detail={"idempotency_key": req.idempotency_key},
            )
        _seen_idempotency_keys.add(req.idempotency_key)

    return type_config
