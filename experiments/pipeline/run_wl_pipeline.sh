#!/usr/bin/env bash
set -e

echo "[WL PIPELINE] Starting WL pipeline"

# ----------------------------------------
# 1. Extract WL AST features
# ----------------------------------------
echo "[WL PIPELINE] Step 1: WL feature extraction"
./experiments/pipeline/run_wl_extract.sh

# ----------------------------------------
# 2. Build WL vocabulary
# ----------------------------------------
echo "[WL PIPELINE] Step 2: Build WL vocabulary"
python3 similarity/build_wl_vocab.py

# ----------------------------------------
# 3. Vectorize WL features
# ----------------------------------------
echo "[WL PIPELINE] Step 3: Vectorize WL features"
python3 similarity/vectorize_wl.py

# ----------------------------------------
# 4. Compute WL similarity matrix
# ----------------------------------------
echo "[WL PIPELINE] Step 4: WL similarity matrix"
python3 evaluation/run_wl_similarity_matrix.py

echo "[WL PIPELINE] WL similarity matrix ready"
