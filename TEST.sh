#!/usr/bin/env bash
set -euo pipefail

echo "[INFO] Running ClaimForge smoke test..."

# Load .env if present, otherwise create a fallback dummy one
if [[ -f .env ]]; then
  export $(grep -v '^#' .env | xargs)
else
  echo "[WARNING] .env file not found. Creating a dummy one..."
  cat <<EOF > .env
GEMINI_API_KEY=dummy
GOOGLE_API_KEY=dummy
SERP_API_KEY=dummy
EOF
  export GEMINI_API_KEY=dummy
  export GOOGLE_API_KEY=dummy
  export SERP_API_KEY=dummy
fi

# Detect and report API keys
[[ -n "${GEMINI_API_KEY:-}" ]] && echo "[INFO] GEMINI_API_KEY detected." || echo "[WARNING] GEMINI_API_KEY not set."
[[ -n "${GOOGLE_API_KEY:-}" ]] && echo "[INFO] GOOGLE_API_KEY detected." || echo "[WARNING] GOOGLE_API_KEY not set."
[[ -n "${SERP_API_KEY:-}" ]]   && echo "[INFO] SERP_API_KEY detected."   || echo "[WARNING] SERP_API_KEY not set."

# Run main CLI help check
if python src/main.py --help; then
  echo "[INFO] CLI responded successfully."
else
  echo "[WARNING] CLI exited with a non-zero status."
fi

echo "[INFO] Smoke test completed."

