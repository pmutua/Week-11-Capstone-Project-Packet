"""Week 11 capstone Minimum Working Product: one authenticated endpoint
that routes a message through an agent (one MCP tool call available),
grounds one answer in a small document set, and returns validated JSON
built on pinned prompt/model versions -- stub mode only, no live key.

Reuses, unmodified where possible:
  - auth.py, rate_limit.py       Week 6 Monday (secure_triage_api.py shape)
  - prompts/pin.json             Week 8 Monday pin pattern, extended with model_id
  - knowledge/ors_faq.md         Week 9 Monday corpus-pin content
  - redact.py                    Week 9 Tuesday redaction patterns, extended with email
  - agents/router.py + tools     Week 6 Thursday / Week 8 Monday logistics MCP tool

Run it:
  uvicorn services.triage.app:app --port 8080
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from services.triage.auth import check_password, create_token, current_user
from services.triage.rate_limit import check_rate_limit
from services.triage.rag import grounded_answer
from services.triage.redact import redact
from agents.router import route
from agents.tools import logistics

PIN_PATH = Path(__file__).resolve().parent / "prompts" / "pin.json"
PIN = json.loads(PIN_PATH.read_text())

app = FastAPI(title="AfyaPlus Module 4 Capstone: Triage API", version="1.0.0")


class LoginRequest(BaseModel):
    username: str
    password: str


class TriageRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1000)


class TriageResponse(BaseModel):
    status: str
    intent: str
    answer: str
    grounded: bool
    tool_called: Optional[str] = None
    model_id: str
    prompt_version: str
    handled_for: Optional[str] = None


def handle_message(payload: dict, stub: bool = True) -> dict:
    """Core routing logic, independent of the HTTP layer so tests can call
    it directly (see tests/unit/test_service.py). stub=True is the only
    mode this capstone runs in without a live model key."""
    text = payload.get("text", "")
    intent = route(text)

    tool_called = None
    if intent == "logistics_lookup":
        tool_result = logistics.lookup(text)
        tool_called = tool_result["tool"]
        rows = tool_result["result"].get("stock", [])
        answer = f"Stock for {tool_result['item']}: " + ", ".join(
            f"{r['clinic']}={r['units']}" for r in rows
        )
        grounded = False
    else:
        rag = grounded_answer(text)
        answer = rag["answer"]
        grounded = rag["grounded"]

    return {
        "status": "ok",
        "intent": intent,
        "answer": answer,
        "grounded": grounded,
        "tool_called": tool_called,
        "model_id": PIN["model_id"],
        "prompt_version": PIN["prompt_version"],
    }


@app.get("/health")
def health() -> dict:
    return {
        "service": "module4-capstone-triage",
        "status": "ok",
        "model_id": PIN["model_id"],
        "prompt_version": PIN["prompt_version"],
        "prompt_sha256": PIN["prompt_sha256"],
    }


@app.post("/token")
def login(body: LoginRequest) -> dict:
    if not check_password(body.username, body.password):
        raise HTTPException(status_code=401, detail="Wrong username or password.")
    return {"access_token": create_token(body.username), "token_type": "bearer"}


@app.post("/triage", response_model=TriageResponse)
def triage(request: TriageRequest, user: dict = Depends(current_user)) -> TriageResponse:
    check_rate_limit(user["sub"])
    # redact() runs before this text would ever reach a log line or an
    # audit record -- handle_message() itself never logs the raw text.
    _ = redact(request.text)
    result = handle_message({"text": request.text}, stub=True)
    result["handled_for"] = user["sub"]
    return TriageResponse(**result)
