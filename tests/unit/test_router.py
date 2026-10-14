"""Change for your project: nothing. Update config.json route_keywords instead."""
from agents.router import route


def test_route_logistics():
    assert route("track delivery") == "logistics_lookup"


def test_route_default():
    assert route("general question") == "triage"


def test_route_catalog_mismatch():
    assert route("listing photo mismatch") == "catalog_mismatch"


def test_route_logistics_shipment_delay():
    assert route("shipment delay") == "logistics_lookup"
