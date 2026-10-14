# User guide

## Run
See `docs/deployment.md`.

## Health check
```
curl localhost:8080/health
```

## Full walkthrough
```
curl -X POST localhost:8080/token -H "Content-Type: application/json" \
  -d '{"username":"mercy","password":"logistics2026"}'
# -> {"access_token": "...", "token_type": "bearer"}

curl -X POST localhost:8080/triage -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" -d '{"text":"track delivery"}'
# -> intent=logistics_lookup, tool_called=check_stock, a real stock table

curl -X POST localhost:8080/triage -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" -d '{"text":"child needs ors"}'
# -> intent=triage, grounded=true, the ors_faq.md answer
```
The demo users are `mercy` / `logistics2026` (role: coordinator) and
`guest` / `lookaround` (role: viewer), both from `week6_monday/auth.py`'s
in-memory user table.

## Fallback path (stub mode)
There is no live-key fallback branch to describe: this build only ever
runs in stub mode. `model_id` in `services/triage/prompts/pin.json` names
the deterministic offline router/RAG/MCP stack actually running, not a
placeholder for a disabled live path.

## Fixture location
`fixtures/triage_messages_sample.jsonl`, 300 rows. Regenerate with
`python scripts/make_fixture.py --rows 300 --out fixtures/triage_messages_sample.jsonl`.
