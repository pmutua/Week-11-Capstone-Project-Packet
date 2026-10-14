# Review log

## Note on this repo's history
This repo's `main` was not hand-committed directly: its first 7 commits
were authored on branch `feature/week11-capstone-setup` in the source
monorepo (github.com/pmutua/afyaplus-learning), where Weeks 1-10's real
artefacts (`week6_monday/`, `week8_monday/`, `week9_monday/`,
`week9_tuesday/`) already lived, then extracted here with
`git subtree split --prefix=module4-capstone` and pushed as `main` --
commit SHAs `f961413`..`9ed5bc1` (subject lines unchanged; see this
file's first entry below for that work's own review). All work *in this
repo* from that point on follows normal feature-branch + PR flow (see
PR #1 below).

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

- 2026-10-14: PR #1 (https://github.com/pmutua/Week-11-Capstone-Project-Packet/pull/1,
  "Fix real CI, render presentation PDF, align README with packet
  template"), branch `fix/rubric-compliance` -> `main`, merge commit
  `ca70fb3`. Reviewer: Philip Mutua (solo-learner self-review, approved
  on GitHub, merged with a regular merge commit -- not squashed -- so
  the branch history stays visible). Outcome: approved and merged after
  CI went green. Two real bugs were found and fixed by actually running
  CI rather than assuming it would pass, not by inspection:
  - Bare `pytest -q` (what CI runs, not `python -m pytest`) failed with
    `ModuleNotFoundError` on `services`/`agents`; fixed with
    `pytest.ini`'s `pythonpath = .`
  - `ruff check .` failed on EXE001 (shebang scripts committed without
    the executable bit, since Windows git doesn't track it); fixed with
    `git update-index --chmod=+x` on the five affected scripts
  - A fresh `pip install -r requirements.txt` on the Actions runner
    resolved unpinned `mcp` to 2.x, which renamed
    `mcp.server.fastmcp.FastMCP` to `MCPServer`, breaking test
    collection; fixed by pinning `mcp<2`, verified in a throwaway venv
    that simulated CI's exact install + bare-command sequence
  Also in this PR: a real 10-page `docs/presentation.pdf` (replacing
  outline-only slides), `docs/demo_transcript.txt` (a real captured
  run, not a described one), and a README rewrite matching the official
  packet template's exact section shape.
