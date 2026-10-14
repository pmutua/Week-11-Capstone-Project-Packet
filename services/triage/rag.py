"""Grounded lookup (RAG) over the one-file knowledge corpus this capstone
pins in prompts/pin.json (corpus_path/corpus_sha256). Deliberately a
keyword match over a single markdown file, not an embeddings index --
the corpus is one sentence, and the lesson's own fixture-scale rule (teach
with a slice, not a production system) applies to retrieval depth too.
"""
from __future__ import annotations

from pathlib import Path

KNOWLEDGE_PATH = Path(__file__).resolve().parent / "knowledge" / "ors_faq.md"
TRIGGER_WORDS = ("ors", "rehydrat", "dehydrat", "diarrhea", "diarrhoea")


def grounded_answer(text: str) -> dict:
    low = text.lower()
    if any(word in low for word in TRIGGER_WORDS):
        return {
            "grounded": True,
            "citation": "services/triage/knowledge/ors_faq.md",
            "answer": KNOWLEDGE_PATH.read_text(encoding="utf-8").strip(),
        }
    return {
        "grounded": False,
        "citation": None,
        "answer": "Rest, drink fluids, and monitor your symptoms. Seek clinic care if unsure.",
    }
