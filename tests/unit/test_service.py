"""Required Lab 1 additions: a real service-function test in stub mode
(not just router logic) and a pin check that both model id and prompt
version are present. Extended with one case per handle_message() branch
so the RAG and MCP-tool paths are each exercised without the HTTP layer.
"""
import json
from pathlib import Path

from services.triage.app import PIN, handle_message


def test_service_runs_in_stub_mode():
    out = handle_message({"text": "hello"}, stub=True)
    assert out["status"] == "ok"


def test_pin_has_model_and_version():
    pin = json.loads(Path("services/triage/prompts/pin.json").read_text())
    assert pin.get("model_id") and pin.get("prompt_version")


def test_handle_message_routes_logistics_through_mcp_tool():
    out = handle_message({"text": "track delivery"}, stub=True)
    assert out["intent"] == "logistics_lookup"
    assert out["tool_called"] == "check_stock"
    assert out["grounded"] is False


def test_handle_message_grounds_ors_answer():
    out = handle_message({"text": "child needs ors and fluids"}, stub=True)
    assert out["grounded"] is True
    assert "oral rehydration" in out["answer"].lower()


def test_handle_message_default_triage_is_not_grounded():
    out = handle_message({"text": "general question"}, stub=True)
    assert out["intent"] == "triage"
    assert out["grounded"] is False


def test_pin_matches_prompt_file_bytes():
    """Same drift gate Week 8's check_prompt_pin.py proves, applied to this
    capstone's own pin instead of asserting it by eye."""
    import hashlib

    prompt_path = Path("services/triage/prompts/triage_system_v1.2.0.txt")
    assert hashlib.sha256(prompt_path.read_bytes()).hexdigest() == PIN["prompt_sha256"]
