#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

DATA_DIR="$ROOT_DIR/data"
CPG_DIR="$ROOT_DIR/cpgs"
OUT_DIR="$ROOT_DIR/outputs"
SCRIPT="$ROOT_DIR/cpg/scripts/scdps/scdps_extract.sc"

for PROBLEM in "$DATA_DIR"/*; do
  [ -d "$PROBLEM" ] || continue
  PNAME=$(basename "$PROBLEM")

  for ROLE in ref s; do
    SRC_DIR="$PROBLEM/$ROLE"
    [ -d "$SRC_DIR" ] || continue

    for SRC in "$SRC_DIR"/*.c; do
      [ -f "$SRC" ] || continue

      FILE=$(basename "$SRC")
      NAME="${FILE%.c}"

      CPG_BIN="$CPG_DIR/$PNAME/$ROLE/$NAME/cpg.bin"
      OUT_PROG="$OUT_DIR/$PNAME/$ROLE/$NAME"

      if [ ! -f "$CPG_BIN" ]; then
        echo "[SCDPS ERROR] Missing CPG: $CPG_BIN"
        exit 1
      fi

      mkdir -p "$OUT_PROG"
      echo "[SCDPS] extracting $PNAME/$ROLE/$NAME"

      TARGET_FILE="$FILE" \
      joern --exit --cpg "$CPG_BIN" \
        --script "$SCRIPT" \
        | sed -n '/^{/,$p' \
        > "$OUT_PROG/scdps.json"

    done
  done
done

echo "[✓] SCDPS extraction complete"
