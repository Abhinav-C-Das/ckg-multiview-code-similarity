#!/usr/bin/env bash
set -e

DATA_DIR="data"
OUT_DIR="outputs"
SCRIPTS_DIR="cpg/scripts"

mkdir -p "$OUT_DIR"

for PROBLEM in "$DATA_DIR"/*; do
  [ -d "$PROBLEM" ] || continue
  PNAME=$(basename "$PROBLEM")
  echo "[+] Problem: $PNAME"

  for ROLE in ref s; do
    SRC_DIR="$PROBLEM/$ROLE"
    [ -d "$SRC_DIR" ] || continue

    for SRC in "$SRC_DIR"/*.c; do
      [ -f "$SRC" ] || continue

      PROG=$(basename "$SRC" .c)
      SRC_FILE=$(basename "$SRC")
      OUT_PROG="$OUT_DIR/$PNAME/$ROLE/$PROG"
      CPG_DIR="cpgs/$PNAME/$ROLE/$PROG"
      CPG="$CPG_DIR/cpg.bin"

      mkdir -p "$OUT_PROG"
      mkdir -p "$CPG_DIR"

      mkdir -p "$OUT_PROG"
      echo "  └─ $ROLE/$PROG"

      # -----------------------------------------------
      # 1. Build or reuse CPG (PERSISTENT)
      # -----------------------------------------------
      if [ ! -f "$CPG" ]; then
        echo "     [CPG] building"
        joern-parse "$SRC" --output "$CPG" >/dev/null
      else
        echo "     [CPG] reused"
      fi

      # -----------------------------------------------
      # 2. Canonicalization
      # -----------------------------------------------
      TARGET_FILE="$SRC_FILE" \
      joern --exit --cpg "$CPG" \
        --script "$SCRIPTS_DIR/preprocess/canonicalize.sc" \
        > canon.out 2>/dev/null

      sed -n '/^{/,$p' canon.out > "$OUT_PROG/canonical.json"

      # -----------------------------------------------
      # 3. Structural features
      # -----------------------------------------------
      TARGET_FILE="$SRC_FILE" \
      joern --exit --cpg "$CPG" \
        --script "$SCRIPTS_DIR/structural/basic_structural.sc" \
        > structural.out 2>/dev/null

      sed -n '/^{/,$p' structural.out > "$OUT_PROG/structural.json"

      # -----------------------------------------------
      # 4. Semantic features
      # -----------------------------------------------
      TARGET_FILE="$SRC_FILE" \
      joern --exit --cpg "$CPG" \
        --script "$SCRIPTS_DIR/semantic/basic_semantic.sc" \
        > semantic.out 2>/dev/null

      sed -n '/^{/,$p' semantic.out > "$OUT_PROG/semantic.json"

      # -----------------------------------------------
      # 5. Behavioral features
      # -----------------------------------------------
      TARGET_FILE="$SRC_FILE" \
      joern --exit --cpg "$CPG" \
        --script "$SCRIPTS_DIR/behavioral/basic_behavioral.sc" \
        > behavioral.out 2>/dev/null

      sed -n '/^{/,$p' behavioral.out > "$OUT_PROG/behavioral.json"
 
      # -----------------------------------------------
      # 5.5 Variable role features (CANONICALIZED)
      # -----------------------------------------------
      CANONICAL_JSON="$OUT_PROG/canonical.json" \
      TARGET_FILE="$SRC_FILE" \
      joern --exit --cpg "$CPG" \
        --script "$SCRIPTS_DIR/semantic/variable_roles.sc" \
        > variable_roles.out 2>/dev/null

      sed -n '/^{/,$p' variable_roles.out > "$OUT_PROG/variable_roles.json"

      # -----------------------------------------------
      # 6. Aggregate
      # -----------------------------------------------
      python3 similarity/aggregate_baseline.py "$OUT_PROG"

    done
  done
done

echo "[✓] Joern feature extraction complete (CPG reused)"
