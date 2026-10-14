# Capstone proposal

## Path
AfyaPlus Module 4 Capstone: integrated AI health-operations system.

## Problem
Clinic coordinators and partner-clinic staff need one place to send a
patient-facing message and get back either (a) grounded health guidance for
a known FAQ topic, (b) a stock/logistics answer pulled live from the
logistics MCP tool, or (c) safe generic triage advice when neither applies
-- all behind auth, all rate-limited, all logged with identifiers
redacted. Today that reasoning is split across the Week 6 triage API, the
Week 7/8 logistics MCP tool, and Week 9's security/redaction habits, with
no single service wiring the three together. This week's build closes that
gap: one FastAPI service, one router, one MCP tool call, deterministic in
stub mode. Success this week looks like: proposal + matrix + map + a
pytest pyramid + security smoke + a printed eval score + a full doc pack,
with `/health` returning 200 from one documented command and no live model
key required.

## Dataset
`fixtures/triage_messages_sample.jsonl`: 300 synthetic rows across the
three labels the router already recognises (`triage`, `logistics_lookup`,
`catalog_mismatch`), generated offline by `scripts/make_fixture.py` from
`config.json`'s route keywords.

Do not scrape production data. Do not use millions of rows here. No
clinical PII and no marketplace PII are mixed in the same file; the
optional catalog lane (if built) would get its own fixture under a
separate path.

## Milestones
- Monday: proposal, skill_matrix, integration_map, base service `/health` 200
- Tuesday: pytest pyramid, security smoke, CI, grounded lookup + MCP tool
  wired, fixture generated, one row diagnosed, eval score printed
- Thursday: doc pack, peer review (self-review, solo learner), presentation
  outline, demo script
- Week 12 Monday: presentation and demo

## Out of scope
- Training a new foundation model
- Live crawl of patient or buyer PII
- Mixing clinical and marketplace fixtures in one file
- A live, billed model call anywhere in the default test/CI path (stub
  mode is the only mode this build is graded in; a `LIVE_MODEL=1` path is
  documented but never exercised automatically)
