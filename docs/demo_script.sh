#!/usr/bin/env bash
# Three-command demo, run from module4-capstone/. Every line below was
# run against the real service before being written down here.
set -e

# 1. start the service
uvicorn services.triage.app:app --port 8080 &
sleep 2

# 2. confirm health
curl -s localhost:8080/health

# 3. log in, then send one demo message through the agent + MCP tool
TOKEN=$(curl -s -X POST localhost:8080/token -H "Content-Type: application/json" \
  -d '{"username":"mercy","password":"logistics2026"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
curl -s -X POST localhost:8080/triage -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" -d '{"text":"track delivery"}'
