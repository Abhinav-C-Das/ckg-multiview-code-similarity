#!/usr/bin/env bash
set -euo pipefail

echo "[SCDPS] Step 1: Extraction"
bash experiments/pipeline/run_scdps_extract.sh

echo "[SCDPS] Step 2: Build vocab"
python3 similarity/build_scdps_vocab.py

echo "[SCDPS] Step 3: Vectorize"
python3 similarity/vectorize_scdps.py

echo "[SCDPS] Step 4: Normalize"
mkdir -p vectors/scdps
for f in vectors/scdps/*.vec; do
  python3 similarity/normalize_scdps.py "$f" "${f%.vec}.norm.vec"
done

echo "[SCDPS] Step 5: Similarity"
python3 similarity/scdps_similarity.py

echo "[✓] SCDPS pipeline complete"

