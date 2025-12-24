#!/usr/bin/env bash
set -euo pipefail

DATA_DIR="data"
OUT_DIR="features/scdps"
CPG_BIN="workspace/cpg.bin"
SCRIPT="cpg/scripts/scdps/scdps_extract.sc"

mkdir -p "$OUT_DIR"

for PROBLEM in "$DATA_DIR"/*; do
  [ -d "$PROBLEM" ] || continue
  PNAME=$(basename "$PROBLEM")

  for ROLE in ref s; do
    SRC_DIR="$PROBLEM/$ROLE"
    [ -d "$SRC_DIR" ] || continue

    for SRC in "$SRC_DIR"/*.c; do
      FILE=$(basename "$SRC")
      NAME="${FILE%.c}"
      ID="${PNAME}_${ROLE}_${NAME}"

      echo "[SCDPS] extracting $ID"

      mkdir -p "$OUT_DIR/$ID"
      export TARGET_FILE="$FILE"

      joern --exit \
        --import "$CPG_BIN" \
        --script "$SCRIPT" \
        | sed -n '/^{/,$p' \
        > "$OUT_DIR/$ID/scdps.json"
    done
  done
done
