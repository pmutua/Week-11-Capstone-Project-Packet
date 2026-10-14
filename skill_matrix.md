# Skill coverage matrix

| Skill | Week resource to open | My module / file | Required / Optional |
| --- | --- | --- | --- |
| API or agent path | Week 6 Monday `secure_triage_api.py` + `auth.py` | `services/triage/app.py`, `services/triage/auth.py`, `services/triage/rate_limit.py` | Required |
| Cost / MCP tools | Week 8 Monday `logistics_mcp_versioned.py` (versions the Week 6 Thursday / Week 7 logistics tool) | `agents/router.py`, `agents/tools/logistics.py`, `agents/tools/logistics_mcp_versioned.py` | Required |
| Pin / versioning | Week 8 Monday `prompts/pin.json` pattern, extended with `model_id` | `services/triage/prompts/pin.json`, `services/triage/prompts/triage_system_v1.2.0.txt` | Required |
| Security hygiene | Week 9 Tuesday `redact.py`; Week 9 Monday corpus pin and `.env` hygiene | `services/triage/redact.py`, `tests/test_security_smoke.py`, `.gitignore` | Required |
| Eval / test | Week 11 Tuesday pyramid + golden set | `tests/unit/`, `tests/integration/`, `evals/golden.jsonl` | Required |
| Docs | Prior READMEs (`services/triage/README.md`) + Week 11 doc pack | `docs/` | Required |
| Grounded answer (RAG) | Week 9 Monday `knowledge/ors_faq.md` corpus pin | `services/triage/rag.py`, `services/triage/knowledge/ors_faq.md` | Required |
| Optional multimodal | Week 10 Monday catalog-mismatch lane | not built this week; `catalog_mismatch` stays a router label only | Optional (deferred) |
