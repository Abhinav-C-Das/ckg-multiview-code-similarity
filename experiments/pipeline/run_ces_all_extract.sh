#!/usr/bin/env bash
set -e

# --- force project root ---
cd "$(dirname "$0")"
cd ../..

PROBLEMS=$(./experiments/pipeline/list_problems.sh)
for p in $PROBLEMS; do
  echo "=== CES extracting $p ==="

  # students
  for s in data/$p/s/*.c; do
    sid=$(basename "$s" .c)
     ./experiments/pipeline/run_ces_extract.sh "$p" "$sid" s
  done

  # references
  for r in data/$p/ref/*.c; do
    rid=$(basename "$r" .c)
    ./experiments/pipeline/run_ces_extract.sh "$p" "$rid" ref
  done

  # ---- CREATE index.json FOR EACH refs DIR (MANDATORY) ----
  # ---- CREATE index.json FOR EACH refs DIR (SAFE, NO cd) ----
  for rdir in outputs/p*/ref; do
    refs=()
    for d in "$rdir"/*/; do
      refs+=("$(basename "$d")")
    done
    printf '%s\n' "${refs[@]}" | jq -R . | jq -s . > "$rdir/index.json"
  done


done
