"""Stub-mode MCP tool call for the capstone agent.

Imports logistics_mcp_versioned.py (copied unchanged from
week8_monday/logistics_mcp_versioned.py) and calls its @server.tool()
functions directly as plain Python, the same precedent every other week's
MCP tests use (see tests/test_week8_monday_llmops.py in the repo root):
no MCP subprocess, no client/server handshake, because the schema the
decorator registers is not what this capstone's agent needs to exercise in
stub mode -- the function body is.
"""
from __future__ import annotations

import json

from . import logistics_mcp_versioned as mcp_tool

ITEM_KEYWORDS = ["amoxicillin", "ors_sachets", "malaria_kits"]
DEFAULT_ITEM = "amoxicillin"


def _item_in(text: str) -> str:
    low = text.lower()
    for item in ITEM_KEYWORDS:
        if item.replace("_", " ") in low or item in low:
            return item
    return DEFAULT_ITEM


def lookup(text: str) -> dict:
    """Route a logistics-intent message to check_stock() for the item it
    names, defaulting to amoxicillin when no item keyword is present."""
    item = _item_in(text)
    result = json.loads(mcp_tool.check_stock(item))
    return {
        "tool": "check_stock",
        "mcp_version": mcp_tool.MCP_VERSION,
        "item": item,
        "result": result,
    }
