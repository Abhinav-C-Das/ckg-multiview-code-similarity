#!/usr/bin/env bash
set -euo pipefail

FEATURES_DIR="outputs"
VECTORS_DIR="vectors/baseline"

mkdir -p "$VECTORS_DIR"

find "$FEATURES_DIR" -mindepth 3 -maxdepth 3 -type d | while read -r PROG_DIR; do
  NAME=$(basename "$PROG_DIR")
  PROBLEM=$(basename "$(dirname "$(dirname "$PROG_DIR")")")
  ROLE=$(basename "$(dirname "$PROG_DIR")")

  ID="${PROBLEM}_${ROLE}_${NAME}"

  echo "[PIPELINE] $ID"

  # --------------------------------------------------
  # 1. Aggregate numeric features (SAFE)
  #    → save BOTH to outputs/ and temp
  # --------------------------------------------------
  COMBINED_JSON="$PROG_DIR/combined_features.json"

  python3 similarity/aggregate_baseline.py "$PROG_DIR" \
    | tee "$COMBINED_JSON" \
    > "/tmp/$ID.features.json"

  # sanity check
  if [ ! -s "/tmp/$ID.features.json" ]; then
    echo "[WARN] Empty features for $ID, skipping"
    continue
  fi

  # --------------------------------------------------
  # 2. Vectorize
  # --------------------------------------------------
  python3 similarity/vectorize_features.py \
    "/tmp/$ID.features.json" \
    "$VECTORS_DIR/$ID.vec"

  # --------------------------------------------------
  # 3. Normalize (L2)
  # --------------------------------------------------
  python3 similarity/normalize.py \
    "$VECTORS_DIR/$ID.vec" \
    "$VECTORS_DIR/$ID.norm.vec"

  # --------------------------------------------------
  # 4. Compute baseline similarity matrix
  # --------------------------------------------------
  python3 evaluation/run_baseline_similarity_matrix.py

done
