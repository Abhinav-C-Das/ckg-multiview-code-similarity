#!/usr/bin/env bash
set -e

DATA_DIR="data"
OUT_DIR="outputs"
WL_SCRIPT="cpg/scripts/wl/wl_ast.sc"

for PROBLEM in "$DATA_DIR"/*; do
  [ -d "$PROBLEM" ] || continue
  PNAME=$(basename "$PROBLEM")
  echo "[WL] Problem: $PNAME"

  for ROLE in ref s; do
    SRC_DIR="$PROBLEM/$ROLE"
    [ -d "$SRC_DIR" ] || continue

    for SRC in "$SRC_DIR"/*.c; do
      [ -f "$SRC" ] || continue

      PROG=$(basename "$SRC" .c)
      SRC_FILE=$(basename "$SRC")
      OUT_PROG="$OUT_DIR/$PNAME/$ROLE/$PROG"
      CPG="cpgs/$PNAME/$ROLE/$PROG/cpg.bin"

      echo "  └─ WL $ROLE/$PROG"

      if [ ! -f "$CPG" ]; then
        echo "     [ERROR] Missing CPG: $CPG"
        exit 1
      fi

      TARGET_FILE="$SRC_FILE" \
      joern --exit --cpg "$CPG" \
        --script "$WL_SCRIPT" \
        > wl.out 2>/dev/null

      sed -n '/^{/,$p' wl.out > "$OUT_PROG/wl_ast.json"

    done
  done
done

echo "[✓] WL AST extraction complete (CPG reused)"
