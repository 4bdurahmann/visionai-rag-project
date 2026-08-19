#!/usr/bin/env bash
# VisionAI Medical RAG - server launcher (works without activating the venv)
# Usage:  ./run.sh            -> start API on 0.0.0.0:8000
#         ./run.sh 9000       -> start API on 0.0.0.0:9000
#         ./run.sh --reload   -> dev reload mode on 8000
set -euo pipefail

cd "$(dirname "$0")"
PY="rag/bin/python"

if [ ! -x "$PY" ]; then
    echo "ERROR: venv python not found at $PY — run: python3 -m venv rag" >&2
    exit 1
fi

PORT="8000"
RELOAD=()
if [ "${1:-}" = "--reload" ]; then
    RELOAD=(--reload)
else
    PORT="${1:-8000}"
fi

echo "==> Starting VisionAI Medical RAG on http://0.0.0.0:${PORT}"
exec "$PY" -m uvicorn --app-dir src "${RELOAD[@]}" main:app --host 0.0.0.0 --port "${PORT}"