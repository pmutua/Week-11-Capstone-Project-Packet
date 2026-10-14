# logistics_mcp_versioned.py - Week 8 Monday, Lab 2: version the Week 6
# Thursday logistics MCP server (week6_thursday/logistics_mcp.py) under
# semver, without touching its existing tool schemas.
#
# 1.0.0 baseline carried forward unchanged: check_stock(item),
# plan_delivery_route(start_clinic_id), get_delivery_eta(from, to), and
# the clinics://directory resource — this repo's REAL Week 6 baseline,
# not the lesson's illustrative check_stock(clinic_id, item) shape (see
# notes/week8_monday/monday_lesson_7_lab2_version_mcp.md for why the two
# differ and why this file versions the real tool instead of inventing a
# new one to match the lesson's snippet).
#
# 1.1.0 additive release: a version://current resource (the machine-
# readable pin CI reads, not a FastMCP(version=...) kwarg — SDK support
# for that varies) and one new tool, list_low_stock(clinic_id). Old
# agents that never call list_low_stock are unaffected; existing
# check_stock/plan_delivery_route/get_delivery_eta callers see zero
# schema change. See CHANGELOG.md for the release notes.
#
# Run it:
#   python logistics_mcp_versioned.py
# Fastest first test (no agent, no protocol):
#   python -c "
#   import logistics_mcp_versioned as m
#   print(m.version_current())
#   print(m.check_stock('amoxicillin'))
#   print(m.list_low_stock('C01'))
#   "

from __future__ import annotations

import json
import logging
import math
from pathlib import Path

from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger("logistics")

MCP_VERSION = "1.1.0"
server = FastMCP("afyaplus-logistics")  # do not pass version=; pin via version://current

CLINICS_PATH = Path(__file__).resolve().parent / "clinics.json"
with open(CLINICS_PATH) as f:
    CLINICS = json.load(f)["clinics"]

VALID_ITEMS = ["amoxicillin", "ors_sachets", "malaria_kits"]
REORDER_THRESHOLD = 10  # matches check_stock's existing reorder_needed rule, unchanged since 1.0.0


@server.resource("version://current")
def version_current() -> str:
    """Semver of this MCP server. Agents and CI should read this, not
    guess it from behaviour."""
    return MCP_VERSION


def distance_km(a: dict, b: dict) -> float:
    """Rough distance between two clinics in kilometres."""
    dx = (a["lon"] - b["lon"]) * 111.32 * math.cos(math.radians((a["lat"] + b["lat"]) / 2))
    dy = (a["lat"] - b["lat"]) * 110.57
    return round(math.sqrt(dx * dx + dy * dy), 1)


@server.tool()
def check_stock(item: str) -> str:
    """Check how many units of a medical item each clinic holds.
    Valid items: amoxicillin, ors_sachets, malaria_kits. Stock counts are
    units on hand, not prices or orders — this tool has no price data.
    Schema unchanged since 1.0.0."""
    log.info("tool=check_stock item=%s", item)
    if item not in VALID_ITEMS:
        return json.dumps({"error": f"Unknown item '{item}'. Valid items: {VALID_ITEMS}"})
    rows = [
        {
            "clinic": c["name"],
            "county": c["county"],
            "units": c["stock"][item],
            "reorder_needed": c["stock"][item] < REORDER_THRESHOLD,
        }
        for c in CLINICS
    ]
    return json.dumps({"item": item, "stock": rows})


@server.tool()
def list_low_stock(clinic_id: str) -> str:
    """List items at one clinic at or below the reorder threshold.
    Additive in 1.1.0: a new tool old agents can ignore, no existing
    tool schema changed."""
    log.info("tool=list_low_stock clinic_id=%s", clinic_id)
    clinic = next((c for c in CLINICS if c["id"] == clinic_id), None)
    if clinic is None:
        ids = [c["id"] for c in CLINICS]
        return json.dumps({"error": f"Unknown clinic id '{clinic_id}'. Valid ids: {ids}"})
    low = [
        {"item": item, "units": units}
        for item, units in clinic["stock"].items()
        if units < REORDER_THRESHOLD
    ]
    return json.dumps({"clinic": clinic["name"], "low_stock": low, "mcp_version": MCP_VERSION})


@server.tool()
def plan_delivery_route(start_clinic_id: str) -> str:
    """Plan a delivery route visiting every clinic, starting from one clinic.
    Uses the nearest-neighbour rule: always drive to the closest unvisited clinic next.
    This is quick decision support, not a guaranteed-shortest route.
    Schema unchanged since 1.0.0."""
    log.info("tool=plan_delivery_route start=%s", start_clinic_id)
    start = next((c for c in CLINICS if c["id"] == start_clinic_id), None)
    if start is None:
        ids = [c["id"] for c in CLINICS]
        return json.dumps({"error": f"Unknown clinic id '{start_clinic_id}'. Valid ids: {ids}"})
    route, remaining, total = [start], [c for c in CLINICS if c["id"] != start_clinic_id], 0.0
    while remaining:
        here = route[-1]
        nearest = min(remaining, key=lambda c: distance_km(here, c))
        total += distance_km(here, nearest)
        route.append(nearest)
        remaining.remove(nearest)
    return json.dumps(
        {
            "route": [c["name"] for c in route],
            "total_km": round(total, 1),
            "method": "nearest-neighbour heuristic",
        }
    )


@server.tool()
def get_delivery_eta(from_clinic_id: str, to_clinic_id: str) -> str:
    """Estimate driving distance (km) and time (minutes) between two clinics,
    assuming a 40 km/h average speed on regional roads. This is a planning
    estimate, not a commitment — actual travel time depends on road
    conditions and traffic this tool has no data about.
    Schema unchanged since 1.0.0."""
    log.info("tool=get_delivery_eta from=%s to=%s", from_clinic_id, to_clinic_id)
    a = next((c for c in CLINICS if c["id"] == from_clinic_id), None)
    b = next((c for c in CLINICS if c["id"] == to_clinic_id), None)
    if a is None or b is None:
        ids = [c["id"] for c in CLINICS]
        return json.dumps({"error": f"Unknown clinic id. Valid ids: {ids}"})
    km = distance_km(a, b)
    return json.dumps(
        {
            "from": a["name"],
            "to": b["name"],
            "km": km,
            "eta_minutes": round(km / 40 * 60),
            "assumed_speed_kmh": 40,
        }
    )


@server.resource("clinics://directory")
def clinic_directory() -> str:
    """Read-only directory of all AfyaPlus partner clinics.
    Schema unchanged since 1.0.0."""
    return json.dumps([{"id": c["id"], "name": c["name"], "county": c["county"]} for c in CLINICS])


if __name__ == "__main__":
    server.run()
