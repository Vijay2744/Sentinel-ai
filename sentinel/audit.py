"""
FR-010: Audit.

Append-only JSONL log. Every decision -- including failed ones -- gets an
audit record, because a technical failure must never silently disappear
(section 23). `reconstruct` lets an authorized caller replay the full
lifecycle of one request from the audit trail alone.

MVP storage is a local JSONL file for simplicity; the interface (write +
reconstruct by audit_id/request_id) is what matters and is what a real
deployment would back with an append-only store (e.g. a WORM bucket or an
audit-specific database table).
"""
from __future__ import annotations

import json
import os
import threading

from .models import AuditRecord, new_id

_LOCK = threading.Lock()
_DEFAULT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "audit_log.jsonl"
)


def _path() -> str:
    return os.environ.get("SENTINEL_AUDIT_LOG", _DEFAULT_PATH)


def write(record: AuditRecord) -> str:
    path = _path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with _LOCK:
        with open(path, "a") as f:
            f.write(json.dumps(record.to_dict(), default=str) + "\n")
    return record.audit_id


def new_audit_id() -> str:
    return new_id("AUD")


def reconstruct(audit_id: str | None = None, request_id: str | None = None) -> dict | None:
    """Find and return one audit record by audit_id or request_id.
    Returns the most recent matching record (a request_id could in theory
    be retried and re-audited -- the latest record wins)."""
    path = _path()
    if not os.path.exists(path):
        return None
    match = None
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if audit_id and rec.get("audit_id") == audit_id:
                match = rec
            elif request_id and rec.get("request_id") == request_id:
                match = rec
    return match


def list_recent(limit: int = 20) -> list[dict]:
    path = _path()
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        lines = [json.loads(l) for l in f if l.strip()]
    return lines[-limit:][::-1]
