#!/usr/bin/env python3
"""Render docs/presentation_outline.md's ten slide prompts into a real,
valid docs/presentation.pdf using matplotlib's PDF backend (already a
project dependency via pytest/ruff's own transitive deps are not
guaranteed, so this script is the only place matplotlib is imported --
no pandoc/wkhtmltopdf/LaTeX available in this environment). One page per
slide, text only, no network, no model call.
"""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

SLIDES = [
    ("Problem and user", [
        "Clinic coordinators and partner-clinic staff need one endpoint",
        "that answers a message with a grounded FAQ answer, a live",
        "logistics lookup, or safe generic triage advice.",
        "Today that logic is split across three separate Week 6-9 labs.",
    ]),
    ("Path chosen and why", [
        "AfyaPlus Module 4 Capstone.",
        "This repo already has real, tested Week 6/8/9/10 artefacts to",
        "integrate rather than invent from scratch (see skill_matrix.md).",
    ]),
    ("Architecture", [
        "client -> services/triage/app.py (auth + rate limit)",
        "       -> agents/router.py",
        "            -> agents/tools/logistics.py (MCP tool, stub mode)",
        "            -> services/triage/rag.py (grounded FAQ lookup)",
        "See docs/architecture.md for the full diagram.",
    ]),
    ("Skill coverage", [
        "API/agent path -- Week 6 (auth.py, rate_limit.py)",
        "MCP tool + pin -- Week 8 (logistics_mcp_versioned.py, pin.json)",
        "Grounded lookup -- Week 9 (knowledge/ors_faq.md corpus pin)",
        "Security hygiene -- Week 9 (redact.py, security smoke)",
        "Eval -- Week 11 (evals/golden.jsonl, pytest pyramid)",
    ]),
    ("Live demo", [
        "GET /health -> 200",
        "POST /triage with no token -> 401",
        "POST /token -> a real JWT",
        "POST /triage \"track delivery\" -> a real check_stock MCP result",
        "POST /triage \"child needs ors\" -> grounded ORS FAQ answer",
        "See docs/demo_script.sh and docs/demo_transcript.txt.",
    ]),
    ("Testing evidence", [
        "pytest -q: 16 passed, 1 deselected",
        "tests/test_security_smoke.py: env not tracked, no live key,",
        "  a real redaction test (email stripped)",
        "evals/run_eval.py: golden-set score 3/3 = 1.00",
        "perf_stub.json: measured p95 over 10 /health calls",
    ]),
    ("Security and compliance choices", [
        "Bearer-token auth + per-user rate limiting (Week 6)",
        "redact() strips bearer tokens, phone numbers, M-Pesa codes,",
        "  Kenyan IDs, and email addresses before any log line",
        ".env gitignored and verified untracked by a real test",
    ]),
    ("Cost table", [
        "Stub tests: 0 calls, $0",
        "Thursday demo: 0 calls, $0",
        "No live-model code path exists in this build --",
        "model_id is stub-local-router-v1, not a hosted model.",
    ]),
    ("What works vs deferred", [
        "Works: full MWP in stub mode end to end (auth, RAG, MCP tool,",
        "  pins, security smoke, eval, fixture)",
        "Deferred: Week 10 catalog-mismatch lane, any live model call,",
        "  real CI/cloud execution beyond this repo's own GitHub Actions",
    ]),
    ("Process", [
        "Feature branches + conventional commits per lesson day",
        "A real PR reviewed and merged (see review_log.md for the link)",
        "Next step: Week 12 Monday live demo",
    ]),
]


def render(out_path: str = "docs/presentation.pdf") -> None:
    with PdfPages(out_path) as pdf:
        for i, (title, lines) in enumerate(SLIDES, start=1):
            fig = plt.figure(figsize=(11, 6.19))  # 16:9
            fig.text(0.06, 0.88, f"{i}. {title}", fontsize=22, weight="bold")
            body = "\n".join(lines)
            fig.text(0.08, 0.78, body, fontsize=13, va="top", family="monospace")
            fig.text(0.06, 0.04, "AfyaPlus Module 4 Capstone -- Week 11", fontsize=9, color="gray")
            pdf.savefig(fig)
            plt.close(fig)
    print(f"wrote {out_path}: {len(SLIDES)} slides")


if __name__ == "__main__":
    render()
