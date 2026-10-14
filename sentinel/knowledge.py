"""
FR-004: Knowledge / RAG.

MVP retrieval uses lexical (token-overlap) scoring rather than embeddings,
so the whole platform runs with zero external services or API keys. The
retrieval interface is the real contract -- swap `_score` for a vector
store call (or drop in an embeddings model) without touching callers;
every caller only ever sees EvidenceItem objects with source/version/
section/relevance_score, regardless of how the score was computed.
"""
from __future__ import annotations

import re
from typing import Optional

from . import config
from .errors import KnowledgeNotFoundError
from .models import EvidenceItem

_WORD_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> set[str]:
    return set(_WORD_RE.findall(text.lower()))


def ingest_document(source: str, version: str, raw_text: str, chunk_words: int = 120) -> dict:
    """FR-004 ingestion: extraction -> chunking. Returns a knowledge-source
    record in the same shape consumed by retrieve(), ready to be written to
    config/knowledge/<source>.json for reuse.
    """
    words = raw_text.split()
    sections = []
    for i in range(0, len(words), chunk_words):
        chunk = " ".join(words[i : i + chunk_words])
        sections.append({"section": f"chunk-{i // chunk_words + 1}", "content": chunk})
    return {"source": source, "version": version, "sections": sections}


def _score(query_tokens: set[str], content: str) -> float:
    content_tokens = _tokenize(content)
    if not content_tokens or not query_tokens:
        return 0.0
    overlap = query_tokens & content_tokens
    # Jaccard-style overlap against the query side only, so long documents
    # aren't penalized for containing lots of unrelated text.
    return round(len(overlap) / len(query_tokens), 4)


def retrieve(
    query: str,
    sources: Optional[list[str]] = None,
    top_k: int = 5,
    min_relevance: float = 0.15,
) -> list[EvidenceItem]:
    """Retrieve relevant evidence for a query, scoped to the given knowledge
    sources (or all configured sources if none given). Every item keeps its
    source, version and section so explanations and audit can cite it.
    """
    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    records = []
    if sources:
        for name in sources:
            rec = config.load_knowledge_source(name)
            if rec is None:
                raise KnowledgeNotFoundError(f"Knowledge source not configured: {name}")
            records.append(rec)
    else:
        records = config.list_knowledge_sources()

    scored: list[EvidenceItem] = []
    for rec in records:
        for sec in rec.get("sections", []):
            score = _score(query_tokens, sec.get("content", ""))
            if score >= min_relevance:
                scored.append(
                    EvidenceItem(
                        source=rec["source"],
                        version=rec.get("version", "unversioned"),
                        section=sec.get("section", ""),
                        content=sec.get("content", ""),
                        relevance_score=score,
                    )
                )

    scored.sort(key=lambda e: e.relevance_score, reverse=True)
    return scored[:top_k]
