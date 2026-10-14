"""
Thin HTTP layer over the Sentinel pipeline.

Built on Flask only because this sandbox has no network access to pip
install FastAPI. The entire contract lives in sentinel/orchestrator.py's
run(payload) -> dict, so swapping this file for a FastAPI app later is a
rewrite of this one file only, not of any decision logic. See README.

Endpoints:
  POST /v1/decisions           -> run a decision request (the Decision Contract)
  GET  /v1/decisions/<audit_id>-> reconstruct a past decision from the audit trail
  GET  /v1/decision-types      -> list configured decision types (FR-012)
  GET  /healthz                -> liveness check
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request  # noqa: E402

import sentinel  # noqa: E402
from sentinel import audit, config  # noqa: E402

app = Flask(__name__)


@app.get("/healthz")
def healthz():
    return jsonify({"status": "ok"})


@app.get("/v1/decision-types")
def decision_types():
    return jsonify({"decision_types": config.list_decision_types()})


@app.post("/v1/decisions")
def create_decision():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"status": "INVALID_REQUEST", "error": {"code": "INVALID_REQUEST", "message": "Body must be valid JSON"}}), 400
    result = sentinel.run(payload)
    http_status = 200 if result["status"] not in ("INVALID_REQUEST",) else 400
    return jsonify(result), http_status


@app.get("/v1/decisions/<audit_id>")
def get_decision(audit_id):
    record = audit.reconstruct(audit_id=audit_id)
    if record is None:
        return jsonify({"error": {"code": "NOT_FOUND", "message": f"No audit record for {audit_id}"}}), 404
    return jsonify(record)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
