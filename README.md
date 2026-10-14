# Module 4 Capstone: AfyaPlus integrated AI health-operations system

![CI](https://github.com/pmutua/Week-11-Capstone-Project-Packet/actions/workflows/ci.yml/badge.svg)

## Overview
One FastAPI service (`services/triage`) accepts an authenticated message,
routes it through an agent (`agents/router.py`) that can call one MCP
logistics tool in stub mode, grounds one answer in a small document set,
and returns validated JSON built on prompt/model versions pinned in
`services/triage/prompts/pin.json`.

## Project path
- [x] AfyaPlus Module 4 Capstone (recommended)
- [ ] Domain / field alternative with skill checklist

## Week reuse (open these)
- Weeks 1-5: no direct code reuse in this build; the MWP's layers map
  onto Weeks 6-9 specifically (see below) rather than an earlier week
- Week 6: `services/triage/auth.py` + `rate_limit.py`, copied unchanged
  from `week6_monday/auth.py` and `week6_monday/rate_limit.py`
- Week 7: lineage only -- the real MCP tool code imported is Week 8
  Monday's versioned copy of Week 6 Thursday's `logistics_mcp.py`; no
  separate Week 7 file is imported directly
- Week 8: `services/triage/prompts/pin.json` (extends
  `week8_monday/prompts/pin.json`'s prompt pin with a `model_id`);
  `agents/tools/logistics_mcp_versioned.py`, copied unchanged from
  `week8_monday/logistics_mcp_versioned.py`
- Week 9: `services/triage/redact.py` (extends
  `week9_tuesday/redact.py`'s patterns with an email rule);
  `services/triage/knowledge/ors_faq.md`, the same corpus
  `week9_monday/knowledge/pin.json` pins
- Week 10: deferred -- `services/catalog/README.md` documents the
  catalog-mismatch lane as the one optional multimodal item not built
  this week

## Dataset
- `fixtures/triage_messages_sample.jsonl`: 300 rows (200-500 range). No
  production scrape -- see `fixtures/README.md`.

## Quick start
```
pip install -r requirements.txt
pytest -q
```

## Docs
- docs/architecture.md
- docs/deployment.md
- docs/cost_analysis.md
- docs/user_guide.md
- docs/build_checkpoint.md

## Testing
- unit default: `pytest -q` (16 passed, 1 deselected as of this commit)
- integration: `pytest -m integration` (needs `SERVICE_UP=1` and the
  service running on `localhost:8080`)
- security: `pytest tests/test_security_smoke.py` (3 passed)
- eval: `python evals/run_eval.py evals/golden.jsonl` -> `3/3 = 1.00`

## Demo
Three commands, bundled in one script (`bash docs/demo_script.sh`):
start the service, curl `/health`, log in and curl `/triage` with the
bearer token. A real captured run is in `docs/demo_transcript.txt`. Full
walkthrough in `docs/user_guide.md`.

## Presentation
`docs/presentation.pdf` (10 slides, rendered from
`docs/presentation_outline.md` by `scripts/make_slides_pdf.py`),
presented Week 12 Monday.

## Peer review
- review_log.md entry (date, PR reference, reviewer, outcomes)
- checklist: docs/peer_review_checklist.md (8 items)

## Fallbacks declared
- [x] no live OpenAI key (deterministic stub router/RAG/MCP stack --
      `model_id: stub-local-router-v1`, no live-model code path exists)
- [x] no Docker (pytest + httpx integration test instead)
- [x] no cloud deploy executed (docs/deployment.md steps marked "not
      executed live")
- [x] solo reviewer (self-review with checklist, PR opened and merged
      by the same author -- see review_log.md)

## Submission checklist
- [x] proposal + skill_matrix + map (`check_proposal.py`,
      `check_integration_map.py` both pass)
- [x] five docs linked (`check_doc_links.py` passes)
- [x] peer review completed (`check_review_doc.py` passes; review_log.md
      has a dated entry with a PR reference)
- [x] slides PDF in docs/ and demo command documented (`docs/presentation.pdf`,
      `bash docs/demo_script.sh`)
