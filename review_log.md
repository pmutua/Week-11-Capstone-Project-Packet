# Review log

- 2026-10-14: branch `feature/week11-capstone-setup`, reviewer: Philip
  Mutua (solo learner, self-review per the lesson's own allowance -- no
  second reviewer available this week). Outcome: 8/8 checklist items
  ticked against `docs/peer_review_checklist.md`:
  - [x] No secrets or `.env` in diff (checked `git diff` by hand; also
        covered by `tests/test_security_smoke.py::test_env_not_tracked`)
  - [x] `proposal.md` path choice explicit (AfyaPlus Module 4 Capstone)
  - [x] `skill_matrix.md` maps required skills to weeks
  - [x] `integration_map.json` paths exist on disk
        (`check_integration_map.py` -> `integration map OK 6`)
  - [x] `pytest -q` unit layer attached (`16 passed, 1 deselected`)
  - [x] Eval score printed (`golden-set score: 3/3 = 1.00`)
  - [x] Fixture row count in hundreds; no production-scrape claim
        (300 rows, `proposal.md` states the rule explicitly)
  - [x] README links all five docs (`check_doc_links.py` -> `doc links OK`)
  No follow-ups filed; see `docs/build_checkpoint.md` for the one
  substantive change this review caught (the `config.json` route-keyword
  gap found while generating the fixture).
