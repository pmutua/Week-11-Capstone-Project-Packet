# Presentation outline (8-10 slides for Week 12 Monday)

1. **Problem and user**: clinic coordinators and partner-clinic staff need
   one authenticated endpoint that answers a message with either a
   grounded FAQ answer, a live logistics lookup, or safe generic triage
   advice -- today that logic is split across three separate Week 6-9
   labs with no single service wiring them together.

2. **Path chosen and why**: AfyaPlus Module 4 Capstone, because this
   repo already has real, tested Week 6/8/9/10 artefacts to integrate
   rather than invent from scratch (see `skill_matrix.md`).

3. **Architecture diagram with module boundaries**: `docs/architecture.md`
   -- client -> `services/triage/app.py` (auth + rate limit) ->
   `agents/router.py` -> either `agents/tools/logistics.py` (MCP tool,
   stub mode) or `services/triage/rag.py` (grounded FAQ lookup).

4. **Skill coverage (which skills, where in repo)**: `skill_matrix.md`'s
   table -- API/agent path (Week 6), MCP tool (Week 8), pin (Week 8), RAG
   (Week 9 corpus), security hygiene (Week 9 redaction), eval (Week 11).

5. **Live demo** (or `docs/demo_script.sh`'s transcript as a 60-second
   recording backup): `/health` -> 200, no-token `/triage` -> 401,
   `/token` -> a real JWT, authenticated `/triage` on `"track delivery"`
   -> a real `check_stock` MCP tool result, and on `"child needs ors"` ->
   a grounded ORS FAQ answer.

6. **Testing evidence**: `pytest -q` -> 16 passed, 1 deselected;
   `tests/test_security_smoke.py` green (env not tracked, no live key,
   real email redaction); `evals/run_eval.py` -> `3/3 = 1.00`;
   `perf_stub.json`'s measured p95, captioned as a laptop stub.

7. **Security and compliance choices**: Bearer-token auth + per-user rate
   limiting (Week 6); `redact()` strips bearer tokens, phone numbers,
   M-Pesa codes, Kenyan IDs, and email addresses before any text would
   reach a log line (Week 9, extended); `.env` is gitignored and verified
   untracked by a real test, not a promise.

8. **Cost table with assumptions**: `docs/cost_analysis.md` -- genuinely
   $0 throughout, since this build has no live-model code path at all
   (`model_id: stub-local-router-v1`), not merely a capped demo budget.

9. **What works vs deferred**: `docs/build_checkpoint.md` -- the full
   MWP runs in stub mode end to end, and `ci.yml` is real, green CI on
   this repo's own GitHub Actions; deferred items are the Week 10
   catalog-mismatch lane, any live model wiring, and any cloud deploy.

10. **Process**: one feature branch (`feature/week11-capstone-setup`),
    conventional commits per lesson day, a solo self-review against
    `docs/peer_review_checklist.md` (8/8 ticked, logged in
    `review_log.md`), next step is Week 12 Monday's live demo.
