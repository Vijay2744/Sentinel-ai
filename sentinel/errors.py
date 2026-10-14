"""
Error taxonomy (PRD section 23).
A technical failure must never silently become a valid business decision --
every failure path raises one of these, which the orchestrator catches and
turns into an explicit ERROR response, never a default outcome.
"""


class SentinelError(Exception):
    code = "SYSTEM_ERROR"

    def __init__(self, message: str, detail: dict | None = None):
        super().__init__(message)
        self.message = message
        self.detail = detail or {}

    def to_dict(self) -> dict:
        return {"code": self.code, "message": self.message, "detail": self.detail}


class InvalidRequestError(SentinelError):
    code = "INVALID_REQUEST"


class KnowledgeNotFoundError(SentinelError):
    code = "KNOWLEDGE_NOT_FOUND"


class AIServiceError(SentinelError):
    code = "AI_SERVICE_ERROR"


class DecisionEngineError(SentinelError):
    code = "DECISION_ENGINE_ERROR"


class PolicyEngineError(SentinelError):
    code = "POLICY_ENGINE_ERROR"


class InsufficientEvidenceError(SentinelError):
    code = "INSUFFICIENT_EVIDENCE"


class HumanReviewRequired(SentinelError):
    """Not a failure -- a deliberate escalation signal (FR-011)."""
    code = "HUMAN_REVIEW_REQUIRED"


class SystemError(SentinelError):
    code = "SYSTEM_ERROR"
