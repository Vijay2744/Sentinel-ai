"""
FR-005: AI reasoning.

Produces a structured recommendation -- never the final outcome (5.1, 5.2).
Two reasoners ship:

  - HeuristicReasoner: a deterministic, offline, weighted-scoring reasoner.
    This is what runs by default so the whole platform works with zero
    external services or API keys (useful for demos, tests, air-gapped
    environments).
  - LLMReasoner: a real extension point for an actual model call. It is
    NOT wired up by default -- set SENTINEL_AI_REASONER=llm and provide
    an `invoke` callable (e.g. a call to the Claude API) to use it.

Both return the same AIOutput shape, so the rest of the pipeline (decision
resolver, explainability, audit) never needs to know which one ran.
"""
from __future__ import annotations

import os
from typing import Callable, Optional

from .errors import AIServiceError
from .models import AIOutput, EvidenceItem


class Reasoner:
    def reason(self, decision_type: str, context: dict, evidence: list[EvidenceItem], ai_config: dict) -> AIOutput:
        raise NotImplementedError


class HeuristicReasoner(Reasoner):
    """Deterministic weighted-scoring reasoner.

    ai_config shape:
      {
        "weights": {"<context.field>": <float weight, positive or negative>},
        "bias": <float>,
        "thresholds": [{"max_score": <float>, "recommendation": "<label>"}, ...]  # ascending max_score
      }
    """

    def reason(self, decision_type: str, context: dict, evidence: list[EvidenceItem], ai_config: dict) -> AIOutput:
        from .rules import get_field  # local import to avoid a cycle at module load

        weights = ai_config.get("weights", {})
        score = ai_config.get("bias", 0.0)
        contributions = []
        for field_path, weight in weights.items():
            value = get_field(context, field_path)
            if isinstance(value, bool):
                value = 1.0 if value else 0.0
            if not isinstance(value, (int, float)):
                continue
            contribution = weight * value
            score += contribution
            contributions.append(f"{field_path}={value} * {weight} = {round(contribution, 3)}")

        thresholds = ai_config.get("thresholds", [])
        recommendation = ai_config.get("default_recommendation", "REVIEW")
        for t in thresholds:
            if score <= t["max_score"]:
                recommendation = t["recommendation"]
                break

        # Confidence: distance from the nearest threshold boundary, normalized.
        # Deliberately conservative -- a heuristic reasoner should not claim
        # high confidence it hasn't earned.
        boundaries = [t["max_score"] for t in thresholds] or [0.0]
        nearest_gap = min(abs(score - b) for b in boundaries)
        confidence = max(0.5, min(0.95, 0.5 + nearest_gap / (abs(score) + nearest_gap + 1e-6) * 0.45))

        summary = (
            f"Weighted score {round(score, 3)} over {len(contributions)} factor(s); "
            f"{len(evidence)} evidence item(s) considered."
        )
        return AIOutput(
            recommendation=recommendation,
            confidence=round(confidence, 3),
            reasoning_summary=summary,
            evidence_ids=[f"{e.source}#{e.section}" for e in evidence],
            model="heuristic-reasoner-v1",
        )


class LLMReasoner(Reasoner):
    """Real-model extension point. Not used unless explicitly configured --
    this sandbox has no network access, so wiring a live call here will
    simply fail with AIServiceError until you deploy this in an environment
    that can reach an LLM API. See README for how to plug in the Claude API.
    """

    def __init__(self, invoke: Optional[Callable[[str], str]] = None):
        self.invoke = invoke

    def reason(self, decision_type: str, context: dict, evidence: list[EvidenceItem], ai_config: dict) -> AIOutput:
        if self.invoke is None:
            raise AIServiceError(
                "LLMReasoner is not configured with an `invoke` callable. "
                "See README.md for wiring this to the Claude API."
            )
        prompt = ai_config.get("prompt_template", "{context}\n\nEvidence:\n{evidence}").format(
            context=context, evidence="\n".join(e.content for e in evidence)
        )
        try:
            raw = self.invoke(prompt)
        except Exception as e:  # noqa: BLE001 -- any transport failure becomes AI_SERVICE_ERROR
            raise AIServiceError(f"LLM call failed: {e}") from e
        # Expect the model to return STRICT JSON matching AIOutput's fields.
        import json

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as e:
            raise AIServiceError("LLM did not return valid JSON output", detail={"raw": raw[:500]}) from e
        return AIOutput(
            recommendation=parsed.get("recommendation"),
            confidence=float(parsed.get("confidence", 0.0)),
            reasoning_summary=parsed.get("reasoning_summary", ""),
            evidence_ids=[f"{e.source}#{e.section}" for e in evidence],
            model=parsed.get("model", "llm-reasoner"),
        )


def get_reasoner() -> Reasoner:
    kind = os.environ.get("SENTINEL_AI_REASONER", "heuristic")
    if kind == "heuristic":
        return HeuristicReasoner()
    if kind == "llm":
        return LLMReasoner()
    raise AIServiceError(f"Unknown SENTINEL_AI_REASONER: {kind}")
