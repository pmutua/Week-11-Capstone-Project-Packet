# Week 6 triage (integrated)

- Routes: `POST /token`, `POST /triage` (authenticated), `GET /health` (open)
- Pins: `prompts/pin.json` (model_id + prompt_version + prompt_sha256 + corpus_sha256)
- Auth: `auth.py`, copied unchanged from `week6_monday/auth.py`
- Rate gate: `rate_limit.py`, copied unchanged from `week6_monday/rate_limit.py`
- Redaction: `redact.py`, adapted from `week9_tuesday/redact.py` (added an
  email pattern the Week 9 version did not need)
- Grounded lookup: `rag.py` over `knowledge/ors_faq.md`, the same file
  `week9_monday/knowledge/pin.json` pins
- Agent + tool: `agents/router.py` routes a `logistics_lookup` intent to
  `agents/tools/logistics.py`, which calls `week8_monday`'s versioned
  logistics MCP tool functions directly (stub mode, no subprocess)

Do not log raw patient narrative to stdout; `redact()` runs on the request
text before it would reach any log line or audit record.
