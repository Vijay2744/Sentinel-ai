# Sentinel MVP

A working implementation of the MVP scope in the Sentinel PRD (section 9):
API gateway, request validation, orchestrator, knowledge/RAG, AI reasoning,
decision engine, policy engine, decision resolver, explainability, audit,
and human-review escalation -- as one modular package, not a microservice
sprawl, per the PRD's own instruction.

## Why this stack

Built with the **Python standard library only** for the core pipeline
(`sentinel/`), plus **Flask** for the thin HTTP layer (`api/`) -- Flask was
already available in this sandbox, which has no network access to install
anything else. Nothing here is Flask-specific except `api/app.py` itself:
every route is a two-line wrapper around `sentinel.run(payload) -> dict`.
Swapping to FastAPI (or anything else) later means rewriting that one file,
not the decision logic.

The RAG layer uses lexical (token-overlap) retrieval, not embeddings, for
the same reason -- zero external services, zero API keys, runs anywhere.
`sentinel/knowledge.py` documents exactly where to swap in a real vector
store. The AI reasoning layer ships a deterministic heuristic reasoner by
default and a real LLM extension point (`LLMReasoner` in
`sentinel/ai_reasoning.py`) that you wire up to the Claude API (or any
model) once this runs somewhere with network access.

## Run it

```bash
# End-to-end demo: 4 scenarios (clean approval, policy override, escalation, invalid request)
python3 run_demo.py

# Unit tests (11 tests, no external dependencies)
python3 -m unittest discover -s tests -v

# HTTP API
python3 api/app.py          # listens on :8080 (set PORT to change)
curl -X POST localhost:8080/v1/decisions -H "Content-Type: application/json" -d '{
  "decision_type": "loan_against_securities",
  "context": {
    "applicant_id": "APP-1001", "portfolio_value": 2000000, "requested_amount": 800000,
    "ltv_requested": 0.4, "kyc_status": "VERIFIED", "asset_class": "mutual_fund_units",
    "existing_exposure": 200000, "credit_score": 760, "requested_amount_within_limit": true
  }
}'
curl localhost:8080/v1/decision-types
curl localhost:8080/v1/decisions/<audit_id>   # reconstruct from the audit trail
```

## How it maps to the PRD

| PRD section | Module |
|---|---|
| FR-001/FR-002 Request + validation | `sentinel/gateway.py` |
| FR-003 Orchestrator | `sentinel/orchestrator.py` |
| FR-004 Knowledge/RAG | `sentinel/knowledge.py` |
| FR-005 AI reasoning | `sentinel/ai_reasoning.py` |
| FR-006 Decision engine | `sentinel/decision_engine.py` |
| FR-007 Policy engine | `sentinel/policy_engine.py` |
| FR-008 Decision resolution | `sentinel/resolver.py` |
| FR-009 Explainability | `sentinel/explainability.py` |
| FR-010 Audit | `sentinel/audit.py` |
| FR-011 Human review | `sentinel/human_review.py` |
| FR-012 Configuration | `config/decision_types/*.json`, `config/policies/*.json` |
| Section 22 Decision contract | `sentinel/models.py::DecisionResponse` |
| Section 23 Error handling | `sentinel/errors.py` |

**Resolution precedence** (`resolver.py`), matching the PRD's own worked
example in section 17: **Policy > Decision Engine > AI recommendation.**
The AI never decides on its own; a failing policy always overrides the
deterministic engine; every override is recorded with a reason.

## Adding a new decision type (FR-012, no code changes)

1. Drop a new JSON file in `config/decision_types/<name>.json` (copy
   `loan_against_securities.json` as a template: required fields, knowledge
   sources, AI weights/thresholds, decision-engine rules/thresholds,
   policies, escalation rules).
2. Add any new policies it references under `config/policies/`.
3. Add any new knowledge sources under `config/knowledge/`.
4. Call it: `{"decision_type": "<name>", "context": {...}}`.

No file under `sentinel/` needs to change. This is what section 27.8 of
the PRD ("Reuse") is testing for.

## Example domain config included

`loan_against_securities.json` is a worked example: LTV caps by asset
class, a mandatory KYC policy, a regulatory hard LTV cap, and an
AI-reasoning config whose recommendation labels intentionally share the
decision engine's vocabulary (ELIGIBLE/REVIEW/DECLINE) so a genuine
AI-vs-engine conflict is detectable rather than an artifact of two
different label sets.

## What's deliberately NOT here yet (see PRD section 28, MVP non-goals)

- No persistence beyond a local JSONL audit log and in-memory idempotency
  set -- swap `sentinel/audit.py`'s storage for a real database/WORM store
  without touching its interface.
- No auth/RBAC/tenant isolation on the API -- section 24 flags this as a
  later phase, not MVP.
- No real reviewer queue/UI for human review -- `human_review.py` decides
  *whether* to escalate; wiring an actual reviewer workflow is additive.
- No real LLM call wired by default -- see `LLMReasoner` above.
- No industry-specific product modules (Wealth/Credit/Fraud/Compliance) --
  those are config packs on top of this same core, exactly as section 29
  describes, and are a Month 2+ concern, not this skeleton.

## Next steps to merge into your repo

This package has no dependency on any file structure outside itself --
`sentinel/`, `api/`, `config/`, `tests/` can be dropped into your existing
repo as-is. The two integration points to review first: (1) swap
`api/app.py` for your framework of choice if not Flask, (2) wire
`LLMReasoner.invoke` to a real model call once deployed somewhere with
network access.
