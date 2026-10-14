# Deployment

## Run locally
```
pip install -r requirements.txt
uvicorn services.triage.app:app --port 8080
```
Run from `module4-capstone/` so `services.triage` and `agents` resolve as
importable packages (the app also inserts the repo root onto `sys.path`
itself, so this works from either location in practice).

## Env vars
- `JWT_SECRET` (optional; `auth.py` falls back to a dev-only secret with a
  loud comment never to rely on that fallback outside a classroom)
- No model API key of any kind is read by this build -- there is no live
  model code path yet (see `docs/build_checkpoint.md`)

## Health
`GET /health` returns 200 with `model_id`, `prompt_version`, and
`prompt_sha256` from `services/triage/prompts/pin.json`.

## Fallback
No cloud deploy, no Docker, and no CI runner have actually executed this
build. `module4-capstone/.github/workflows/ci.yml` is illustrative only
(see `docs/build_checkpoint.md`); everything in this doc pack was run on
a laptop, commands transcribed as they were actually executed.
