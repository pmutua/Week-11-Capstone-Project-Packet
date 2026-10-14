"""Gold-row router coverage over the real 300-row fixture, the pytest-visible
twin of scripts/diagnose_fixture.py's standalone check (Tuesday Lab 2's
diagnosis drill runs that script directly; this test is what fails under
pytest if a fixture row's label ever drifts from what the router returns).
"""
import json
from pathlib import Path

from agents.router import route

FIXTURE = Path("fixtures/triage_messages_sample.jsonl")


def _rows():
    return [json.loads(line) for line in FIXTURE.read_text().splitlines() if line.strip()]


def test_all_fixture_rows_agree_with_router():
    disagreements = [
        (row["id"], row["label"], route(row["text"]))
        for row in _rows()
        if route(row["text"]) != row["label"]
    ]
    assert disagreements == []


def test_gold_row_logistics_delivery():
    assert route("track delivery") == "logistics_lookup"


def test_gold_row_catalog_listing_photo():
    assert route("listing photo mismatch") == "catalog_mismatch"
