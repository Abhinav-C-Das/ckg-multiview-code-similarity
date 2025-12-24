#!/usr/bin/env bash
set -e

for P in data/p*; do
  [ -d "$P" ] || continue
  PROB=$(basename "$P")

  REFS=()
  for R in "$P"/ref/*.c; do
    REFS+=("${PROB}_$(basename "$R" .c)")
  done

  for S in "$P"/s/*.c; do
    SID="${PROB}_$(basename "$S" .c)"

    echo "[WL] evaluating $SID"
    ./experiments/pipeline/run_wl_evaluate.sh \
      "${REFS[@]}" "$SID"
  done
done
