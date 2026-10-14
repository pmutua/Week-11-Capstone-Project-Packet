# Build checkpoint

## Works now
- `proposal.md` path: AfyaPlus Module 4 Capstone
- `skill_matrix.md` and `integration_map.json` complete; `check_proposal.py`
  and `check_integration_map.py` both exit 0
- `pytest -q` from `module4-capstone/`: 16 passed, 1 deselected
  (the `integration`-marked health check, which needs `SERVICE_UP=1` and a
  running service -- also verified green separately, see below)
- `tests/test_security_smoke.py` passes: `.env` not tracked, no
  `sk-live-*`-looking string outside `tests/`, and a real redaction test
  (`redact()` strips an email address)
- Golden-set eval: `python evals/run_eval.py evals/golden.jsonl` ->
  `golden-set score: 3/3 = 1.00`
- Minimum Working Product runs end to end in stub mode, verified live:
  `GET /health` -> 200, `POST /triage` with no token -> 401, `POST /token`
  -> a real JWT, `POST /triage` with that token on `"track delivery"` ->
  validated JSON carrying a real `check_stock` MCP tool result
  (`tool_called: "check_stock"`), and `"child needs ors and fluids"` ->
  `grounded: true` with the ORS FAQ text as the answer
- `fixtures/triage_messages_sample.jsonl`: 300 synthetic rows,
  `scripts/diagnose_fixture.py` reports "diagnose OK, all rows agree with
  router"
- `perf_stub.json`: a real measured p95 over 10 `/health` calls against
  the running service (laptop teaching stub, not a production SLA)
- `docs/presentation.pdf`: a real 10-page PDF (`%PDF-1.4`, 10 `/Type
  /Page` objects, verified by reading the file bytes) rendered from
  `docs/presentation_outline.md` by `scripts/make_slides_pdf.py`
- `.github/workflows/ci.yml` is real CI now, not illustrative --
  `module4-capstone` is its own GitHub repository
  (github.com/pmutua/Week-11-Capstone-Project-Packet), so pushes
  actually trigger Actions. Running the bare commands CI uses (not
  `python -m pytest`) surfaced a real bug: `pytest -q` failed with
  `ModuleNotFoundError` on `services`/`agents` because nothing put the
  repo root on `sys.path`. Fixed with `pytest.ini`'s `pythonpath = .`.
  `ruff check .` also now passes clean (5 real findings fixed or
  justified-ignored; see the `fix/rubric-compliance` PR)

## Incident note
Running `scripts/diagnose_fixture.py` for the first time surfaced a real
disagreement: the starter pack's own `"where is my order"` template for
`logistics_lookup` had no matching keyword in `config.json`'s
`route_keywords`, so 28 of 300 rows misrouted to `triage`. Fixed by adding
`"order"` to `logistics_lookup`'s keyword list -- a genuine router-coverage
gap, not a fixture edit. Full detail, including the separate deliberate
T-002 break/restore drill, is in `fixtures/diagnosis_notes.txt`.

## Deferred
- The optional Week 10 catalog-mismatch lane (`services/catalog/`) --
  `catalog_mismatch` is a router label only; no handler consumes it. See
  `services/catalog/README.md`.
- Any live model call. `model_id` in `services/triage/prompts/pin.json` is
  `stub-local-router-v1`: this build's deterministic offline router/RAG/MCP
  stack, never a hosted model. No `LIVE_MODEL=1` code path exists yet, so
  the cost table in `docs/cost_analysis.md` is honestly $0 throughout, not
  the ~$1 Thursday-demo figure the generic lesson template assumes.
- A peer-reviewed PR from a *second* reviewer. This is a solo-learner
  project with no second reviewer available; `review_log.md` records a
  real, merged PR self-reviewed against `docs/peer_review_checklist.md`
  instead, per the lesson's own allowance for solo cohorts.
