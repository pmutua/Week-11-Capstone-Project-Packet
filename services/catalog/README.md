# Week 10 catalog lane (deferred)

The optional multimodal lane (Week 10 Monday's catalog-mismatch join over
`week10_monday/catalog.json` + `mismatch.py`) is not wired into this
capstone's request path. The MWP's "at most one" optional lane is left
unbuilt this week so the required layers (auth, pin, RAG, MCP tool,
security smoke, eval) stay the graded focus.

`catalog_mismatch` remains a label `agents/router.py` can route to (see
`config.json`), but no handler consumes it yet -- see
`docs/build_checkpoint.md` for the honest status.
