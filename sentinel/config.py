"""
Configuration loading (FR-012).

Decision types and policies live as JSON files on disk, not in platform
code. This is what lets Sentinel support a new decision workflow (a new
industry, a new product) by adding config, not by rewriting the engine.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECISION_TYPES_DIR = os.path.join(BASE_DIR, "config", "decision_types")
POLICIES_DIR = os.path.join(BASE_DIR, "config", "policies")
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "config", "knowledge")


@dataclass
class DecisionTypeConfig:
    decision_type: str
    version: str
    required_context_fields: list
    decision_engine: dict
    policies: list
    escalation: dict
    raw: dict


class ConfigError(Exception):
    pass


def _load_json(path: str) -> dict:
    if not os.path.exists(path):
        raise ConfigError(f"Config file not found: {path}")
    with open(path, "r") as f:
        return json.load(f)


def list_decision_types() -> list[str]:
    if not os.path.isdir(DECISION_TYPES_DIR):
        return []
    return sorted(
        fn[:-5] for fn in os.listdir(DECISION_TYPES_DIR) if fn.endswith(".json")
    )


def load_decision_type(decision_type: str) -> DecisionTypeConfig:
    path = os.path.join(DECISION_TYPES_DIR, f"{decision_type}.json")
    if not os.path.exists(path):
        raise ConfigError(f"Unsupported decision type: {decision_type}")
    raw = _load_json(path)
    return DecisionTypeConfig(
        decision_type=raw["decision_type"],
        version=raw.get("version", "1.0"),
        required_context_fields=raw.get("required_context_fields", []),
        decision_engine=raw.get("decision_engine", {}),
        policies=raw.get("policies", []),
        escalation=raw.get("escalation", {}),
        raw=raw,
    )


def load_policy(policy_id: str) -> dict:
    path = os.path.join(POLICIES_DIR, f"{policy_id}.json")
    return _load_json(path)


def load_knowledge_source(name: str) -> Optional[dict]:
    path = os.path.join(KNOWLEDGE_DIR, f"{name}.json")
    if not os.path.exists(path):
        return None
    return _load_json(path)


def list_knowledge_sources() -> list[dict]:
    if not os.path.isdir(KNOWLEDGE_DIR):
        return []
    out = []
    for fn in os.listdir(KNOWLEDGE_DIR):
        if fn.endswith(".json"):
            out.append(_load_json(os.path.join(KNOWLEDGE_DIR, fn)))
    return out
