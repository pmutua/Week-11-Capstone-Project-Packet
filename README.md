# Module 4 Capstone: AfyaPlus integrated AI health-operations system

## Overview
One FastAPI service (`services/triage`) accepts an authenticated message,
routes it through an agent (`agents/router.py`) that can call one MCP
logistics tool in stub mode, grounds one answer in a small document set,
and returns validated JSON built on prompt/model versions pinned in
`services/triage/prompts/pin.json`. Path chosen: AfyaPlus Module 4
Capstone (see `proposal.md`).

## Quick start
```
pip install -r requirements.txt
pytest -q
uvicorn services.triage.app:app --port 8080
curl localhost:8080/health
```

## Docs
- docs/architecture.md
- docs/deployment.md
- docs/cost_analysis.md
- docs/user_guide.md
- docs/build_checkpoint.md

## Demo
Three commands: start the service, curl `/health`, curl `/triage` with a
bearer token (see `docs/user_guide.md`).

## Presentation
docs/presentation_outline.md, presented Week 12 Monday.

## Peer review
- review_log.md entry
- checklist: docs/peer_review_checklist.md
