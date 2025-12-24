#!/usr/bin/env bash
set -e

# ---------------------------------------
# Force project root
# ---------------------------------------
cd "$(dirname "$0")"
cd ../..

# Usage:
# ./run_ces_extract.sh p1 s1 students
# ./run_ces_extract.sh p1 ref1 refs

PROBLEM="$1"
ID="$2"
MODE="$3"   # students | refs

# ---------------------------------------
# Normalize role + paths (CRITICAL FIX)
# ---------------------------------------
if [ "$MODE" = "students" ]; then
  ROLE="s"
  SRC="data/${PROBLEM}/s/${ID}.c"
  OUT="outputs/${PROBLEM}_students/${ID}"
elif [ "$MODE" = "refs" ]; then
  ROLE="ref"
  SRC="data/${PROBLEM}/ref/${ID}.c"
  OUT="outputs/${PROBLEM}_refs/${ID}"
else
  echo "Unknown MODE: $MODE"
  exit 1
fi

# ---------------------------------------
# Canonical CPG path (MATCHES BASELINE)
# ---------------------------------------
CPG_DIR="cpgs/${PROBLEM}/${ROLE}/${ID}"
CPG_PATH="${CPG_DIR}/cpg.bin"

mkdir -p "$OUT" "$CPG_DIR"

echo "[CES] Extracting $PROBLEM $MODE $ID"

# ---------------------------------------
# Build CPG ONLY if missing
# ---------------------------------------
if [ ! -f "$CPG_PATH" ]; then
  echo "[CES] Building CPG at $CPG_PATH"
  joern-parse "$SRC" --output "$CPG_PATH" >/dev/null
else
  echo "[CES] Reusing CPG at $CPG_PATH"
fi

# ---------------------------------------
# Run CES extraction using EXISTING CPG
# ---------------------------------------
export TARGET_FILE="$(basename "$SRC")"

joern --exit --cpg "$CPG_PATH" \
      --script cpg/scripts/semantic/ces_semantic.sc \
      > "$OUT/ces_raw.json"

# ---------------------------------------
# Sanitize JSON output
# ---------------------------------------
awk '/^[[:space:]]*\[\{/{flag=1} flag' \
  "$OUT/ces_raw.json" > "$OUT/ces.json"

rm "$OUT/ces_raw.json"

echo "[CES] Done → $OUT/ces.json"
