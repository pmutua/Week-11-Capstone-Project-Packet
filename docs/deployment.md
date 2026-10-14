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
No cloud deploy and no Docker have executed this build. CI is real,
though: `.github/workflows/ci.yml` runs on every push and pull request
against this repo's own GitHub Actions
(github.com/pmutua/Week-11-Capstone-Project-Packet/actions), and is
green as of the last commit to `main` -- see the badge at the top of
`README.md`. Everything else in this doc pack was run on a laptop first,
commands transcribed as they were actually executed.
